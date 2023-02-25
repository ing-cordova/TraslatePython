import urllib.request
import re
import nltk
from inscriptis import get_text
from nltk import word_tokenize, sent_tokenize
from googletrans import Translator

translator = Translator()

#nltk.download()

cadena = """JavaScript ( JS ) is a lightweight, interpreted, or just -in-time compiled programming language with first-class functions. 
While it is best known as a scripting language (scripting) for web pages, and is used in many non-browser environments , such as Node.js ,
Apache CouchDB , and Adobe Acrobat JavaScript is a prototype-based programming language , multi-paradigm, single-threaded, dynamic, with 
support for object-oriented, imperative, and declarative programming (for example, functional programming). Read more on about JavaScript. 
This section is dedicated to the JavaScript language itself, and not to the parts that are specific to web pages or other host environments. 
For information about specific APIs for Web pages, see Web APIs and the DOM . The standard for JavaScript is ECMAScript (ECMA-262) and the 
API specification for ECMAScript Internationalization (ECMA-402). The documentation on MDN is based entirely on the latest ECMA-262 and 
ECMA-402 preview versions. And in some cases where proposals for new features for ECMAScript have already been implemented in browsers, 
documentation and some MDN articles may make use of some of these features."""
#enlace = "https://es.wikipedia.org/wiki/Python"
#html = urllib.request.urlopen(enlace).read().decode('utf-8')
text = get_text(cadena)

print("############################################")

#Removing square brackets and extra spaces
formatted_article_text = re.sub('[^a-zA-z]', ' ', text)
formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)

sentence_list = nltk.sent_tokenize(text)
stopwords = nltk.corpus.stopwords.words('english')

word_frequencies = {}
for word in nltk.word_tokenize(formatted_article_text):
    if word not in stopwords:
        if word not in word_frequencies.keys():
            word_frequencies[word] = 1
        else:
            word_frequencies[word] += 1


maximum_frequency = max(word_frequencies.values())

for word in word_frequencies.keys():
    word_frequencies[word] = (word_frequencies[word]/maximum_frequency)

#CALCULA LA FRASE QUE MAS SE REPITE
sentence_scores ={}
for sent in sentence_list:
    for word in nltk.word_tokenize(sent.lower()):
        if word in word_frequencies.keys():
            if len(sent.split(' ')) < 20:
                if sent not in  sentence_scores.keys():
                    sentence_scores[sent] = word_frequencies[word]
                else:
                    sentence_scores[sent] += word_frequencies[word]

#REALIZA EL RESUMEN CON LAS MEJORES FRASES
import heapq
summary_sentences = heapq.nlargest(7, sentence_scores, key=sentence_scores.get)

summary = ' '.join(summary_sentences)

summary = translator.translate(summary, dest='es').text
print(summary)
print("*********************************")