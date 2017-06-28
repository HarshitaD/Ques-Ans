def get_questions(doc=-1):
    doc = nlp(doc)
    doc_save = str(doc)
    print(doc_save)
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
        x=x.strip()
        x = x[0].upper() + x[1:]
        x_new = x
        if(x[-2]==' '):
            x = x[:-2]+'?'
        elif(x[-1] in ['.',',','!',';',':',' ']):
            x = x[:-1]+'?'
        elif(x[-1].isalpha()):
            x=x+'?'
            x_new = x
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
        return x_new
        
#        return x

    def get_new_words(word,ext):
        try:
            new_words = wn.synset(str(word)+ext).lemma_names()
            new_words = [x.replace('_',' ') for x in new_words]
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
        
        
############ What - dep -obj
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
            
        
## Entitiy questions
        
    for word in nlp(str(sent)).ents:
        s=word.start
        e=word.end
        if(word.label_ == 'ORG'):
            ent_ques('which organization')
        elif(word.label_ == 'PERSON'):
            ent_ques('who')
        elif(word.label_ in ['FACILITY','GPE','LOCATION']):
            ent_ques('which location')
        elif(word.label_ in ['EVENT']):
            a = str(word).lower().split()
            b = ['decade','year','month','day','minute','hour','second','decades','years','months','days','minutes','hours','seconds']
            if (not set(a).isdisjoint(b) ):
                ent_ques('how long')
            else:
                ent_ques('which event')
        elif(word.label_ in ['DATE']):
            a = str(word).lower().split()
            b = ['decade','year','month','day','minute','hour','second','decades','years','months','days','minutes','hours','seconds']
            if (not set(a).isdisjoint(b) ):
                ent_ques('how long')
            else:
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

### How / Why
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

    d = defaultdict(list)
    for Question,Answer in data:
        Ans = str(Answer)
        if(str(Ans)[-1]=='.'):
            Ans = Ans[:-1]
        d['Answer: '+str(Ans)].append('Question: '+str(Question))  
        d['Answer: '+str(Ans)] = list(set(d['Answer: '+str(Ans)]))
#            d['Question: '+str(Question)] = list(set(d['Question: '+str(Question)]))
    for index, row in cmu_ques.iterrows():
        valid_ques = 0
        x = str(row['Question'])
        y = str(row['Answer'])
        temp = alphas.sub('',x).split()
        useful_words = [word for word in temp if word.lower() not in wh_words+pronouns and lemmatizer.lemmatize(word,'v') not in aux_verb]
        if(y.strip().lower() not in wh_words+pronouns and len(useful_words)>0):
            valid_ques=1
        if(str(row['Sentence']).strip().lower()==str(doc_save).strip().lower() and valid_ques==1):
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

#
#def get_questions_text(inpath = '/home/harshita/Desktop/Question_Generation/Input Text.txt' ,import_needed=1, outpath= '/home/harshita/Desktop/Question_Generation/Output Question Answers.json'):
#    
#    with open(inpath, 'r') as myfile:
#        x=myfile.read()
#        
#    x = re.sub("[\(\[].*?[\)\]]", "",x)
#    
#    data3 = dict()
#    y = [x.strip() for x in x.split('\n')]
#    for j in range(0,len(y)):
#        data2 = dict()
#        doc = nlp(y[j])
#        sents = list(doc.sents)
#        for i in range(0,len(sents)):
#            try:
#                temp = get_questions(str(sents[i]))
#                data2['Sentence: '+str(sents[i]) ] =  temp
#            except:
#                pass
#        data3['Paragraph '+str(j+1)] = data2
#    # Write JSON file
#    with io.open(outpath, 'w',
#                 encoding='utf8') as outfile:
#        str_ = json.dumps(data3,indent=4, sort_keys=True,separators=(',', ': '), ensure_ascii=False)
#        outfile.write(to_unicode(str_))
#    
#
#### EDIT 4: Extract simple sentence
##command prompt, output formats, 
#
#
#if __name__ == "__main__":
#   
#    (get_questions_text())