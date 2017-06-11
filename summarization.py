# -*- coding: utf-8 -*-
"""
@author: Cynthia Mora Olmedo
"""
'''
To be able to interact with parser, their server needs to be running
locally

to do so, computer must have StanfordCoreNLP installed and must
run the following line through the command. We also installed pycorenlp wrapper package:
https://github.com/smilli/py-corenlp/blob/master/README.md


java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer -port 9000 -timeout 15000

will run on port 9000 in local computer by default. Can change this to whatever port user chooses to use.

'''

import nltk
#from nltk import sent_tokenize #sentence tokenizing can also be done using nltk

from pycorenlp import StanfordCoreNLP
nlp = StanfordCoreNLP('http://localhost:9000')#this depends on what port you choose to host server

'''
Takes in a list of reviews obtained from scrap data from trip advisor page.
Since we are only taking the first page,We are only expecting like 5- 7 reviews
Instead of seperating summary phrases into pos/ neg, we will just output the top 
6 things talked about. So to dothis we need to put all reviews together as a collective
text that discusses the hotel.
'''    
def sentences(reviews):
    sentenceList=[]
    for review in reviews:
        review1 = review.split('.')#split review into sentences
        for i in review1:#add each sentence to a list
            sentenceList.append(i)
    return sentenceList
        
review_sentences = sentences(reviews)
'''
Takes in a list of sentence of all reviews from the hotel. Then uses the parser 
and returns a list of adjectival modification 
'''
def summarization(reviews):
    features = []
    output = nlp.annotate(reviews, properties={'annotators': 'tokenize,ssplit,pos,depparse,parse','outputFormat': 'json'})
    print(output['sentences'][0]['parse'])
    
    #TODO: iterate thorugh tree, pull out any amod dependencies. Then make tuples that switches the order
    #of the data extracted- amods are in this order(noun/verb, adjective/adverb), we need to flip it around
    
    return features
    
'''
Our group could not understand the api of the parser so we were not able to finish the summarization portion of the assignment.
The code above creates a parse tree of pos tags and phrases like NP or VP. I know the depparse part is refering to dependencies but 
I was unable to find how to go about obtaining dependencies
'''


    
    
    


