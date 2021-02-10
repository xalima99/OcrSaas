import os
import boto3

def image_ocrer(documentName: str) -> dict:
    # Read document content
    with open(documentName, 'rb') as document:
        imageBytes = bytearray(document.read())

    # Amazon Textract client
    textract = boto3.client('textract')

    # Call Amazon Textract
    response = textract.detect_document_text(Document={'Bytes': imageBytes})

    #print(response)

    # Print detected text
    res = {}
    for idx, item in enumerate(response["Blocks"]):
        if item["BlockType"] == "LINE":
            res[idx - 1] = item["Text"]
            
    return res    


print(image_ocrer('card.jpeg'))