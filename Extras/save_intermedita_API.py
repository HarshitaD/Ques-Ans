#import inflect
#p = inflect.engine()

import spacy
nlp = spacy.load('en')
#
import subprocess
#### FOR GRAMMAR CHECK
#import language_check
#tool = language_check.LanguageTool('en-US')                                                                                                     
### FOR INFINITIVE FORM
from nltk.stem.wordnet import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
###### WORDNET - FOR SYNONYMS
from nltk.corpus import wordnet as wn
import re
pattern = re.compile(r'(<IN>)*(<DT>)*(<JJ>)*(<NN>|<NNS>|<NNP>)+')
w_words = ['when','who','what','why','how','where']
import json
# Make it work for Python 2+3 and with Unicode
try:
    to_unicode = unicode
except NameError:
    to_unicode = str
# Define data
from collections import defaultdict
import pandas as pd

#from code_without_synonyms_single_ques_ans import get_questions
from flask import Flask, request

def get_questions(doc=-1):
    
#    if doc==-1:
#        doc = input('Input the sentence to see questions from it: ')
    import re 
    
    doc = nlp(doc)
    sents = list(doc.sents)
    
    sent = sents[0]
    
    
    ents = str(doc.ents).split()
    
    global data
    data = list()
    
    aux_verb = ['be','can','could','dare','do','have','may','might','must','need','ought','shall','should','will','would']
    
    wh_words = ['when','why','how','what','where','who']
    
    pronouns = ['I','me','my','mine', 'we','our','ours', 'us','you','your','yours','he','she' ,'it','him','her','his', 'her\'s','hers','it\'s','its','they','them', 'their','their\'s' ,'theirs']
    
    
    cmu_ques = pd.read_table('/home/harshita/Desktop/Question_Generation/Output Text.txt',sep='\t',names=['Question','Sentence','Answer','Rank'])
    
    alphas = re.compile('[^a-zA-Z\\s]')
    
    def as_ques(x):
#            print(x)
        x=x.strip()
        x = x[0].upper() + x[1:]
        if(x[-2]==' '):
            x = x[:-2]+'?'
        elif(x[-1] in ['.',',','!',';',':',' ']):
            x = x[:-1]+'?'
        elif(x[-1].isalpha()):
            x=x+'?'
#            print(x)
#            replaceList=[]
#            for word in nlp(x):
#    #            if( str(word).lower() not in str(ents).lower() and str(word).lower() not in w_words):
#                if(  str(word).lower() not in w_words):
#    #                print(word.pos_,word)
#                    if(word.pos_ == 'VERB'):
#                        new_words = get_new_words(word,'.v.01')
#                        if(len(new_words)>1):
#                            replaceList.append((word,new_words))
#                        
#                    elif(word.pos_ == 'NOUN'):
#                        new_words = get_new_words(word,'.n.01')
#                        if(len(new_words)>1):
#                            replaceList.append((word,new_words))
#                        
#                    elif(word.pos_ == 'ADJ'):
#                        new_words = get_new_words(word,'.a.01')
#                        if(len(new_words)>1):
#                            replaceList.append((word,new_words))
#    
#                    elif(word.pos_ == 'ADV'):
#                        new_words = get_new_words(word,'.r.01')
#                        if(len(new_words)>1):
#                            replaceList.append((word,new_words))
#                            
#    #        print('Original Question: ', x, '\n')
#            
#            x_new = x
#            for y in replaceList:
#                x_new = x_new.replace(' '+str(y[0]).strip()+' ',' ('+'/'.join(y[1])+') ')
#            return x_new
        
        return x

    def get_new_words(word,ext):
        try:
            new_words = wn.synset(str(word)+ext).lemma_names()
            new_words = [x.replace('_',' ') for x in new_words]
#            print(new_words)
            return new_words
        except:
            return [word]
        
    def first_lower(s):
        if len(s) == 0 or s.split()[0].lower() in str(ents).lower():
            return s
        else:
            return s[0].lower() + s[1:]
    
    def add_data(x,y):
        global data
