
# Make it work for Python 2+3 and with Unicode
try:
   to_unicode = unicode
except NameError:
   to_unicode = str

# Import necessary packages
import spacy
nlp = spacy.load('en')
import subprocess
from nltk.stem.wordnet import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
from nltk.corpus import wordnet as wn
import re
pattern = re.compile(r'(<IN>)*(<DT>)*(<JJ>)*(<NN>|<NNS>|<NNP>)+')
w_words = ['when','who','what','why','how','where']
import json
from collections import defaultdict
import pandas as pd
from flask import Flask, request
import re
import io
from fuzzywuzzy import process, fuzz

## Some import word lists
aux_verb = ['be','can','could','dare','do','have','may','might','must','need','ought','shall','should','will','would']

wh_words = ['when','why','how','what','where','who']

pronouns = ['I','me','my','mine', 'we','our','ours', 'us','you','your','yours','he','she' ,'it','him','her','his', 'her\'s','hers','it\'s','its','they','them', 'their','their\'s' ,'theirs']

## Obtaining the words and spaces only given a text
alphas = re.compile('[^a-zA-Z\\s]')


## Function to convert a question text to proper question fomat
def as_ques(x):
    x=x.strip()
    x = x[0].upper() + x[1:]
    if(x[-2]==' '):
        x = x[:-2]+'?'
    elif(x[-1] in ['.',',','!',';',':',' ']):
        x = x[:-1]+'?'
    elif(x[-1].isalpha()):
        x=x+'?'
    ### Uncomment the below to also take the synonyms as given by synsets
#            replaceList=[]
#            for word in nlp(x):
#                if( str(word).lower() not in str(ents).lower() and str(word).lower() not in w_words):
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
#
#            for y in replaceList:
#                x_new = x_new.replace(' '+str(y[0]).strip()+' ',' ('+'/'.join(y[1])+') ')
    return '**IN-HOUSE**' + x




###  Getting new words from the synsets

def get_new_words(word,ext):
    try:
        new_words = wn.synset(str(word)+ext).lemma_names()
        new_words = [x.replace('_',' ') for x in new_words]
        return new_words
    except:
        return [word]




## Convert the first character to lower if it isn't a named entity

def first_lower(s):
    if len(s) == 0 or s.split()[0].lower() in str(ents).lower():
        return s
    else:
        return s[0].lower() + s[1:]




## Input: Question, Answer; Function: Add to golbal 'data' if the answer contains more than just wh_words and aux_verb as defined earlier

def add_data(x,y):
    global data
#            ques_verbs = sum([1 for i in nlp(str(x)) if i.pos_=='VERB'])
#            ans_verbs = sum([1 for i in nlp(str(y)) if i.pos_=='VERB'])
    temp = alphas.sub('',x).split()
    useful_words = [word for word in temp if word.lower() not in wh_words and lemmatizer.lemmatize(word,'v') not in aux_verb]
    if(y.strip().lower() not in wh_words and y.strip().lower() not in pronouns and len(useful_words)>0):
        data.append((x,y))




def isNaN(num):
    return num != num



## Get a question given the ent_phrase and entity
def ent_ques(ent_phrase):
    ques = first_lower(str(sent[0:s]).strip())+ ' ' + ent_phrase + ' ' +str(sent[e:]).strip()
    ques = as_ques(ques)
    add_data(ques, str(word)[0].upper() + str(word)[1:])


    ### Creates the dependent object kinnd of questions
    ### Dep Obj question: If the verb has only one dependent object to the right.
def add_dobj_ques(sent):
    i=-1
    j=-1
    for word in sent:
        dep_obj = 0
        if( not(word.n_rights==0) and [j.dep_ for j in word.children][0] in ['dobj','pobj'] ):
            dep_obj=1
        if(word.pos_=='VERB' and dep_obj==1):
            q_word = 'what'
            j = word.i
            s=0
            e=j
            word = sent[(e+1):]
            ques = str(sent[s:e+1]).strip() + ' ' + q_word
            ques = as_ques(ques)
            add_data(ques, str(word)[0].upper() + str(word)[1:])



