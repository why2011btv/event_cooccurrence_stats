import stanfordnlp
stanfordnlp.download('en')   # This downloads the English models for the neural pipeline
nlp = stanfordnlp.Pipeline() # This sets up a default neural pipeline in English
doc = nlp("A bus carrying Turkish pilgrims has come under attack in northern Syria , Turkish media and officials say . At least two people , one of them the bus driver , were injured in the attack near the flashpoint city of Homs , reports say . The passengers were returning from the Hajj - the annual Muslim pilgrimage to Mecca , Saudi Arabia - reports say . Private news agency Dogan showed images of the bus with one of its side windows broken inside Turkey . `` We confirm that an attack took place in Syria , '' a foreign ministry official told AFP news agency , without giving any further information , but reiterated Turkey 's warning to its citizens not to visit Syria . Tensions have been running high between Syria and Turkey as Ankara has become increasingly vocal in its criticism of President Bashar al-Assad 's crackdown on anti-government protests in his country . Clashes again erupt in Cairo as Egypt 's health ministry confirms at least 20 people have died and 1,750 have been wounded in a weekend of violence .")
doc.sentences[0].print_dependencies()
doc.sentences[1].print_dependencies()

doc = nlp("trump's budget favors military, inflating deficit")
for token in doc: 
    print(token, token.pos_) 
#doc.sentences[0].print_dependencies()


import nltk
nltk.download('averaged_perceptron_tagger')
from nltk.tokenize import word_tokenize
text = "Trump's Budget Favors Military, Inflating Deficit."
text = split_into_sentences(text.lower())
print(text)
text = word_tokenize(text[0])
print(text)
nltk.pos_tag(text)


stop_words = set([])
def load_stop_words(filename):
    for line in open(filename):
        line = line.strip()
        stop_words.add(line)
    print ("Added", len(stop_words), "stop words.")
    
load_stop_words("/home1/w/why16gzl/KAIROS/event_abstraction/elmo/stop_words_en.txt")


if "have" in stop_words:
    print("yes")
    
# -*- coding: utf-8 -*-
import re
upper = "([A-Z])"
numbers  = "([0-9])"
alphabets= "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"

def split_into_sentences(text):
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(numbers + "[.]" + numbers,"\\1<prd>\\2",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    #if ".''" in text: text = text.replace(".\"","\".") # added by me
    #if "!''" in text: text = text.replace("!\"","\"!") # added by me
    #if "?''" in text: text = text.replace("?\"","\"?") # added by me
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    if "''" in text: text = text.replace("''","") # added by me
    #if "''." in text: text = text.replace("\".",".\"") # added by me
    #if "''!" in text: text = text.replace("\"!","!\"") # added by me
    #if "''?" in text: text = text.replace("\"?","?\"") # added by me
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences



from os import listdir
from os.path import isfile, join 
import csv
import nltk
#nltk.download('wordnet')
from nltk.stem.wordnet import WordNetLemmatizer
#nltk.download('averaged_perceptron_tagger')
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize

stop_words = set([])
def load_stop_words(filename):
    for line in open(filename):
        line = line.strip()
        stop_words.add(line)
    print ("Added", len(stop_words), "stop words.")
load_stop_words("/home1/w/why16gzl/KAIROS/event_abstraction/elmo/stop_words_en.txt")

mypath = '/shared/corpora-tmp/news_corpora/nyt/csv/'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
csv.field_size_limit(100000000)

verb_set = set([])
verb_pair = {}
count_article = 0

for file_name in onlyfiles:
    with open(mypath + file_name, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for text in reader:
            text = text[-1].replace('\n','')
            #if ":" in text: text = text.replace(":","") # added by me
            text = re.sub(":" + upper,":. " + "\\1",text)
            text = re.sub("." + upper + upper + upper,". " + "\\1" + "\\2" + "\\3", text)
            #print(text)
            #if "To the Editor" in text: text = text.split("To the Editor")
            article = text
            if 1:
            #for article in text:
                #print(article)
                s_index_and_verb = set([])
                s_num = len(sent_tokenize(article))
                #for s_index, s in enumerate(split_into_sentences(text.lower())):
                for s_index, s in enumerate(sent_tokenize(article)):
                    #print(s)
                    pos_tags = nltk.pos_tag(word_tokenize(s.lower()))
                    for pos_tag in pos_tags:
                        verb = WordNetLemmatizer().lemmatize(pos_tag[0],'v')
                        if pos_tag[1] in ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"] and verb not in stop_words:
                            verb_set.add(verb)
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