import librosa
import numpy as np
import pandas as pd

from os import listdir, path
from keras.callbacks import EarlyStopping
from keras.layers import Dense, Dropout
from keras.models import Sequential
from keras.utils.np_utils import to_categorical
from sklearn.preprocessing import LabelEncoder, StandardScaler


count = 0

TRAIN = "Train"
VAL = "Validate"
TEST = "Test"


def acquire_dataframe(directory):
    dataframe = pd.DataFrame( listdir("Dataset/" + directory) )
    dataframe = dataframe.rename(columns = {0:'file'})

    speaker = []
    for i in range( 0, len(dataframe) ):
        speaker.append(dataframe['file'][i].split('-')[0])

    dataframe['speaker'] = speaker

    return dataframe

def extract_features(files):
    global count

    directory = "Dataset/" + (TRAIN if (count < 120) else VAL if (count < 210) else TEST)

    file_name = path.join( path.abspath(directory) + '/' + str(files.file) )
    
    X, sample_rate = librosa.load(file_name, res_type = 'kaiser_fast')
    
    mfccs = np.mean(librosa.feature.mfcc(y = X, sr = sample_rate, n_mfcc = 40).T, axis = 0)
    
    stft = np.abs( librosa.stft(X) )
    
    chroma = np.mean(librosa.feature.chroma_stft(S = stft, sr = sample_rate).T, axis = 0)
    
    mel = np.mean(librosa.feature.melspectrogram(X, sr = sample_rate).T, axis = 0)
    
    contrast = np.mean(librosa.feature.spectral_contrast(S = stft, sr = sample_rate).T, axis = 0)
    
    tonnetz = np.mean(librosa.feature.tonnetz(y = librosa.effects.harmonic(X), sr = sample_rate).T, axis = 0)

    count += 1
    print(count)

    return mfccs, chroma, mel, contrast, tonnetz

def process_dataframe(dataframe, file_name):
    global count
    file_path = "Dataset/" + file_name + ".npy"

    if path.exists(file_path):
        features_label = np.load(file_path, allow_pickle=True)
        count += (120 if file_name is TRAIN else 90)
    else:
        features_label = dataframe.apply(extract_features, axis = 1)
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

def initialization():
    process_dataframe(acquire_dataframe(TRAIN), TRAIN)
    process_dataframe(acquire_dataframe(VAL), VAL)

    print("Datasets Proccessed and Saved!")

def check_voice():
    train_df = acquire_dataframe(TRAIN)
    val_df = acquire_dataframe(VAL)
    test_df = acquire_dataframe(TEST)

    X_train = process_dataframe(train_df, TRAIN)
    X_val = process_dataframe(val_df, VAL)
    X_test = process_dataframe(test_df, TEST)

    y_train = np.array(train_df['speaker'])
    y_val = np.array(val_df['speaker'])

    lb = LabelEncoder()
    y_train = to_categorical( lb.fit_transform(y_train) )
    y_val = to_categorical( lb.fit_transform(y_val) )

    ss = StandardScaler()
    X_train = ss.fit_transform(X_train)
    X_val = ss.transform(X_val)
    X_test = ss.transform(X_test)

    model = Sequential()

    model.add( Dense(193, input_shape = (193,), activation = 'relu') )
    model.add( Dropout(0.1) )

    model.add( Dense(128, activation = 'relu') )
    model.add( Dropout(0.25) )

    model.add( Dense(128, activation = 'relu') )
    model.add( Dropout(0.5) )

    model.add( Dense(30, activation = 'softmax') )

    model.compile(loss = 'categorical_crossentropy', metrics = ['accuracy'], optimizer = 'adam')

    early_stop = EarlyStopping(monitor = 'val_loss', min_delta = 0, patience = 100, verbose = 1, mode = 'auto')

    model.fit(X_train, y_train, batch_size = 256, epochs = 100, validation_data = (X_val, y_val), callbacks = [early_stop])

    predictions = model.predict_classes(X_test)

    predictions = lb.inverse_transform(predictions)

    test_df['predictions'] = predictions

    print(test_df[test_df['speaker'] != test_df['predictions']])

    accuracy = ( 1 - round( len(test_df[ test_df['speaker'] != test_df['predictions'] ]) / len(test_df), 3) ) * 100
    print("\nTesting Accuracy: " + str(accuracy) + "%")

    return accuracy

check_voice()