def add_ent_ques(sent):
        ## Entity questions: For each entity creates a question and gives the corresponding phrase to be used
    global s,e,word
    for word in nlp(str(sent)).ents:
        s=word.start
        e=word.end

        if(word.label_ == 'PERSON'):
            ent_ques('who')
        # elif(word.label_ == 'ORG'):
        #     ent_ques('which organization')
        elif(word.label_ in ['FACILITY','GPE','LOCATION']):
            ent_ques('which location')
        elif(word.label_ in ['EVENT']):
            a = str(word).lower().split()
            b = ['decade','year','month','day','minute','hour','second','decades','years','months','days','minutes','hours','seconds']
            if (not set(a).isdisjoint(b) ):
                ent_ques('what amount of duration')
            else:
                ent_ques('which event')
        elif(word.label_ in ['DATE']):
            a = str(word).lower().split()
            b = ['decade','year','month','day','minute','hour','second','decades','years','months','days','minutes','hours','seconds']
            if (not set(a).isdisjoint(b) ):
                ent_ques('what amount of duration')
            else:
                ent_ques('which day/month/year')
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

def add_why_how_ques(doc):
        ### How / Why
        sent = doc
        ents = nlp(str(sent)).ents
        ents_list = [str(i) for i in ents]
    # #### EDIT 4
    # # Step 1: Get Chunks
    # ## Step 2: corresponding input for ent_ques
    #     def filtered_chunks(doc, pattern):
    #         nounList = []
    #         for chunk in (doc).noun_chunks:
    #     #        print(chunk)
    #             signature = ''.join(['<%s>' % w.tag_ for w in chunk])
    #             in_ent = list(set(str(chunk).split()) & (set(ents_list)))
    #             if pattern.match(signature) is not None and len(in_ent)==0 :
    #                 yield chunk

    #     n_phr = list(filtered_chunks((sent), pattern))

    # #    print(ents[0])
    #     for x in n_phr:
    #         if( x not in ents):
    #             s = x.start
    #             e = x.end
    #             word=x
    #             if (str(sent[s-1]).lower()=='to'):
    #                 word = 'to '+str(word)
    #                 s = s-1
    #                 ent_ques('where')
    #             else:
    #                 ent_ques('what')

            ## Get the noun phrases from the sentences
        noun_phrase_position = [(s.start, s.end) for s in sent.noun_chunks]
        noun_phrase_text = dict([(s.start, s.text) for s in sent.noun_chunks])
        token_pos = [(i, t.text, t.pos_, t.tag_) for i, t in enumerate(sent)]
        index = 0
        result = []
        for start, end in noun_phrase_position:
            result += token_pos[index:start]
            result.append(token_pos[start:end])
            index = end

        # Convert the sentence to merged noun phrases so that they are not split in ques and ans
        result_merge = []
        for i, r in enumerate(result):
            if len(r) > 0 and isinstance(r, list):
                result_merge.append((r[0][0], noun_phrase_text.get(r[0][0]), 'NOUN_PHRASE', 'NP'))
            else:
                result_merge.append(r)

# Get the verb positions from the result_merge(noun phrase combined version of sent)
        verb_count = 0
        for x in result_merge:
            if(x[2])=='VERB':
                i = int(x[0])
                j = int(i)
                if(verb_count==0):
                    verb_count=verb_count+1
                    verb_i = i
# Get the How questions
# Get the IN-VBG: Ex - By adding

            i = int(x[0])
            j = int(i)
            if(x[3]=='VBG' and sent[i-1].tag_ == 'IN'):
                s = j-2
                e = len(sent)
                word = str(sent[(s+1):e])
                if(verb_count!=0):
                    ques = 'how' + ' ' + first_lower(str(sent[verb_i])) + ' ' +first_lower(str(sent[0:verb_i])) +' '+ first_lower(str(sent[(verb_i+1):(s+1)]))
                else:
                    ques = 'how' + ' ' + first_lower(str(sent[0:(s+1)]))
                ques = as_ques(ques)
                add_data(ques, str(word)[0].upper() + str(word)[1:])

# Get the why questions
# Get the To-VBG: Ex - To complete
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


def add_cmu_ques(d,cmu_ques,doc_save):
# Now add the cmu_ques to the list d

#    print(cmu_ques)

#    doc_save = process.extractOne(doc_save, cmu_ques['Sentence'])[0]
    for index, row in cmu_ques.iterrows():
        temp = alphas.sub('',str(row['Question'])).split()
#        useful_words = [word for word in temp if word.lower() not in wh_words and lemmatizer.lemmatize(word,'v') not in aux_verb]

# If the Sentence from cmu_ques matches doc_save i.e. the input of get_questions add to the list d for this sentence
# If the answer from CMU is Nan, Make it to be 'Yes'
        # if( not doc_save == 'docnotfounderror'):
        #
        #     print(str(row['Sentence']).strip().lower())
        #     print(str(doc_save).strip().lower())
        #
        #     if(str(row['Sentence']).strip().lower()==str(doc_save).strip().lower()):
        #         print('MATCHED')
        #     else:
        #         print('DIDNT MATCH')
        a = str(row['Sentence']).strip().lower()
        b = str(doc_save).strip().lower()
        fuzz_ratio = fuzz.ratio(a,b)

        if(fuzz_ratio > 90 ):
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


