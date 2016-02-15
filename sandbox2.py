from reportlab.graphics.barcode import code39
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas


def create_bar_codes():
    """
    Create barcode examples and embed in a PDF
    """
    c = canvas.Canvas("barcodes.pdf", pagesize=letter)
    c.setFont('Helvetica-Bold', 6)

    barcode_value = "3"

    barcode39 = code39.Extended39(barcode_value)
    barcode39std = code39.Standard39(barcode_value, barHeight=20, stop=1)

    x = 1 * mm
    y = 270 * mm

    for code in [
            barcode39,
            barcode39std
            ]:
        code.drawOn(c, x, y)
        w = code.width / 2
        c.drawCentredString(x + w, y - 2 * mm, barcode_value)
        c.drawCentredString(x + w, y - 4 * mm, 'Hello, world!')
        y -= 15 * mm

    c.save()

if __name__ == "__main__":
    create_bar_codes()
