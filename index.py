import os
import fnmatch
import time
import  memory_profiler
from multiprocessing import Pool


file_list=[]
for file in os.listdir('.'):
	file_list.append(file)


pattern=input("Enter search Pattern ::>> ")
set_of_output=[]

print("\nmemory Before:: {}".format(memory_profiler.memory_usage()))
a=time.time()

for fopen in file_list:
	f=open(fopen,encoding="iso-8859-1")
	line=f.readlines()
	
	for word in line:
		if pattern in word:
			set_of_output.append(fopen)
			break			



b=time.time()
print("\nmemory After:: {}".format(memory_profiler.memory_usage()))
output=set(set_of_output)
number=len(output)
print(number,"File(s) containing search pattern ::> ",output)
print("Time taken to search in seconds: ",b-a)
