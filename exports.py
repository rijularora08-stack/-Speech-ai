from io import BytesIO
from reportlab.pdfgen import canvas


def create_txt_file(content):
    """
    Creates a TXT download file
    """

    return content.encode("utf-8")


def create_pdf_file(title, content):
    """
    Creates a PDF download file
    """

    buffer = BytesIO()

    pdf = canvas.Canvas(buffer)

    pdf.setTitle(title)

    text = pdf.beginText(50, 800)

    for line in content.split("\n"):
        text.textLine(line)

    pdf.drawText(text)

    pdf.save()

    buffer.seek(0)

    return buffer