#            ques_verbs = sum([1 for i in nlp(str(x)) if i.pos_=='VERB'])
#            ans_verbs = sum([1 for i in nlp(str(y)) if i.pos_=='VERB'])
        temp = alphas.sub('',x).split()
        useful_words = [word for word in temp if word.lower() not in wh_words+pronouns and lemmatizer.lemmatize(word,'v') not in aux_verb]
        if(y.strip().lower() not in wh_words and y.strip().lower() not in pronouns and len(useful_words)>0):
            data.append((x,y))
    
    def isNaN(num):
        return num != num
    
    def ent_ques(ent_phrase):
        ques = first_lower(str(sent[0:s]).strip())+ ' ' + ent_phrase + ' ' +str(sent[e:]).strip()
        ques = as_ques(ques)
        add_data(ques, str(word)[0].upper() + str(word)[1:])
    
    if (not str(sent[-1])=='?'):
        all_verb_count = sum([1 for i in sent if i.pos_=='VERB'])
        i=-1
        j=-1
        ques_using_is=0
        for word in sent:
    #        print(word.lemma_,word.tag_)
            if(word.lemma_ in aux_verb ):
        #        print(1,word.lemma_,word.i)
                ques_using_is = 1
                i = word.i
                q_word=''
                ques = str(sent[i]).title()+ ' ' +first_lower(str(sent[0:i]))+ ' ' + str(sent[(i+1):])
                ques = as_ques(ques)
    #            print('Question: ',ques)
    #            print('Answer: ' 'Yes' '\n')
                add_data(ques,'Yes')
    #            print('i=',i,' j=',j,' q_word=',q_word)
            
            elif( word.tag_ == 'VBD' and word.lemma_ not in aux_verb and ques_using_is==0):
        #        print(2)
                q_word = 'did'
                j = word.i
                
                if(i!=-1):
                    if (i<j):
                        ques = str(q_word).title() + ' ' + first_lower(str(sent[0:i])) + ' ' +str(sent[(i+1):j]) + ' ' + lemmatizer.lemmatize(str(sent[j]),'v')+ ' ' +str(sent[(j+1):])
                    else:
                        ques = str(q_word).title() + ' ' + first_lower(str(sent[0:j])) + ' ' + lemmatizer.lemmatize(str(sent[i]),'v')+ ' '  +str(sent[(j+1):i]) +  ' ' +str(sent[(j+1):])
                else:
        #            print(j)
                    ques = q_word+ ' ' + first_lower(str(sent[0:j])) + ' ' + lemmatizer.lemmatize(str(sent[j]),'v') + ' ' +  str(sent[(j+1):])
                    
                    
#                ques = str(q_word).title()+ ' ' + str(sent)
                ques = as_ques(ques)
    #            print('Question: ',ques)
    #            print('Answer: ' 'Yes' '\n')
                add_data(ques,'Yes')
    #            print('i=',i,' j=',j,' q_word=',q_word)
    
        
            elif( ( word.tag_ =='VBP' ) and word.lemma_ not in aux_verb):
                q_word = 'do'
                j = word.i
                ques = str(q_word).title()+ ' ' + first_lower(str(sent))
                ques = as_ques(ques)
    #            print('Question: ',ques)
    #            print('Answer: ', 'Yes', '\n')
                add_data(ques,'Yes')
    #            print('i=',i,' j=',j,' q_word=',q_word)
            dep_obj = 0
            if( word.n_rights and [j.dep_ for j in word.children][0] in ['dobj','pobj'] ):
                dep_obj=1   
            if(word.pos_=='VERB' and dep_obj==1):
                q_word = 'what'
                j = word.i
                s=0
                e=j
                word = sent[(e+1):]
                ques = str(sent[s:e+1]).strip() + ' ' + 'what'
                ques = as_ques(ques)
                add_data(ques, str(word)[0].upper() + str(word)[1:])
                
            
        # Subpart 1: Single Name:
            
        for word in nlp(str(sent)).ents:
        #    print(word.label_, word.text, word.start, word.end)
            s=word.start
            e=word.end
            if(word.label_ == 'ORG'):
                ent_ques('which organization')
            elif(word.label_ == 'PERSON'):
                ent_ques('who')
            elif(word.label_ in ['FACILITY','GPE','LOCATION']):
                ent_ques('which location')
            elif(word.label_ in ['EVENT']):
                if (str(word).lower().split() in ['decade','year','month','day','minute','hour','second','decades','years','months','days','minutes','hours','seconds']):
                    ent_ques('how long')
                else:
                    ent_ques('which event')
            elif(word.label_ in ['DATE']):
                ent_ques('which date')
            elif(word.label_ in ['TIME']):
                ent_ques('when')
            elif(word.label_ in ['MONEY','QUANTITY','PERCENT']):
                ent_ques('how much')
            elif(word.label_ == 'CARDINAL'):
                ent_ques('how many')
            elif(word.label_ in ['WORK_OF_ART','PRODUCT']):
                ent_ques('what')
            elif(word.label_ == 'LAW'):
                ent_ques('which law')
    
    #    sent = nlp(doc[0])
        sent = doc
        ents = nlp(str(sent)).ents
        ents_list = [str(i) for i in ents]
                
    
        noun_phrase_position = [(s.start, s.end) for s in sent.noun_chunks]
        noun_phrase_text = dict([(s.start, s.text) for s in sent.noun_chunks])
        token_pos = [(i, t.text, t.pos_, t.tag_) for i, t in enumerate(sent)]
        index = 0
        result = []
        for start, end in noun_phrase_position:
            result += token_pos[index:start]
            result.append(token_pos[start:end])
            index = end
        
        result_merge = []
        for i, r in enumerate(result):
            if len(r) > 0 and isinstance(r, list):
                result_merge.append((r[0][0], noun_phrase_text.get(r[0][0]), 'NOUN_PHRASE', 'NP'))
            else:
                result_merge.append(r)
        
        verb_count = 0
        for x in result_merge:
            if(x[2])=='VERB':
                i = int(x[0]) 
                j = int(i)
                if(verb_count==0):
                    verb_count=verb_count+1
                    verb_i = i
                i_dash = int(result_merge.index(x))
                j_dash = i_dash
                
                while(result_merge[i_dash+1][2]=='VERB' or result_merge[i_dash+1][3] in ['IN','TO',',','CC']):
                    j = j+1
                    j_dash = j_dash+1
                    i_dash = i_dash+1
                
