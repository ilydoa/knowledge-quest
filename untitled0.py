# -*- coding: utf-8 -*-
"""Untitled0.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1lXUbszNrTmVjkZ21f-sS_AcFJ5A_y9n4
"""

from google import genai
client = genai.Client(api_key ='[UR API KEY]')

import json
def fun(txt):
  response = client.models.generate_content(
      model="gemini-2.0-flash",
      contents=["generate three quiz questions based on this text and return questions and multiple choice as a json file with questions named question and options named options and the answer named answer", txt],
  )
  text = response.text
  text = text[len("```json"):]
  text = text[:text.index("```")]
  data= json.loads(text)
  for i in data:
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=["can you return a sentence directly from this text that contains the answer to" + i['question'],txt]
        )
    i["highlight"] = response.text
  return data

text = "One of the first organisms that humans domesticated was yeast. In 2011, while excavating an old graveyard in an Armenian cave, scientists discovered a 6,000 year-old winery, complete with a wine press, fermentation vessels, and even drinking cups. This winery was a major technological innovation that required understanding how to control Sacharomyces, the genus of yeast used in alcohol and bread production."
print(fun(text))

