# cv.py - Provides Computer Vision class
__all__ = ['VisionAPI']

from io import BytesIO
import os
import requests
import json
from PIL import Image

from mixin import APIMixin


# Add your Computer Vision subscription key and endpoint to your environment variables.
if 'AZURE_SUB_KEY' in os.environ:
    sub_key = os.environ['AZURE_SUB_KEY']
if 'AZURE_VISION_ENDPOINT' in os.environ:
    endpoint = os.environ['AZURE_VISION_ENDPOINT']


class VisionAPI(APIMixin, object):
    def __init__(self, sub_key):
        self.analyze_url = endpoint + "vision/v3.1/analyze"
        self.headers = {'Ocp-Apim-Subscription-Key': sub_key}
        self.headers['Content-Type'] = 'application/octet-stream'
        self.params = {'visualFeatures': 'Categories,Description,Color'}

    def analyse(self, image: str):
        """
        params:
        image: url of image file to be analysed.
        """
        img = open(image, 'rb').read()
        response = requests.post(self.analyze_url, headers=self.headers, params=self.params, data=img, json=None)
        response.raise_for_status()
        analysis = response.json()
        return analysis["description"]["captions"][0]["text"].capitalize()

if __name__ == '__main__':
    image = 'test.jpg'
    vision = VisionAPI(sub_key)
    input(vision.test())
    descr = vision.analyse(image)
    print(descr)
