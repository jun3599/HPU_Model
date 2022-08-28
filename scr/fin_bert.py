from os import truncate
import torch
from transformers import AutoTokenizer,  AutoModelForSequenceClassification, pipeline
import pandas as pd 
from tqdm import tqdm 
tqdm.pandas()

# load model
tokenizer = AutoTokenizer.from_pretrained("snunlp/KR-FinBert-SC")
model =  AutoModelForSequenceClassification.from_pretrained("snunlp/KR-FinBert-SC")
sentiment_classifier = pipeline('sentiment-analysis', tokenizer=tokenizer, model=model)

# # load model
# tokenizer = AutoTokenizer.from_pretrained("jaehyeong/koelectra-base-v3-generalized-sentiment-analysis")
# model = AutoModelForSequenceClassification.from_pretrained("jaehyeong/koelectra-base-v3-generalized-sentiment-analysis")
# sentiment_classifier = TextClassificationPipeline(tokenizer=tokenizer, model=model)


# import data 
data = pd.read_excel('D:/Users/wnsgnl/downloads/sentences.xlsx')
data.drop_duplicates(subset=['sentence'])
data = data.iloc[:1000,:]

data['sa'] = data.sentence.progress_apply(lambda x: sentiment_classifier(str(x)[:511]))
data.to_excel('D:/Users/wnsgnl/Desktop/paper_master2/analysis/data/sentiment_test_fin_Bert_SC.xlsx')
print(data)



# 