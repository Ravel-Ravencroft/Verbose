# dummy data
data = [
    ['Student ID','Date and Time','Attendance'],
    ['w179669','13.3.2021 8am','absent'],
    ['w179455','21.4.2021 5pm','late'],
    ['w179187','5.11.2021 2pm','present'],
    ['w179423','6.9.2021 6am','late']
]

# creating a new pdf
fileName = 'pdfTable.pdf'

from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.pagesizes import letter

pdf = SimpleDocTemplate(
    fileName,
    pagesize=letter
)
# creating a table
from reportlab.platypus import Table
table = Table(data)

# styling the table
from reportlab.platypus import TableStyle
from reportlab.lib import colors

style = TableStyle([
    # main row styles
    ('BACKGROUND', (0,0), (2,0), colors.mediumslateblue),
    ('TEXTCOLOR', (0,0), (-1,0), colors.black),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('FONTSIZE', (0,0), (-1,0), 16),
    ('FONTNAME', (0,0), (-1,-1), 'Courier-Bold'),
    ('BOTTOMPADDING', (0,0), (-1,0), 12),
    ('BACKGROUND', (0,1), (-1,-1), colors.lightskyblue),
])
table.setStyle(style)

# generating different colored rows
rowNumber = len(data)
for i in range(1, rowNumber):
    if i % 2 == 0:
        backgroundcolor = colors.deepskyblue
    else:
        backgroundcolor = colors.lightskyblue

    tablestyle1 = TableStyle(
        [('BACKGROUND', (0,i), (-1,i), backgroundcolor)]
    )
    table.setStyle(tablestyle1)

# borders
tablestyle2 = TableStyle(
    [
        ('BOX', (0,0), (-1,-1), 2, colors.black),
        ('GRID', (0,1), (-1,-1), 2, colors.black),
    ]
)
table.setStyle(tablestyle2)

# passing the elements to the table
elements = []
elements.append(table)

pdf.build(elements)