#Corpus: Question and corresponding document pairs
#Input: Question
#Output: Ranked list of matching documents. The system does not know which is the most relevant document.
#Statistics Calculated: Precision, Recall, NDCG

print("Importing Libraries.Please Wait...")
import csv
import re
import sklearn
import nltk
import enchant
import math
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
quest=[]


flatten = lambda l: [item for sublist in l for item in sublist]

def flatten2(x):
    result = []
    for el in x:
        if isinstance(x, collections.Iterable) and not isinstance(el, str):
            result.extend(flatten(el))
        else:
            result.append(el)
    return result


ArticleTitle=[]
Question=[]
ArticleLoc=[]
Covered=[]
Actual=[]

Rank=[]
iRank=[]
rel=[]


word_set = set()
train_set = list()
dictionaries={}
documents_list = list()
first_main = set()
second_main = set()
DictRank = {}                
Dictrel = {}                
DictiRank = {}                


line_count = 0
print("\nLoading Data...")
with open("question_answer_pairs.txt") as tsv:
    for line in csv.reader(tsv, dialect="excel-tab"): #You can also use delimiter="\t" rather than giving a dialect.
        line_count += 1
        document = list()
        #print("\nline[2]",line[2])
        #print("\nline[3]",line[3])
        #print("\nline[4]",line[4])
        #print("\nline[5]",line[5])
        ArticleTitle.append(line[0])
        Question.append(line[1])
        Covered.append(0)
        Rank.append(0)
        iRank.append(0)
        rel.append(0)
        
        ArticleLoc.append(line[5])

for set_no in range(1,5):
    for file_no in range(1,11):
    
        line_count += 1
        document = list()
        


        document = list()
        ###print("data/set",set_no,"/a",file_no,".txt.clean")
        filename = "data/set"+str(set_no)+"/a"+str(file_no)+".txt.clean"

        if(set_no == 4 and file_no == 8):
            f = open(filename,"r",encoding="latin_1");
        else:
            f = open(filename,"r",encoding="utf8");
        #print("I : ",str(i));
        lines = f.readlines();
        for j in lines:
            #print len(lines)
            #print j
                    
            document.append(j)


        stemmer = PorterStemmer()


        temp_list_B = list()
        for line in document:
            temp_list_B.append(re.sub("[^\w]", " ",  line).split())  #Remove Special Characters
      #  print("\n\n\n\nAfter Special Character Removal:\n\n\n\n")

        temp_list_B = flatten(temp_list_B)

        document = temp_list_B
        document = [x.lower() for x in document]
        document = [word for word in document if word not in stop]   #Remove Stop Words
        
     #   print("\n\n\n\nAfter Stopword Removal:\n\n\n\n")


        #print(document)
        
        temp_list_B = document
        
        document = [stemmer.stem(word) for word in temp_list_B]
    #    print("\n\n\n\nAfter Stemming:\n\n\n\n")
        #print(document)
        train_set.append(' '.join(document))
        documents_list.append(document)
        word_set = set(word_set).union(set(document))



for set_no in range(1,5):
    for file_no in range(1,11):
        doc = 'data/set%d/a%d' %  (set_no,file_no)
        dictionaries[doc] = {}
        dictionaries[doc] = dict.fromkeys(word_set,0) 

for set_no in range(1,5):
    for file_no in range(1,11):
        doc = 'data/set%d/a%d' %  (set_no,file_no)
        for word in documents_list[(set_no-1)*10+(file_no-1)]:
            dictionaries[doc][word] += 1

    

vectorizer = TfidfVectorizer(vocabulary=word_set)
matrix = vectorizer.fit_transform(train_set)

matrix2 = matrix.toarray()


print("\nNote : According to the given instructions, the program does not take Yes/No answer questions into account.")
                



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
    temp_list = list(re.sub("[^\w]", " ",  inp).split())  #Remove Special Characters
    input_text = list(temp_list)
    
    #print(temp_list)
    if inp == "exit0":       # Terminate
        break
    else:

        #temp_list = flatten(temp_list)
        temp_list = [word for word in temp_list if word not in stop]   #Remove Stop Words
        
        
        to_break = 0;
        if(len(temp_list)==0):
            print("Please refine search query to include more non-stopword terms!!!\n")
            
        else:
            print("Processing. Please Wait...")
            abc = list()
            abc.append(temp_list)
            abc = flatten(abc)
            ###print("\nInitial abc :",abc)
            for j in range(0,len(temp_list)):
                
                #word = wn.synsets('relative', 'n')[0]
                #hypos = lambda s:s.hyponyms()
                #print("\nPLAIN:\n",list(word.closure(hypos)))
                #abc = synset.name.split('.')[0] for synset in wn.synsets('dog')
                #print("\nMODDED:\n",(synset.name().split('.')[0] for synset in wn.synsets('dog')))
                ###print("\nCUR:",temp_list[j],"\n")
                maybespecial = list()
                for ss in wn.synsets(temp_list[j]):
               ###     print(ss.name().partition('.')[0])
                    maybespecial.append(re.sub("[^\w]", " ",  ss.name().partition('.')[0]).split())  #Remove Special Characters
               ###     print("\nmaybe:",maybespecial,"\n")
                
                abc.append(maybespecial)
                abc = flatten2(abc)


                
                
            ###    print("\nMid abc :",abc)
            temp_list2 = list()
            abc = list(set(abc))
            ###print("\nFinal abc :",abc)
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
                   
                
            for i in range(0,len(documents_list)):
                #print("i: ",i," Set : tpl2 :",set(temp_list2))
                #print("i: ",i," Set : doc :",set(documents_list[i]))
                if(set(temp_list2) < set(documents_list[i])):
                    if((i+1) in output_dict):
                        output_dict[i+1]+=0.25
                    else:
                        output_dict[i+1] = 0.10
