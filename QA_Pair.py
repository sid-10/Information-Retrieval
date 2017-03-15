Corpus: Question-Answer pairs
Input: Question
Output: Ranked list of answers; The system does not know which is the most relevant answer.
Statistics Calculated : Precision, Recall, NDCG
Note: The questions whose answers are yes and no are discarded.

print("Importing Libraries.Please Wait...")

    
import csv
import re
import sklearn
import nltk
import math
import enchant
import operator
import collections
from nltk.stem.porter import *
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from scipy.sparse import csr_matrix, find
from enchant.checker import SpellChecker

from nltk.corpus import wordnet as wn



nltk.download('wordnet')
nltk.download("stopwords")    
d = enchant.request_dict("en_US")
chkr = SpellChecker("en_US")
stop = set(stopwords.words('english'))


flatten = lambda l: [item for sublist in l for item in sublist]

def flatten2(x):
    result = []
    for el in x:
        if isinstance(x, collections.Iterable) and not isinstance(el, str):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result

 
names=[]
ages=[]
ArticleTitle=[]
Question=[]
Answer=[]
DifficultyFromQuestioner=[]
DifficultyFromAnswerer=[]
ArticleFile=[]
Covered=[]
Actual=[]
Rank=[]
iRank=[]
rel=[]
word_set = set()
train_set = list()
dictionaries={}
documents_list = list()

line_count = 0

with open("question_answer_pairs.txt") as tsv:
    for line in csv.reader(tsv, dialect="excel-tab"): #You can also use delimiter="\t" rather than giving a dialect.
        line_count += 1
        document = list()
        
        ArticleTitle.append(line[0])
        Question.append(line[1])
        Answer.append(line[2])
        Covered.append(0)
        Rank.append(0)
        iRank.append(0)
        rel.append(0)
        stemmer = PorterStemmer()


        temp_list = list()
        temp_list.append(re.sub("[^\w]", " ",  line[2]).split())  #Remove Special Characters
      #  print("\n\n\n\nAfter Special Character Removal:\n\n\n\n")

        temp_list = flatten(temp_list)

        document = temp_list
        document = [x.lower() for x in document]
        document = [word for word in document if word not in stop]   #Remove Stop Words
        
     #   print("\n\n\n\nAfter Stopword Removal:\n\n\n\n")


        #print(document)
        
        temp_list = document
        
        document = [stemmer.stem(word) for word in temp_list]
    #    print("\n\n\n\nAfter Stemming:\n\n\n\n")
        #print(document)
        train_set.append(' '.join(document))
        documents_list.append(document)
        word_set = set(word_set).union(set(document))
    



for x in range (0,line_count):
    doc = 'doc%d' % x 
    dictionaries[doc] = {}
    dictionaries[doc] = dict.fromkeys(word_set,0) 


for x in range (0,line_count):
    doc = 'doc%d' % x 
    #print("X = ",x)
    for word in documents_list[x-1]:
        dictionaries[doc][word] += 1

    

vectorizer = TfidfVectorizer(vocabulary=word_set)
matrix = vectorizer.fit_transform(train_set)

matrix2 = matrix.toarray()






while True:         # Loop continuously
    print("\nEnter Search Query ('exit0' without the single-quotes to terminate) :")
    inp = input()   # Get the input
    chkr.set_text(inp)
    inp = inp.lower()
    
    
    #inp = stemmer.stem(inp)
    test_set=list()
    test_set.append(inp)
    #print("Modified Input : ",inp)

    temp_list = list()
    temp_list_stemmed = list()
    temp_list = list(re.sub("[^\w]", " ",  inp).split())  #Remove Special Characters
    input_text = list(temp_list)
    
    #print(temp_list)
    if inp == "exit0":       # Terminate
        break
    else:
        #print("\nInitial temp_list :",temp_list)
        print("\nProcessing.Please Wait...")
        temp_list = [word for word in temp_list if word not in stop]   #Remove Stop Words
        #print("\nInitial temp_list :",temp_list)
        for i in range(0,len(temp_list)):
            
                if(temp_list[i] not in stop):
        
                    temp_list_stemmed.append(stemmer.stem(temp_list[i]))
            
        to_break = 0;
        if(len(temp_list)==0):
            print("Please refine search query to include more non-stopword terms!!!\n")
            
        else:    
            abc = list()
            abc = list(temp_list)
            #abc = flatten(abc)
            #print("\nInitial abc :",abc)
            for j in range(0,len(temp_list)):
                
                #word = wn.synsets('relative', 'n')[0]
                #hypos = lambda s:s.hyponyms()
                #print("\nPLAIN:\n",list(word.closure(hypos)))
                #abc = synset.name.split('.')[0] for synset in wn.synsets('dog')
                #print("\nMODDED:\n",(synset.name().split('.')[0] for synset in wn.synsets('dog')))
               # print("\nCUR:",temp_list[j],"\n")
                for ss in wn.synsets(temp_list[j]):
                   #print(ss.name().partition('.')[0])
                    maybespecial = list()
                    maybespecial.append(re.sub("[^\w]", " ",  ss.name().partition('.')[0]).split())  #Remove Special Characters
                abc.append(maybespecial)
                abc = flatten2(abc)


                
                
                #print("\nMid abc :",abc)
            temp_list2 = list()
            abc = list(set(abc))
            #print("\nFinal abc :",abc)
            for i in range(0,len(abc)):
            
                if(abc[i] not in stop):
        
                    temp_list2.append(stemmer.stem(abc[i]))
            
            if(to_break == 0):
                output_dict = dict()
                for j in range(0,len(temp_list2)):
                    search_val = vectorizer.vocabulary_.get(temp_list2[j])
                   # print("temp_list[j] : ",temp_list[j])
                   # print("Search_val : ",search_val)
                    if(search_val is None):
                        continue
                            
                    for k in range(0, matrix2.shape[0]):
                        if(matrix2[k][search_val]>0):
                            if((k+1) in output_dict):
                                #print("\nAlready dict term exists\n")
                                output_dict[k+1] +=  matrix2[k][search_val]
                            else:
                                #print("\nNew dict term entry\n")
                                output_dict[k+1] =  matrix2[k][search_val]
                            to_break = 1

                #print("Non Sorted Dict : \n\n\n",output_dict)        
                   
            ###print("\n\n\nTEMP LIST : ",temp_list_stemmed)    
            for i in range(0,len(documents_list)):
               
                #print("i: ",i," Set : tpl2 :",set(temp_list2))
                #print("i: ",i," Set : doc :",set(documents_list[i]))
                if(set(temp_list2) < set(documents_list[i])):
                    if((i+1) in output_dict):
                        output_dict[i+1]+=0.25
                    else:
                        output_dict[i+1] = 0.10
                if(set(temp_list_stemmed) < set(documents_list[i])):
                    #print("\n\n\n MATCHED !!!! "))    
            
                    if((i+1) in output_dict):
                        output_dict[i+1]+=2
                    else:
                        output_dict[i+1] = 1
