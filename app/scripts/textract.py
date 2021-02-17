import os
import boto3

from app.scripts.id_parser import IdCard

def detext_text(imageBytes) -> dict:
    # Read document content
    # with open(documentName, 'rb') as document:
    #     imageBytes = bytearray(document.read())

    try:
        # Amazon Textract client
        textract = boto3.client('textract')

        # Call Amazon Textract
        response = textract.detect_document_text(Document={'Bytes': imageBytes})

        #print(response)

        # Print detected text
        res = []
        for item in response['Blocks']:
            if item['BlockType'] == "LINE":
                res.append(item['Text'])
        
        if len(res):
            card = IdCard(res)
            infos = card.scan()
            return infos
    except Exception as e:
        print(e)
