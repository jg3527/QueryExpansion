E6111 Advanced Database Systems - Project 1

Team Member
**********************

	Jing Guo(jg3527)
	Zixuan Lu(zl2348)
	
Files 
**********************

	README 
	project1.py
	InformationRetrival.py
	transcript_musk
	transcript_gates
	transcript_columbia
	
How To Run The Program
**********************

	To run the program, just enter the directory of our files and enter the following commands in terminal:

 	python project1.py <bing account key> <precision> <query>
	
	Desired precision and query can be changed to any value you want.
	For example:
	python project1.py w7Hv5UCrrHE3bZysRWRvuBCbibeduPuGJSfKqM1rc7Y 0.9 gates



Internal Design
**********************

	Input: Bing Account key, query, desired precision(value between 0 and 1)
	       For each iteration: user's judge for each returned result.
	
	Function Design:
		1.project.py : drive file, get user's input and initialize the InformationRetrival class and call it's infoQuery() function.
		2.InformationRetrival.py: 
			define a class named "InformationRetrival" :
			consists of following functions:
			__init__() : constructor
			infoQuery(): main flow control function
			bingTest(): gather the results from Bing API
			resultParsing(): parse Json into document dictionary
			display(): present the results to users and get feedback
			normalize(): implement vector normalization
			update(): update query
			clearStopWords(): delete stop words from modified query vectors
			computeQm(): compute modified query vectors
			
Query-modification Method
**********************

	To solve this problem, we use Rocchio's algorithm combined with vector space model.
	1. Store the returned results as document dictionary and the key is the Url.
	2. Compute tf-idf = tf * idf as weight for each terms in each document.
	3. With the feedback from users, we record the number of relevant documents as Dr.
	4. We compute modified query vector using the following equation which is derived from the underlying theory of Rocchio's algorithm:
	   Qm =  q = beta * sum(DrV) / Dr - gamma * sum(DnrV) / Dnr
	   In the upon equation, DrV is the relevant document vectors, DnrV is non-relevant document vectors, Dr is the number of relevant documents and Dnr is the number of non-relevant documents.
	5. Delete the previous query words and the stop words from Qm before sort Qm in decreasing order according to the weight we compute from step 5.
	6. If the weight difference of the first two words with the highest weight is small, we append both words to the query, otherwise only append the first word. 

Bing Search Account Key
**********************
	w7Hv5UCrrHE3bZysRWRvuBCbibeduPuGJSfKqM1rc7Y

Reference
**********************
	1. http://blog.csdn.net/chenfei_5201213/article/details/9094989
	2. http://learn.adicu.com/python/#dictionaries
	
			
			
			
