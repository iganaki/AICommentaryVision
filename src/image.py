import os
import requests
from openai import OpenAI

class ImageGenerator:
    def __init__(self):
        self.my_api_key = os.getenv("OPENAI_API_KEY", "")
        self.client = OpenAI(api_key=self.my_api_key)

    def create_and_save_image(self, image_prompt, save_path):

        response = self.client.images.generate(
        model="dall-e-3",
        prompt=image_prompt,
        size="1792x1024",
        quality="standard",
        n=1,
        )

        image_url = response.data[0].url

        self.save_image_from_url(image_url, save_path)

    def save_image_from_url(self, image_url, file_path):
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(file_path, 'wb') as file:
                file.write(response.content)