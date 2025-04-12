# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1lXUbszNrTmVjkZ21f-sS_AcFJ5A_y9n4
"""

from google.colab import userdata
from google import genai
client = genai.Client(api_key =userdata.get('GOOGLE_API_KEY') )

sample_pdf = client.files.upload(file="/content/gemini.pdf")

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=["generate three quiz questions based on this pdf and return questions and multiple choice as a json file with questions named question and options named options and the answer named answer", sample_pdf],
)
print(response.text)

text = response.text
text = text[len("```json"):]
text = text[:text.index("```")]

import json

data =json.loads(text)
for i in data:

  response = client.models.generate_content(
      model="gemini-2.0-flash",
      contents=["can you return a quote directly from this pdf that contains the answer to" + i['question'], sample_pdf],
  )
  print(response.text)

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=["can you return a quote directly from this pdf that contains the answer to <In what year did scientists discover a 6,000-year-old winery in an Armenian cave?>", sample_pdf],
)
print(response.text)