def add_cmu_backup_questions(sent):

#    print(' hit the cmu_backup ')

    try:
        rootj = [ w.i for w in sent if w.head is w][0]
        rooti = rootj

        try:
            if (sent[rooti-1].pos_ in ['RB','MD','VERB']):
                rooti = rooti-1
        except:
            pass

        try:
            if (sent[rooti-1].pos_ in ['RB','MD','VERB']):
                rooti = rooti-1
        except:
            pass

        try:
            if (sent[rooti-1].pos_ in ['RB','MD','VERB']):
                rooti = rooti-1
        except:
            pass

        try:
            if (sent[rootj+1].pos_ in ['ADP','IN','TO','VERB']):
                rootj = rootj+1
        except:
            pass
        try:
            if (sent[rootj+1].pos_ in ['ADP','IN','TO','VERB']):
                rootj = rootj+1
        except:
            pass
        try:
            if (sent[rootj+1].pos_ in ['ADP','IN','TO','VERB']):
                rootj = rootj+1
        except:
            pass



        word = str(sent[0:rooti])
        ques = 'what' +' '+ first_lower(str(sent[rooti:]))
        ques = as_ques(ques)
        add_data(ques, str(word)[0].upper() + str(word)[1:])

        word = str(sent[rootj+1:])
        ques = first_lower(str(sent[:rootj+1]))+ ' ' + 'what'
        ques = as_ques(ques)
        add_data(ques, str(word)[0].upper() + str(word)[1:])

    except:
        pass

def match_cmu_sentence(actual_sentences, cmu_sentences):

    def get_top(x):

        temp = process.extractOne(str(x), cmu_sentences)

        if( temp is not None):
            if(temp[1]>90):
    #            global cmu_0_questions
                cmu_0_questions.append(1)
                x = re.sub("[\(\[].*?[\)\]]", "",str(temp[0]))
                return x
            else:
    #            global cmu_0_questions
                cmu_0_questions.append(0)

                x = re.sub("[\(\[].*?[\)\]]", "",str(x))
                return x
        else:
            cmu_0_questions.append(0)

            x = re.sub("[\(\[].*?[\)\]]", "",str(x))
            return x

    y = [map(get_top,x) for x in actual_sentences]

#    [print("ACTUAL: ",xdash,"NEW: ",list(ydash),"END") for xdash in actual_sentences for ydash in y]

    return y


def match_only_cmu_sentence(actual_sentences, cmu_sentences):

    def get_cmu_top(x):

        temp = process.extractOne(str(x), cmu_sentences)

        if( temp is not None):
            if(temp[1]>90):
                return str(x)
            else:
                return 'exactnotfound'
        else:
            return 'lolnotfound'

    y = [map(get_cmu_top,x) for x in actual_sentences]

#    [print("ACTUAL: ",xdash,"NEW: ",list(ydash),"END") for xdash in actual_sentences for ydash in y]

    return y

## Define global data which will be used to collect the questions at each iteration over the word




## Input: Sentence, Output: Questions and Answers from CMU And in-house generator
def get_questions(doc=-1):

    global data, doc_save, sents, sent, ents, i, j, s, e, word, ques, debug_flag, d

    debug_flag=1

    ## Convert the string doc to spacy sent
    doc = nlp(doc)
    sents = list(doc.sents)

    if( len(sents) ==0):
        sent = ''
    else:
        sent = sents[0]


    ## Get the named entities from the doc
    ents = str(doc.ents).split()

    data = list()

    #### STEP 1
    add_dobj_ques(sent)

    #### STEP 2
    add_ent_ques(sent)

    #### STEP 3
    add_why_how_ques(doc)

    #### STEP 4
    try:
        if( not (len(data)==0)):
            cmu_0_questions[sentence_counter] = 1
        else:
            cmu_0_questions[sentence_counter] = 0
    except:
        print('counter setting error')
        pass

    # print('y u no print')
    # print(data)
    # print(cmu_0_questions)

    try:
        if(cmu_0_questions[sentence_counter] == 0):
            add_cmu_backup_questions(sent)
            pass
    except Exception as x:
        print('counter access error')
        print(x, sent)
        pass

# Define d: The output of get_questions and add all the questions from the global data
    d = defaultdict(list)
    for Question,Answer in data:
        Ans = str(Answer)
        if(str(Ans)[-1]=='.'):
            Ans = Ans[:-1]
        d['Answer: '+str(Ans)].append('Question: '+str(Question))
        d['Answer: '+str(Ans)] = list(set(d['Answer: '+str(Ans)]))
