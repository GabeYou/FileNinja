from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
import os
import json

def detect_document(path):
    """Detects document features in an image."""
    from google.cloud import vision

    client = vision.ImageAnnotatorClient()

    with open(path, "rb") as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.document_text_detection(image=image)

    for page in response.full_text_annotation.pages:
        paragraph_coords = {}
        paragraph_num = 0
        
        for block in page.blocks:
            for paragraph in block.paragraphs:
                text = ""
                paragraph_num += 1    

                for word in paragraph.words:
                    text += "".join([symbol.text for symbol in word.symbols])+" "

                paragraph_coords[paragraph_num] = text

                print(text)

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )
    
    return paragraph_coords

def add_to_pdf(paragraph_coords, name):
    doc = SimpleDocTemplate(name+"to_text.pdf",
                        pagesize=letter,
                        rightMargin=72,
                        leftMargin=72,
                        topMargin=65,
                        bottomMargin=18)
    
    width, height = letter
    styles = getSampleStyleSheet()
    flowables = []
    style = getSampleStyleSheet()
    
    myStyle = ParagraphStyle('custom',
                            fontName="Helvetica",
                            fontSize=16,
                            parent=style['Heading2'],
                            spaceAfter=14)
    
    for pnum in paragraph_coords:
        para = Paragraph("- " + paragraph_coords[pnum], myStyle)
        para.wrap(width, height)
        flowables.append(para)

    doc.build(flowables)

    return {"path": os.getcwd() + name}
    # return doc