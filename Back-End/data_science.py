import librosa
import numpy as np
import pandas as pd

from os import listdir, path, remove
from keras.callbacks import EarlyStopping
from keras.layers import Dense, Dropout
from keras.models import Sequential
from keras.utils.np_utils import to_categorical
from sklearn.preprocessing import LabelEncoder, StandardScaler


TRAIN = "Train"
VAL = "Validate"
TEST = "Test"

count = 0
TRAIN_SIZE = 0
VAL_SIZE = 0


def acquire_dataframe(directory):
    global TRAIN_SIZE
    global VAL_SIZE

    # List the files and add them to the Pandas Dataframe
    dataframe = pd.DataFrame( listdir("Dataset/" + directory) )

    # Renaming the column name to file
    dataframe = dataframe.rename(columns = {0:'file'})

    # We create an empty list where we will append all the speaker ids for each row of our dataframe by slicing the file name since we know the id is the first number before the dash
    speaker = []
    for i in range( 0, len(dataframe) ):
        speaker.append(dataframe['file'][i].split('-')[0])

    # We now assign the speaker to a new column 
    dataframe['speaker'] = speaker

    if directory is TRAIN:
        TRAIN_SIZE = dataframe.shape[0]

    elif directory is VAL:
        VAL_SIZE = dataframe.shape[0]

    return dataframe

def extract_features(files):
    #Progress Marker
    global count

    directory = "Dataset/" + (TRAIN if (count < TRAIN_SIZE) else VAL if (count < (TRAIN_SIZE + VAL_SIZE) ) else TEST)

    # Sets the name to be the path to where the file is in my computer
    file_name = path.join( path.abspath(directory) + '/' + str(files.file) )
    
    # Loads the audio file as a floating point time series
    X, sample_rate = librosa.load(file_name, res_type = 'kaiser_fast')
    
    # Generate Mel-frequency cepstral coefficients (MFCCs) from a time series 
    mfccs = np.mean(librosa.feature.mfcc(y = X, sr = sample_rate, n_mfcc = 40).T, axis = 0)
    
    # Generates a Short-time Fourier transform (STFT) to use in the chroma_stft
    stft = np.abs( librosa.stft(X) )
    
    # Computes a chromagram from a waveform or power spectrogram.
    chroma = np.mean(librosa.feature.chroma_stft(S = stft, sr = sample_rate).T, axis = 0)
    
    # Computes a mel-scaled spectrogram.
    mel = np.mean(librosa.feature.melspectrogram(X, sr = sample_rate).T, axis = 0)
    
    # Computes spectral contrast
    contrast = np.mean(librosa.feature.spectral_contrast(S = stft, sr = sample_rate).T, axis = 0)
    
    # Computes the tonal centroid features (tonnetz)
    tonnetz = np.mean(librosa.feature.tonnetz(y = librosa.effects.harmonic(X), sr = sample_rate).T, axis = 0)

    count += 1
    print( "Processing: Clip " + str(count) )

    return mfccs, chroma, mel, contrast, tonnetz

def process_dataframe(dataframe, file_name):
    global count
    file_path = "Dataset/" + file_name + ".npy"

    if path.exists(file_path):
        features_label = np.load(file_path, allow_pickle=True)
        count += (TRAIN_SIZE if file_name is TRAIN else VAL_SIZE)

    else:
        features_label = dataframe.apply(extract_features, axis = 1)

        if file_name in (TRAIN, VAL):
            np.save(file_path, features_label)

    features = []
    for i in range( 0, len(features_label) ):
        features.append(np.concatenate( (
            features_label[i][0],
            features_label[i][1], 
            features_label[i][2], 
            features_label[i][3],
            features_label[i][4]), axis = 0) )

    return np.array(features)

def rebuild():
    file_name = path.abspath("Dataset")
    remove(file_name + "/Train.npy")
    remove(file_name + "/Validate.npy")

    process_dataframe(acquire_dataframe(TRAIN), TRAIN)
    process_dataframe(acquire_dataframe(VAL), VAL)

    print("Datasets Rebuilt and Saved!")

def check_voice():
    train_df = acquire_dataframe(TRAIN)
    val_df = acquire_dataframe(VAL)
    test_df = acquire_dataframe(TEST)

    X_train = process_dataframe(train_df, TRAIN)
    X_val = process_dataframe(val_df, VAL)
    X_test = process_dataframe(test_df, TEST)

    y_train = np.array(train_df['speaker'])
    y_val = np.array(val_df['speaker'])

    # Hot encoding y
    lb = LabelEncoder()
    y_train = to_categorical( lb.fit_transform(y_train) )
    y_val = to_categorical( lb.fit_transform(y_val) )

    ss = StandardScaler()
    X_train = ss.fit_transform(X_train)
    X_val = ss.transform(X_val)
    X_test = ss.transform(X_test)

    # Build a simple dense model with early stopping and softmax for categorical classification, remember we have 30 classes
    model = Sequential()

    model.add( Dense(193, input_shape = (193,), activation = 'relu') )
    model.add( Dropout(0.1) )

    model.add( Dense(128, activation = 'relu') )
    model.add( Dropout(0.25) )

    model.add( Dense(128, activation = 'relu') )
    model.add( Dropout(0.5) )

    model.add( Dense( (TRAIN_SIZE/4), activation = 'softmax') )

    model.compile(loss = 'categorical_crossentropy', metrics = ['accuracy'], optimizer = 'adam')

    early_stop = EarlyStopping(monitor = 'val_loss', min_delta = 0, patience = 100, verbose = 1, mode = 'auto')

    model.fit(X_train, y_train, batch_size = 256, epochs = 100, validation_data = (X_val, y_val), callbacks = [early_stop])

    predictions = model.predict_classes(X_test)

    predictions = lb.inverse_transform(predictions)

    test_df['predictions'] = predictions

    accuracy = ( 1 - round( len(test_df[ test_df['speaker'] != test_df['predictions'] ]) / len(test_df), 3) ) * 100
    print(accuracy)

    return accuracy
    # return True if accuracy == 100 else False

i = 0
y = 0

while i < 5:
    y += check_voice()

print(str(y) + "%")