#            d['Question: '+str(Question)] = list(set(d['Question: '+str(Question)]))


    #### STEP 4
    add_cmu_ques(d,cmu_ques,doc_save)


    return d

def get_questions_text():

    inpath_init = '/home/harshita/Desktop/Question_Generation/Input.txt'
    inpath = '/home/harshita/Desktop/Question_Generation/Input_new.txt'
    outpath= '/home/harshita/Desktop/Question_Generation/Output.json'
    midpath = '/home/harshita/Desktop/Question_Generation/CMU.txt'

    with open(inpath_init,'r') as myfile:
        x=myfile.read()

    x=  re.sub("[\(\[].*?[\)\]]", "",x)
    print('Input_new: ',x)
    with open(inpath,'w') as myfile:
        myfile.write(x)

    random = subprocess.run(["/home/harshita/Desktop/Question_Generation/run_from_file.sh",inpath, midpath])

    print("completed subprocess\n")

    global cmu_ques, doc_save
    cmu_ques = pd.read_table(midpath,sep='\t',names=['Question','Sentence','Answer','Rank'])

    with open(inpath, 'r') as myfile:
        x=myfile.read()


    actual_sentences = [x.strip() for x in x.split('\n')]
    actual_sentences = [list(nlp(x).sents) for x in actual_sentences if not len(x)==0]

    data3 = dict()
    cmu_sentences=list(set(cmu_ques['Sentence']))
    print(cmu_sentences)

    ### y contains the paragraphs
    global cmu_0_questions, sentence_counter
    sentence_counter = -1
    cmu_0_questions = list()

    y = match_cmu_sentence(actual_sentences,cmu_sentences)

    cmu_y = match_only_cmu_sentence(actual_sentences,cmu_sentences)


    for j in range(0,len(y)):

        data2 = dict()
        doc = list(y[j])
        doc_cmu = list(cmu_y[j])


        if ( doc is not None ):
            sents = [nlp(x) for x in doc]

            for i in range(0,len(sents)):

                sentence_counter = sentence_counter + 1

                global doc_save
                sents_cmu = [nlp(x) for x in doc_cmu]

                if(len(sents_cmu)==0):
                    doc_save = 'docnotfounderror'
                else:
                    doc_save = sents_cmu[i]

#                print(' SENTENCE 1' , sents[i])
                current_sentence = str(sents[i])
                current_sentence  = re.sub("[0-9] .[0-9]", ".",current_sentence )
                current_sentence  = nlp(re.sub("[\(\[].*?[\)\]]", "",current_sentence ))
                print(current_sentence)


                # print('SENTENCE: ', current_sentence)
                # print('SENTENCE COUNTER: ',sentence_counter)
                # print('CMU THREAD: ',cmu_0_questions)


                try:
                    temp = get_questions(str(current_sentence))

                    data2['Sentence: '+str(current_sentence) ] =  temp

                except Exception as inst:
                    print('PASSED')
                    print(type(inst))
                    print(inst)
                    pass


            data3['Paragraph '+str(j+1)] = data2

    print(cmu_0_questions)
    # Write JSON file
    with io.open(outpath, 'w',
                 encoding='utf8') as outfile:
        str_ = json.dumps(data3,indent=4, sort_keys=True,separators=(',', ': '), ensure_ascii=False)
        outfile.write(to_unicode(str_))
    return str_


from flask import Flask,render_template,request,redirect
app_lulu = Flask(__name__)

app_lulu.vars={}

@app_lulu.route('/input_sentences',methods=['GET','POST'])
def input_sentences():
    if request.method == 'GET':
        return render_template('get_input_text.html')
    else:
        #request was a POST
        app_lulu.vars['input_text'] = request.form['input_text']
        print('INPUT: ',app_lulu.vars['input_text'])
        inpath_init = '/home/harshita/Desktop/Question_Generation/Input.txt'

        with open(inpath_init,'w') as myfile:
            myfile.write(app_lulu.vars['input_text'])



        output = get_questions_text()
        print('OUTPUT: ',output)

        return render_template('show_output_layout.html',input_text = app_lulu.vars['input_text'], output = output)

@app_lulu.route('/next_page',methods=['POST'])
def next_page():
    return redirect('/input_sentences')
#
# @app_lulu.route('/usefulfunction_lulu',methods=['GET','POST'])
# def usefulfunction_lulu():
#     return render_template('layout_lulu.html',num=1,question='Which fruit do you like best?',ans1='banana',ans2='mango',ans3='pineapple')

if __name__ == "__main__":
    app_lulu.run(debug=True)