#                print(result_merge[i_dash], result_merge[j_dash])
                if(not result_merge[i_dash-1][2]=='VERB'):
                        
                    s = j
                    e = len(sent)
                    word = str(sent[(s+1):e])
                    if(word[-1] in ['.',',','!',';']):
                        word=(word).replace('.','')
                    
                    if(verb_count==1):
                        if(sent[i].lemma_ in aux_verb):
                            ques = 'what' + ' ' +str(sent[i])+' '+first_lower(str(sent[0:i]).strip())+  ' ' + first_lower(str(sent[i+1:(s+1)]).strip())
                            ques = as_ques(ques)
                            add_data(ques, str(word)[0].upper() + str(word)[1:])
                            
                        elif(x[3]=='VBD'):
                            ques = 'what did'+' '+first_lower(str(sent[0:i]).strip())+ ' ' + lemmatizer.lemmatize(str(sent[i]),'v') + ' ' + first_lower(str(sent[i+1:(s+1)]).strip())
                            ques = as_ques(ques)
                            add_data(ques, str(word)[0].upper() + str(word)[1:])
                        elif(x[3]=='VBZ'):
                            ques = 'what does'+' '+first_lower(str(sent[0:i]).strip())+ ' ' + lemmatizer.lemmatize(str(sent[i]),'v') + ' ' + first_lower(str(sent[i+1:(s+1)]).strip())
                            ques = as_ques(ques)
                            add_data(ques, str(word)[0].upper() + str(word)[1:])
                        elif(x[3]=='VBP'):
                            ques = 'what do'+' '+first_lower(str(sent[0:(s+1)]).strip())
                            ques = as_ques(ques)
                            add_data(ques, str(word)[0].upper() + str(word)[1:])
                            
                    else:
                        ques = first_lower(str(sent[0:(s+1)]).strip())+ ' ' + 'what'
                        ques = as_ques(ques)
                        add_data(ques, str(word)[0].upper() + str(word)[1:])
            
            i = int(x[0]) 
            j = int(i)
            if(x[3]=='VBG' and sent[i-1].tag_ == 'IN'):
                s = j-2
                e = len(sent)
                word = str(sent[(s+1):e])