#            print("Non Sorted Dict : \n\n\n",output_dict)        
#            print("Sorted Dict : \n")  
#            print(sorted_dict)
            a_keys = sorted(output_dict, key=output_dict.get, reverse=True)

            doc_counter = 1
            for r in a_keys:
                if(output_dict[r]<0.2):
                    break;
                #if(quest[r-1]=="Yes" or quest[r-1]=="yes" or quest[r-1]=="No" or quest[r-1]=="no" or quest[r-1]=="Yes." or quest[r-1]=="yes." or quest[r-1]=="No." or quest[r-1]=="no."):
                #    continue;
                print("\n\nRank : ",doc_counter,"Custom Score : ",output_dict[r])
                print("\nProbable Document : ","data/set%d/a%d" % (math.ceil(r/10),r%11),"\n")
                DictRank["data/set"+str(math.ceil(r/10))+"/a"+str(r%11)] = doc_counter                
                Dictrel["data/set"+str(math.ceil(r/10))+"/a"+str(r%11)] = 0               



                first_main.add("data/set"+str(math.ceil(r/10))+"/a"+str(r%11))
                Rank[r-1] = doc_counter
                
                Covered[r-1] = 1
                doc_counter+=1

                

            print("\nActual Matching Locations : ")
            for sy in range(0,len(Question)+1):
                Actual.append(0)
            for sy in range(0,len(Question)):
                first_s = set()
                for item in input_text:
                    first_s.add(item.lower())
                second_s = re.sub("[^\w]", " ",  Question[sy]).split()
                second_s = [element.lower() for element in second_s]
                    
                if(first_s == set(second_s)):
                    print("\nActual Location : ",ArticleLoc[sy])
                    Actual[sy] = 1
                    Dictrel[ArticleLoc[sy]] = 1               

                
                    second_main.add(ArticleLoc[sy])
                
               

            
            
            retrieved=len(first_main)
            relevant=len(second_main)
            relevantandretrieved=len(first_main & second_main)


           # print("\nRank : ",Rank)
           # print("\nrel : ",rel)

            total_DCG = 0
            for key in DictRank.keys():
                if(DictRank[key]>0):
                    #print("\n Rank : ",DictRank[key]," rel :",Dictrel[key])
                    reldivlog = Dictrel[key]/(math.log(DictRank[key]+1,2))
                    total_DCG+=reldivlog

            
            optimal_relevance = list()
            for k,v in Dictrel.items():
                optimal_relevance.insert(0,v)

            optimal_relevance.sort(reverse=True)
            
                
            rank_count = 1
            for lim in range(0,len(optimal_relevance)):
                if(optimal_relevance[lim]<=0):
                    break
                iRank[lim] = rank_count
                rank_count +=1
            #print("\n iRank : ",iRank)
            #print("\n rel : ",rel)
            
            total_iDCG = 0
            for lim in range(0,len(iRank)):
                if(iRank[lim]>0):
#                    print("\n iRank : ",iRank[lim]," iRel :",optimal_relevance[lim])
                    reldivlog = optimal_relevance[lim]/(math.log(iRank[lim]+1,2))
                    total_iDCG+=reldivlog

            




            
            print("\nPrecision : ",relevantandretrieved/retrieved)
            print("\nRecall : ",relevantandretrieved/relevant)
            print("\nDCG : ",total_DCG)
            print("\niDCG : ",total_iDCG)
            print("\nnDCG : ",total_DCG/total_iDCG)
            



            if(doc_counter == 1):
                print("No Documents with a High Match Found.\nHowever the following documents had some Match:\n")
                ctr = 1
                for r in a_keys:
                    if(ctr<4):
                        print("\nCustom Score : ",output_dict[r])
                        print("\nProbable Document : ","data/set%d/a%d" % (math.ceil(r/10),r%11),"\n")
                        ctr+=1
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

                
