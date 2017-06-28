    
    
    def get_questions(doc=-1):
        
    #    if doc==-1:
    #        doc = input('Input the sentence to see questions from it: ')
        doc = nlp(doc)
        sents = list(doc.sents)
        
        sent = sents[0]
        
        
        ents = str(doc.ents).split()
        
        global data
        data = list()
        # PART 1: Facts
        
        ### Conv
        #### Convert to Question format
        
        def as_ques(x):
            print(x)
            x=x.strip()
            x = x[0].upper() + x[1:]
            if(x[-2]==' '):
                x = x[:-2]+'?'
            elif(x[-1] in ['.',',','!',';',':',' ']):
                x = x[:-1]+'?'
            elif(x[-1].isalpha()):
                x=x+'?'
            print(x)
#           replaceList=[]
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
#    #                elif(word.pos_ == 'ADV'):
#    #                    new_words = get_new_words(word,'.r.01')
#    #                    if(len(new_words)>1):
#    #                        replaceList.append((word,new_words))
#                            
#    #        print('Original Question: ', x, '\n')
#            
#            x_new = x
#            for y in replaceList:
#                x_new = x_new.replace(' '+str(y[0]).strip()+' ',' ('+'/'.join(y[1])+') ')
#             return x_new
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
            data.append((x,y))
        
                
    #        x = language_check.correct(x,tool.check(x))
        
        print('\n','    Original Sentence: ', sent, '\n')
        
        aux_verb = ['be','can','could','dare','do','have','may','might','must','need','ought','shall','should','will','would']
         
        i=-1
        j=-1
        ques_using_is=0
        for word in sent:
    #        print(word.lemma_,word.tag_)
            if(word.lemma_ in aux_verb):
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
                ques = str(q_word).title()+ ' ' + str(sent)
                ques = as_ques(ques)
    #            print('Question: ',ques)
    #            print('Answer: ' 'Yes' '\n')
                add_data(ques,'Yes')
    #            print('i=',i,' j=',j,' q_word=',q_word)
    
        
            elif(word.tag_ =='VBZ' and word.lemma_ not in aux_verb and ques_using_is==0):
        #        print(3)
                q_word = 'does'
        #        print(word,word.tag_)
                j = word.i
                if(i!=-1):
                    if (i<j):
                        ques = str(q_word).title() + ' ' + first_lower(str(sent[0:i])) + ' ' +str(sent[(i+1):j]) + ' ' + lemmatizer.lemmatize(str(sent[j]),'v')+ ' ' +str(sent[(j+1):])
                    else:
                        ques = str(q_word).title() + ' ' + first_lower(str(sent[0:j])) + ' ' + lemmatizer.lemmatize(str(sent[i]),'v')+ ' '  +str(sent[(j+1):i]) +  ' ' +str(sent[(j+1):])
                else:
        #            print(j)
                    ques = q_word+ ' ' + first_lower(str(sent[0:j])) + ' ' + lemmatizer.lemmatize(str(sent[j]),'v') + ' ' +  str(sent[(j+1):])
                ques = as_ques(ques)
    #            print('Question: ',ques)
    #            print('Answer: ', 'Yes', '\n')
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
        
        # PART 2: WHO
        
        def ent_ques(ent_phrase):
    #        if(j>e):
    #            ques = ent_phrase+' '+q_word+' '+str(sent[0:s]).strip()+' '+str(sent[e:i]).strip()+' '+lemmatizer.lemmatize(str(sent[j]),'v')+ ' '  +str(sent[(j+1):]) 
    #        else:
    #            ques = ent_phrase+' '+q_word+' ' +str(sent[0:j]).strip()+' '+lemmatizer.lemmatize(str(sent[j]),'v')+' '+str(sent[(j+1):s]).strip()+ ' '  +str(sent[e:]) 
                
            ques = first_lower(str(sent[0:s]).strip())+ ' ' + ent_phrase + ' ' +str(sent[e:]).strip()
    #        ques = language_check.correct(ques,tool.check(ques))
            ques = as_ques(ques)
    #        print('Question: ',ques)
    #        print('Answer: ', str(word)[0].upper() + str(word)[1:], '\n')
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
            elif(word.label_ in ['DATE','TIME','EVENT']):
                if (str(word).split() in ['decade','year','month','day','minute','hour','second','decades','years','months','days','minutes','hours','seconds']):
                    ent_ques('how long')
                else:
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
                
    #### EDIT 4
    # Step 1: Get Chunks
    ## Step 2: corresponding input for ent_ques
        def filtered_chunks(doc, pattern):
            nounList = []
            for chunk in (doc).noun_chunks:
        #        print(chunk)
                signature = ''.join(['<%s>' % w.tag_ for w in chunk])
                in_ent = list(set(str(chunk).split()) & (set(ents_list)))
                if pattern.match(signature) is not None and len(in_ent)==0 :
                    yield chunk
                
        n_phr = list(filtered_chunks((sent), pattern))
    
    #    print(ents[0])
        for x in n_phr:
            if( x not in ents):
                s = x.start
                e = x.end
                word=x
                if (str(sent[s-1]).lower()=='to'):
                    word = 'to '+str(word)
                    s = s-1
                    ent_ques('where')
                else:
                    ent_ques('what')
    
    ##### EDIT 5: Divide by verb questions
    # Step 1: get noun1*, verb2*, noun3*, verb4*, noun5*
    # Step 2: Ques: replace * before with what, Ans: noun*
    
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
                
