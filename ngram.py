import multiprocessing
from multiprocessing import Pool
from multiprocessing import Process, Value, Manager
cpu_count = multiprocessing.cpu_count()
manager = Manager()
verbs = manager.list()

import re
upper = "([A-Z])"
from os import listdir
from os.path import isfile, join 
import csv
import nltk
#nltk.download('wordnet')
from nltk.stem.wordnet import WordNetLemmatizer
#nltk.download('averaged_perceptron_tagger')
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize

import time
print(time.ctime())
start = time.time()
stop_words = set([])
def load_stop_words(filename):
    for line in open(filename):
        line = line.strip()
        stop_words.add(line)
    print ("Added", len(stop_words), "stop words.")
load_stop_words("./stop_words_en.txt")

mypath = '/shared/corpora-tmp/news_corpora/nyt/csv/'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
#print(len(onlyfiles))
#onlyfiles = [onlyfiles[0]]
#csv.field_size_limit(100000000)

#verb_set = {}
#verb_pair = {}
#count_article = 0

def contain_punc(text):
    punc = '''!()[]{};:'"\,<>./?@#$%^&*_~+'''
    for p in punc:
        if p in text:
            return True
    return False

def my_process(file):
    while True:
        with open(mypath + file, newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for text in reader:
                text = text[-1].replace('\n','')
                #if ":" in text: text = text.replace(":","") # added by me
                text = re.sub(":" + upper,":. " + "\\1",text)
                text = re.sub("." + upper + upper + upper,". " + "\\1" + "\\2" + "\\3", text)
                #print(text)
                #if "To the Editor" in text: text = text.split("To the Editor")
                article = text
                #count_article += 1
                #if count_article % 100 == 0:
                #    print(count_article)
                #    print(time.time() - start)
                if 1:
                #for article in text:
                    #print(article)
                    #s_index_and_verb = set([])
                    #s_num = len(sent_tokenize(article))
                    #for s_index, s in enumerate(split_into_sentences(text.lower())):
                    for s_index, s in enumerate(sent_tokenize(article)):
                        #print(s)
                        pos_tags = nltk.pos_tag(word_tokenize(s.lower()))
                        for pos_tag in pos_tags:
                            verb = WordNetLemmatizer().lemmatize(pos_tag[0],'v')
                            if pos_tag[1] in ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"] and verb not in stop_words:
                                if contain_punc(verb):
                                    continue
                                #if verb in verb_set.keys():
                                #    verb_set[verb] += 1
                                #else:
                                #    verb_set[verb] = 1
                                    #print(verb)
                                    #print(pos_tag)
                                verbs.append((verb, 1))
                                #if len(verbs) % 100 == 0:
                                    #print(len(verbs))

with Pool(processes=cpu_count) as pool:
    list_of_return_statements = pool.map(my_process, onlyfiles)      
                                
verb_dict = {}
for verb in verbs:
    if verb[0] in verb_dict.keys():
        verb_dict[verb[0]] += 1
    else:
        verb_dict[verb[0]] = 1
        
import pickle

##To save in file
with open('verb_dict.pkl','wb') as f:
    pickle.dump(verb_dict, f)
"""                            
                            s_index_and_verb.add((s_index, verb))
                print("s_index_and_verb", s_index_and_verb, "\n")
                for siav_1 in s_index_and_verb:
                    for siav_2 in s_index_and_verb:
                        if siav_1[0] <= min(siav_2[0] + 3, s_num - 1) and siav_1[0] >= max(siav_2[0] - 3, 0) and siav_1[1] != siav_2[1]:
                            if (siav_1[1], siav_2[1]) not in verb_pair.keys():
                                verb_pair[(siav_1[1], siav_2[1])] = 1
                            else:
                                verb_pair[(siav_1[1], siav_2[1])] += 1

#print(verb_pair)                                            
#print(verb_set)



text = "tion.JOHN ROSA"
text = re.sub("." + upper + upper + upper, ". " + "\\1" + "\\1" + "\\2" + "\\2" + "\\3" + "\\3", text)
print(text)



for (a, b) in verb_pair.keys():
    if a == "fall":
        print(b)
"""