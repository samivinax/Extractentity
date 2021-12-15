# -*- coding: utf-8 -*-
"""
Created on Wed Dec 15 18:29:12 2021

@author: Sami
"""

# pip install transformers==4.4.2
# pip install tensorflow
from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline
import re
import pandas as pd
import re
from flask import Flask, request
#pip install openpyxl
#pip install fsspec

app = Flask(__name__)


model_name = 'deepset/roberta-base-squad2'
model_pipe = pipeline('question-answering',model = model_name,tokenizer = model_name)

annotate = pd.read_excel('Pre-Annotation.xlsx',skiprows = [1])
prods = []
plugs = []

for i in annotate.itertuples():
  if i[2] =="PRODUCT":
    prods.append(i[1].lower())
  else:
    plugs.append(i[1].lower())
    
# inp = ''' Hi,

# Please quote renewal and upgrade user tier for the items below:
# Product-J Software Premium Upgrade Tier: 1800 users to 3000 User license
# Tempo Timesheets - time tracking & reports cloud
# Upgrade Tier:  1800 users to 3000 User license

# Thank you.'''


def extractdata(inp):
  inp = inp.lower()
  inp = inp.replace('-',' hyphen ')
  inp = re.sub(r'[^\w]',' ',inp)
  inp = inp.replace(' hyphen ','-')
  found_prod = [x for x in inp.split() if x in prods]
  found_plug = [x for x in inp.split() if x in plugs]

  found_prod = list(set(found_prod))
  found_plug = list(set(found_plug))

  prod_res = []
  if len(found_prod) > 0:
    question = "How many users for product"
    for it in found_prod:
      q = question.replace("product",it)
      temp = {}
      mod_input = {
          'question':q,
          'context': inp
      }
      res = model_pipe(mod_input)
      temp['Product'] = it
      temp['Users'] = res['answer']
      temp['Score'] = res['score']
      prod_res.append(temp)

  plug_res = []
  if len(found_plug) > 0:
    for it in found_plug:
      temp = {}
      temp['Product'] = it
      temp['Users'] = 'NA'
      temp['Score'] = 'NA'
      plug_res.append(temp)
  final = prod_res + plug_res
  return final

    
@app.route('/')
def extract():
    data = request.get_json()
    inp = data['Input']
    res = extractdata(inp)  
    return res


if __name__ == '__main__':
    app.run()