#        print(result_merge)
        
        # pos = [2]
        #tag = [3]
        
        for x in result_merge:
            if(x[2])=='VERB':
                i = int(x[0]) 
                j = int(i)
                print(i)
                i_dash = int(result_merge.index(x))
                j_dash = i_dash
                if(result_merge[i_dash+1][2]=='VERB' or result_merge[i_dash+1][3] in ['IN','TO']):
                    j = j+1
#                print(result_merge[i_dash], result_merge[j_dash])
                if(not result_merge[i_dash-1][2]=='VERB'):
                    s = j
                    e = len(sent)
                    word = str(sent[(s+1):e])
                    if(word[-1] in ['.',',','!',';']):
                        word=(word).replace('.','')
                    ques = first_lower(str(sent[0:(s+1)]).strip())+ ' ' + 'what'
                    ques = as_ques(ques)
                    add_data(ques, str(word)[0].upper() + str(word)[1:] )
            if(x[3]=='VBZ'):
                s = 0
                e = i
                word = sent[s:(e)]
                if(str(word[-1]) in ['.',',','!',';']):
                    word=(word).replace('.','')
                ques = 'what' + ' ' +str(sent[(e):]).strip()
                ques = as_ques(ques)
                add_data(ques, str(word)[0].upper() + str(word)[1:] )
                    
                
        
#        for x in sent:
#            if(x.pos_)=='VERB':
#                i = x.i 
#                j = i
#                if(sent[i+1].pos_=='VERB' or sent[i+1].tag_ in ['IN','TO']):
#                    j = j+1
#                print(sent, sent[i], sent[j])
#                if(not sent[i-1].pos_=='VERB'):
#                    s = j
#                    e = len(sent)
#                    word = sent[(s+1):e]
#                    ques = first_lower(str(sent[0:(s+1)]).strip())+ ' ' + 'what'
#                    ques = as_ques(ques)
#                    add_data(ques, str(word)[0].upper() + str(word)[1:])
#    
#            if(x.tag_=='VBZ'):
#                s = 0
#                e = i
#                word = sent[s:(e)]
#                ques = 'what' + ' ' +str(sent[(e):]).strip()
#                ques = as_ques(ques)
#                add_data(ques, str(word)[0].upper() + str(word)[1:])
                    
    
        d = defaultdict(list)
        for Question,Answer in data:
            d['Question: '+str(Question)].append('Answer: '+str(Answer))
            d['Question: '+str(Question)] = list(set(d['Question: '+str(Question)]))
#        print(d)
        
        return d
    
    #sub_toks = [tok for tok in nlp(doc) if (tok.dep_ == "nsubj") ]
    #
    #print(sub_toks) 
    
    #doc= 'Shyam and Ravi go to college together. John has gone to Delhi. Shvet Chakra is going to attend a seminar. '
    
    #doc = 'London is a big city in the United Kingdom. The quick brown fox jumps over the lazy dog. Francoise lives in Paris. \n Reading comprehension is the ability to read text, process it, and understand its meaning. \n Wikipedia is hosted by the Wikimedia Foundation, a non-profit organization that also hosts a range of other projects. '
    
    #doc = 'Interest rate risk is the risk of loss resulting from changes in interest rates'
    #
    #doc = 'The development and establishment of a system for market risk management is extremely important from the viewpoint of ensuring the soundness and appropriateness of a financial institution’s business. '
    #
    #doc = 'Credit Risk refers to the chance that the issuer of the debt security will not meet its obligations of interest and principal payments. '
    #for x in doc:
    #    input('Press any key for a sample sentence.')
    #    get_questions(x)
    
    def get_questions_text(inpath = '/home/harshita/Desktop/Question_Generation/Input Text.txt' ,import_needed=1, outpath= '/home/harshita/Desktop/Question_Generation/Output Question Answers.json'):
        
        with open(inpath, 'r') as myfile:
            x=myfile.read()
        
        data3 = dict()
        y = [x.strip() for x in x.split('\n')]
        print(y)
        for j in range(0,len(y)):
            data2 = dict()
            doc = nlp(y[j])
            sents = list(doc.sents)
            for i in range(0,len(sents)):
                data2['Sentence: '+str(sents[i]) ] =   get_questions(str(sents[i]))
            data3['Paragraph '+str(j+1)] = data2
        # Write JSON file
        with io.open(outpath, 'w',
                     encoding='utf8') as outfile:
            str_ = json.dumps(data3,indent=4, sort_keys=True,separators=(',', ': '), ensure_ascii=False)
            outfile.write(to_unicode(str_))
    
    ### EDIT 4: Extract simple sentence
    #command prompt, output formats, 
    
    
    if __name__ == "__main__":
   
        get_questions_text()    