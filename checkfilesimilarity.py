import spacy
import os
import sys
from gensim.summarization.summarizer import summarize

doc1_file = sys.argv[1]
dir_path = sys.argv[2]
doc2_file = None

if len(sys.argv) != 3:
    print("Insufficient arguments")
    sys.exit()

print('doc1_file : '+doc1_file)
print('dir_path : '+dir_path)

# list to store files
similarity = 0
max_len = 1000000
doc1 = None
doc2 = None
nlp = spacy.load("en_core_web_lg")

with open(doc1_file,'r') as f:
    contents = f.read()
    doc1 = nlp(summarize(contents))
    if len(contents) < max_len:
        max_len = len(contents)

# Iterate directory
for root, dirs, files in os.walk(dir_path):
    for filename in files:
        if len(filename) <= 8:
            path = os.path.join(root, filename)
            #print("path = "+path)
            with open(path,'r') as f:
                #ValueError: [E088] Text of length 1650801 exceeds maximum of 1000000. The parser and NER models require roughly 1GB of temporary memory per 100,000 characters in the input. This means long texts may cause memory allocati
on errors. If you're not using the parser or NER, it's probably safe to increase the `nlp.max_length` limit. The limit is in number of characters, so you can check whether your inputs are too long by checking `len:wq(text)`.
                contents = f.read()
                doc2 = nlp(summarize(contents))
                similarity_tmp = doc1.similarity(doc2)
                if similarity_tmp > 0:
                    print(str(similarity_tmp)+':'+path)
                if similarity_tmp > similarity:
                    similarity = similarity_tmp
                    doc2_file = path

print('File '+doc2_file+' is most similar('+str(similarity)+') to file '+doc1_file+'.');
