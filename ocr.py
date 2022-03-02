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


print(getOcrText('./test_images/IMG_4232.PNG'))