from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import Frame, Table, TableStyle

from config import INSTITUTE_START_TIME as time


PAGE_COUNT = 15

def create_pdf(id, data):
    today = datetime.now()

    canvas = Canvas("Student Daily Attendance Records.pdf", pagesize = A4)

    i = 0
    page = 0
    while i < len(data):
        if i%PAGE_COUNT == 0:
            canvas.setFont("Times-Bold", 30)
            canvas.drawString(210, 750, "Attendance List")

            canvas.setFont("Times-Roman", 16)
            canvas.drawString(50, 700, "Teacher ID: " + id)
            canvas.drawString( 50, 675, "Date Generated: " + today.strftime("%Y-%m-%d") )
            canvas.drawString( 50, 650, "Time Generated: " + today.strftime("%H:%M:%S") )

            rows = []
            rows.append(['Student ID', 'Check-In Time', 'Punctuality'])
            page+=1

        punctuality = "Absent" if data[i]['time'] == "-" else "On Time" if data[i]['time'] <= time else "Late"
        rows.append([data[i]['id'], data[i]['time'], punctuality])

        if i == (len(data)-1) or i == ( (page*PAGE_COUNT)-1 ):
            table = Table(rows, 150, 30)

            tableStyle = TableStyle([
                ('BACKGROUND', (0, 0), (2, 0), colors.deepskyblue),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTSIZE', (0, 0), (-1, 0), 20),
                ('FONT', (0, 0), (-1, -1), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 16),
                ('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),
                ('BOX', (0, 0), (-1, -1), 2, colors.black),
                ('GRID', (0, 0), (-1, -1), 2, colors.black),
            ])

            table.setStyle(tableStyle)
            frame = Frame(50, 0, 500, 625)
            frame.addFromList([table], canvas)
            canvas.drawString( 525, 25, "Page " + str(page) )
            canvas.showPage()

        i+=1

    canvas.save()