#                ques = 'how <merge-IN-VBG>' +str(sent[i])+' '+first_lower(str(sent[0:i]).strip())+  ' ' + first_lower(str(sent[i+1:(s+1)]).strip())
                
                if(verb_count!=0):
                    ques = 'how' + ' ' + first_lower(str(sent[verb_i])) + ' ' +first_lower(str(sent[0:verb_i])) +' '+ first_lower(str(sent[(verb_i+1):(s+1)]))
                else:
                    ques = 'how' + ' ' + first_lower(str(sent[0:(s+1)]))
                ques = as_ques(ques)
                add_data(ques, str(word)[0].upper() + str(word)[1:])
                            
            i = int(x[0]) 
            j = int(i)            
            if(x[3]=='VBG' and sent[i-1].tag_ == 'TO'):
                s = j-2
                e = len(sent)
                word = str(sent[(s+1):e])
#                ques = 'how <merge-IN-VBG>' +str(sent[i])+' '+first_lower(str(sent[0:i]).strip())+  ' ' + first_lower(str(sent[i+1:(s+1)]).strip())
                ques = 'why' + ' ' + first_lower(str(sent[0:s+1]))
                ques = as_ques(ques)
                add_data(ques, str(word)[0].upper() + str(word)[1:])

#            i = int(x[0]) 
#            j = int(i)            
#            if(x[3]=='VBZ' ):
#                s = 0
#                e = i
#                word = sent[s:(e)]
#                ques = 'what<VBZ>' + ' ' +str(sent[(e):]).strip()
#                ques = as_ques(ques)
#                add_data(ques, str(word)[0].upper() + str(word)[1:])
    
    d = defaultdict(list)
    for Question,Answer in data:
        Ans = str(Answer)
#        print(Ans)
        if(str(Ans)[-1]=='.'):
            Ans = Ans[:-1]
#            print(Ans)
        d['Answer: '+str(Ans)].append('Question: '+str(Question))  
        d['Answer: '+str(Ans)] = list(set(d['Answer: '+str(Ans)]))
#            d['Question: '+str(Question)] = list(set(d['Question: '+str(Question)]))
        for index, row in cmu_ques.iterrows():
            valid_ques = 0
            x = str(row['Question'])
            y = str(row['Answer'])
            print(x,y)
            temp = alphas.sub('',x).split()
            useful_words = [word for word in temp if word.lower() not in wh_words+pronouns and lemmatizer.lemmatize(word,'v') not in aux_verb]
            if(y.strip().lower() not in wh_words+pronouns and len(useful_words)>0):
                valid_ques=1
            
            if(str(row['Sentence']).strip().lower()==str(sent).strip().lower() and valid_ques==1):
                if(isNaN(row['Answer'])): 
                    d['Answer: '+'Yes'].append('Question: '+str(row['Question']))  
                    d['Answer: '+'Yes'] = list(set(d['Answer: '+'Yes']))
                else: 
                    Ans = (str(row['Answer']))
                    Ans = Ans[0].upper()+Ans[1:]
                    if(str(Ans)[-1]=='.'):
                        Ans = Ans[:-1]
                    d['Answer: '+str(Ans)].append('Question: '+str(row['Question']))  
                    d['Answer: '+str(Ans)] = list(set(d['Answer: '+str(Ans)]))
        
    return d

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
    if request.headers['Content-type'] == 'text/plain':
        text = request.data.decode('ascii')
        with open('Input Text.txt', 'wb') as f:
            f.write(request.data)
        print(text)
        subprocess.run(["/home/harshita/Desktop/CMU_Ques/QuestionGeneration/run_from_file.sh"])
        print("completed subprocess\n")
        x = re.sub("[\(\[].*?[\)\]]", "",text)
#        print(x)
    
        data3 = dict()
        y = [x.strip() for x in x.split('\n')]
        print("Here\n")
        print(y)                                                                                                            
        for j in range(0,len(y)):
            data2 = dict()
            print(y[j]) 
            doc = nlp(y[j])
#            sents = list(doc.sents)
#            print("Inside loop\n")
#            print(sents)
            sents = []
            for d in doc.sents:
                print(d)
                sents.append(d)
            print(sents)
            for i in range(0,len(sents)):
                temp = get_questions(str(sents[i]))
                data2['Sentence: '+str(sents[i]) ] = temp
                print(data2)
            data3['Paragraph '+str(j+1)] = data2
#        print(data3)
        questions_json = json.dumps(data3,indent=4, sort_keys=True,separators=(',', ': '), ensure_ascii=False)
        return questions_json

if __name__ == '__main__':
    app.run(debug=False, port = 4321)