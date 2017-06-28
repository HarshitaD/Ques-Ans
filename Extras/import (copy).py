#import inflect
#p = inflect.engine()

import spacy
nlp = spacy.load('en')
#
#### FOR GRAMMAR CHECK
#import language_check
#tool = language_check.LanguageTool('en-US')                                                                                                     
### FOR INFINITIVE FORM
from nltk.stem.wordnet import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
###### WORDNET - FOR SYNONYMS
from nltk.corpus import wordnet as wn
import re
import spacy
pattern = re.compile(r'(<IN>)*(<DT>)*(<JJ>)*(<NN>|<NNS>|<NNP>)+')
w_words = ['when','who','what','why','how','where']
import json
# Make it work for Python 2+3 and with Unicode
import io
try:
    to_unicode = unicode
except NameError:
    to_unicode = str
# Define data
from collections import defaultdict
import pandas as pd