#            print("Non Sorted Dict : \n\n\n",output_dict)        
#            print("Sorted Dict : \n")  
#            print(sorted_dict)
            a_keys = sorted(output_dict, key=output_dict.get, reverse=True)
            doc_counter = 1
            for r in a_keys:
                if(output_dict[r]<0.65):
                    break;

                print("Rank : ",doc_counter,"Custom Score : ",output_dict[r])
                print("\nProbable Answer : ", Answer[r-1]," Probable Question : ",Question[r-1],"\n")
                Covered[r-1] = 1
                Rank[r-1] = doc_counter
                doc_counter+=1
            #Matrix1 = [[0 for x in range(doc_counter)] for y in range(2)]
            #doc_counter = 1
            #one_ctr = 0
            #    if(output_dict[r]<0.65):
            #        break;

 #               Matrix[0][one_ctr] = doc_counter
  #              Matrix[1][one_ctr] = 
  #              doc_counter+=1
  #              one_ctr+=1



            print("\nActual Answers : ")
            for sy in range(0,len(Question)+1):
                Actual.append(0)
            for sy in range(0,len(Question)):
                first_s = set()

                for item in input_text:
                    first_s.add(item.lower())
                second_s = re.sub("[^\w]", " ",  Question[sy]).split()
                second_s = [element.lower() for element in second_s]
                #if(pop_ctr>8):
                    
                if(first_s == set(second_s)):
                    print("\nFound Actual Ans : ",Answer[sy],"Actual Question : ",Question[sy])
                    Actual[sy] = 1
                    rel[sy] = 1
                



            retrieved=0
            relevant=0
            relevantandretrieved=0
            for lim in range(0,len(Covered)):
                if(Actual[lim] == 1):
                    relevant+=1
                
                if(Covered[lim] == 1):
                    retrieved+=1
                    if(Actual[lim] == 1):
                         relevantandretrieved+=1
            total_DCG = 0
            for lim in range(0,len(Rank)):
                if(Rank[lim]>0):
                    #print("\n Rank : ",Rank[lim]," rel :",rel[lim])
                    reldivlog = rel[lim]/(math.log(Rank[lim]+1,2))
                    total_DCG+=reldivlog

            
            rank_count = 1
            rel.sort(reverse=True)
            for lim in range(0,len(rel)):
                if(rel[lim]<=0):
                    break
                iRank[lim] = rank_count
                rank_count +=1
            #print("\n iRank : ",iRank)
            #print("\n rel : ",rel)
            
            total_iDCG = 0
            for lim in range(0,len(iRank)):
                if(iRank[lim]>0):
                    #print("\n iRank : ",iRank[lim]," iRel :",rel[lim])
                    reldivlog = rel[lim]/(math.log(iRank[lim]+1,2))
                    total_iDCG+=reldivlog

               
            print("\nPrecision : ",relevantandretrieved/retrieved)
            print("\nRecall : ",relevantandretrieved/relevant)
            print("\n DCG : ",total_DCG)
            print("\n iDCG : ",total_iDCG)
            print("\nnDCG : ",total_DCG/total_iDCG)
            

            if(doc_counter == 1):
                print("No Documents Found.")
            
            if(len(output_dict) == 0):
                print("No Documents Found.")
                err_counter1 = 0
                i = 1
                flag_break = 0
                for err in chkr:
                    if(flag_break == 0):
                        print(" The following words may be misspelled :")
                        flag_break = 1
                    print(i," : ", err.word)
                    print("Possible Corrections : ", d.suggest(err.word))
                    i+=1
                    err_counter1 += 1
                
                            
            else:
                err_counter2 = 0
                for err in chkr:
                    print("\nProbable Misspelled Word : ", err.word)
                    print("\nPossible Corrections : ", d.suggest(err.word))
                    err_counter2 += 1

                
