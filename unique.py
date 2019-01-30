from multiprocessing import Pool
import os
import fnmatch
import time
import sys
from collections import Counter
import  memory_profiler

a=time.time()
print("memory Before:: {}".format(memory_profiler.memory_usage()))

#counter is used to add up each dictionary from the chunks 
unique=Counter()
wc={}
chunks=[]
unwanted_chars = ".,-_$#@!%^&*()[]{}\/~`''?:;"

#making list of chunks
for file in os.listdir('.'):
     if fnmatch.fnmatch(file,'x*'):
          chunks.append(file)

def process(chunks):
	foo=open(chunks,encoding='iso-8859-1') 
	list_obj=foo.readlines()
	for line in list_obj:
		words=''.join(line).split()
		for raw_words in words:
			word=raw_words.strip(unwanted_chars)
			if word not in wc:
				wc[word]=0
			wc[word]+=1
	unique.update(wc) 
	print(unique)

#parallel processing using Pool
if __name__ == "__main__":
    p=Pool(4)
    results = p.map(process, chunks)
    print("finished")
   

b=time.time()
print("memory After:: {}".format(memory_profiler.memory_usage()))

print(b-a,"Seconds....!!")
