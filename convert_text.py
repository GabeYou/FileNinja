from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
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

    words_coords = {}

    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            # print(f"\nBlock confidence: {block.confidence}\n")
            text = ""
            indent = "\t"

            for paragraph in block.paragraphs:
                # print(indent+"Paragraph confidence: {}".format(paragraph.confidence))
                text = indent*2

                for word in paragraph.words:
                    print(f'{word.bounding_box.vertices[0].x}, {word.bounding_box.vertices[0].y}')
                    #add_to_pdf(word, "".join([symbol.text for symbol in word.symbols]))
                    text += "".join([symbol.text for symbol in word.symbols])+" "
                    words_coords["".join([symbol.text for symbol in word.symbols])] = (word.bounding_box.vertices[0].x, word.bounding_box.vertices[0].y)

                # for word in paragraph.words:
                #     word_text = "".join([symbol.text for symbol in word.symbols])
                #     print(
                #         "Word text: {} (confidence: {})".format(
                #             word_text, word.confidence
                #         )
                #     )

                    # for symbol in word.symbols:
                    #     print(
                    #         "\tSymbol: {} (confidence: {})".format(
                    #             symbol.text, symbol.confidence
                    #         )
                    #     )
                    
                                        # for symbol in word.symbols:
                    #     print(
                    #         "\tSymbol: {} (confidence: {})".format(
                    #             symbol.text, symbol.confidence
                    #         )
                    #     )
                # print(text)

    if response.error.message:
        raise Exception(
            "{}\nFor more info on error messages, check: "
            "https://cloud.google.com/apis/design/errors".format(response.error.message)
        )
    
    return words_coords

path = "C:\\Users\\nahle\\OneDrive\\Desktop\\Screenshot 2023-11-04 112207.png"

def add_to_pdf(word_coords):
    c = canvas.Canvas("demo5_pdf.pdf", pagesize=(1001, 748)) # (5.03*inch, 3.78*inch) demo2

    for text in word_coords:
        c.drawString(word_coords[text][0], 748-word_coords[text][1], text)

    # image_path = os.path.join(os.getcwd(), "python_logo.png")
    # c.drawImage(image_path, 50, 400, width=150, height=150)

    c.save()

words_coords = detect_document(path)
add_to_pdf(words_coords)
# detect_document("C:\\Users\\nahle\\OneDrive\\Desktop\\Screenshot 2023-11-04 140017.png")


# from google.api_core.client_options import ClientOptions
# from google.cloud import documentai  # type: ignore

# # TODO(developer): Uncomment these variables before running the sample.
# project_id = "noted-processor-404115"
# location = "us"  # Format is "us" or "eu"
# file_path = "C:\\Users\\nahle\\OneDrive\\Desktop\\236lec01_annotated.pdf"
# processor_display_name = "YOUR_PROCESSOR_DISPLAY_NAME4" # Must be unique per project, e.g.: "My Processor"


# def quickstart(
#     project_id: str,
#     location: str,
#     file_path: str,
#     processor_display_name: str = "My Processor",
# ):
#     # You must set the `api_endpoint`if you use a location other than "us".
#     opts = ClientOptions(api_endpoint=f"{location}-documentai.googleapis.com")

#     client = documentai.DocumentProcessorServiceClient(client_options=opts)

#     # The full resource name of the location, e.g.:
#     # `projects/{project_id}/locations/{location}`
#     parent = client.common_location_path(project_id, location)

#     # Create a Processor
#     processor = client.create_processor(
#         parent=parent,
#         processor=documentai.Processor(
#             type_="OCR_PROCESSOR",  # Refer to https://cloud.google.com/document-ai/docs/create-processor for how to get available processor types
#             display_name=processor_display_name,
#         ),
#     )

#     # Print the processor information
#     print(f"Processor Name: {processor.name}")

#     # Read the file into memory
#     with open(file_path, "rb") as image:
#         image_content = image.read()

#     # Load binary data
#     raw_document = documentai.RawDocument(
#         content=image_content,
#         mime_type="application/pdf",  # Refer to https://cloud.google.com/document-ai/docs/file-types for supported file types
#     )

#     # Configure the process request
#     # `processor.name` is the full resource name of the processor, e.g.:
#     # `projects/{project_id}/locations/{location}/processors/{processor_id}`
#     request = documentai.ProcessRequest(name=processor.name, raw_document=raw_document)

#     result = client.process_document(request=request)

#     # For a full list of `Document` object attributes, reference this page:
#     # https://cloud.google.com/document-ai/docs/reference/rest/v1/Document
#     document = result.document

#     # Read the text recognition output from the processor
#     print("The document contains the following text:")
#     print(document.text)

# quickstart(project_id, location, file_path, processor_display_name)