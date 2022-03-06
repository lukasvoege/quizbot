import requests
import os

def getOcrText(image_path):
    subscription_key = "584a787eed124115a9636d747172af7f"
    assert subscription_key

    search_url = "https://quizvision.cognitiveservices.azure.com/vision/v3.2/ocr"

    image_data = open(image_path, "rb").read()

    headers = {"Ocp-Apim-Subscription-Key": subscription_key, "Content-Type": "application/octet-stream"}
    params = {"language": "de"}
    response = requests.post(search_url, headers=headers, params=params, data=image_data)
    response.raise_for_status()
    search_results = response.json()

    return search_results

def getTextFromLine(line):
    text = []
    for word in line['words']:
        text.append(word['text'])
    return " ".join(text)


def getQuestionAndAnswers(ocr_result, img_width, img_height):
    question = dict()

    for regions in ocr_result['regions']:
        for line in regions['lines']:
            x1, y1, x2, y2 = [int(x) for x in line['boundingBox'].split(",")]

            # 1.) Question: every line whichs y1 lies between 0.239*height and 0.509*height
            if (0.239*img_height) < y1 < (0.509*img_height):
                question['Q'] = (question.get('Q', "") + " " + getTextFromLine(line)).strip()
            
            # 2.) Answer 1: every line whichs y1 lies between 0.560*height and 0.702*height and whichs x1 is smaller than 0.5*width
            elif ((0.560*img_height) < y1 < (0.702*img_height)) and x1 < 0.5*img_width:
                question['A1'] = (question.get('A1', "") + " " + getTextFromLine(line)).strip()

            # 3.) Answer 2: every line whichs y1 lies between 0.560*height and 0.702*height and whichs x1 is greater than 0.5*width
            elif ((0.560*img_height) < y1 < (0.702*img_height)) and x1 > 0.5*img_width:
                question['A2'] = (question.get('A2', "") + " " + getTextFromLine(line)).strip()

            # 4.) Answer 3: every line whichs y1 lies between 0.702*height and 0.839*height and whichs x1 is smaller than 0.5*width
            elif ((0.702*img_height) < y1 < (0.839*img_height)) and x1 < 0.5*img_width:
                question['A3'] = (question.get('A3', "") + " " + getTextFromLine(line)).strip()

            # 5.) Answer 4: every line whichs y1 lies between 0.702*height and 0.839*height and whichs x1 is greater than 0.5*width
            elif ((0.702*img_height) < y1 < (0.839*img_height)) and x1 > 0.5*img_width:
                question['A4'] = (question.get('A4', "") + " " + getTextFromLine(line)).strip()

    return question

print(getQuestionAndAnswers(getOcrText('capture.jpg'), 535, 983))