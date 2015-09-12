#!/usr/bin/python
# -*- coding: utf-8 -*-
#coding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import re
from collections import Counter
import urllib2
import base64
import json
import math


class InformationRetrival:
    
    def __init__(self, accountKey, precision, query):
        self.accountKey = accountKey  # Bing acount key
        self.query = query.split()    # User's query
        self.precision = precision    # Desired precision
        
        self.alpha = 1     # Parameter, unused
        self.beta = 1      # Coefficient
        self.gamma = 1     # Coefficient
         
        self.currPrecison = 0   # Precision for each round
        self.results = []       # Returned result from Bing
        self.docs = {}          # Top 10 documents
        self.df = Counter()     # {word : document frequency}
        self.iteration = 1      # Number of iteration
        self.stop=0             # Judge the continuation of search

        self.stopList = ["i","me","my","myself","we","us","our","ours","ourselves","you","your","yours",
                "yourself","yourselves","he","him","his","himself","she","her","hers","herself","it","its",
                "itself","they","them","their","theirs","themselves","what","which","who","whom","whose",
                "this","that","these","those","am","is","are","was","were","be","been","being","have","has",
                "had","having","do","does","did","doing","will","would","should","can","could","ought",
                "i'm","you're","he's","she's","it's","we're","they're","i've","you've","we've","they've",
                "i'd","you'd","he'd","she'd","we'd","they'd","i'll","you'll","he'll","she'll","we'll","they'll",
                "isn't","aren't","wasn't","weren't","hasn't","haven't","hadn't","doesn't","don't","didn't",
                "won't","wouldn't","shan't","shouldn't","can't","cannot","couldn't","mustn't","let's","that's",
                "who's","what's","here's","there's","when's","where's","why's","how's","a","an","the","and",
                "but","if","or","because","as","until","while","of","at","by","for","with","about","against",
                "between","into","through","during","before","after","above","below","to","from","up","upon",
                "down","in","out","on","off","over","under","again","further","then","once","here","there",
                "when","where","why","how","all","any","both","each","few","more","most","other","some",
                "such","no","nor","not","only","own","same","so","than","too","very","say","says","said",
                "shall","a","s","ve","lets","days","ago","retrieved"]
    
    #Main flow control function
    def infoQuery(self):       
        self.bingTest()       
        self.resultParsing()
        self.display()
    
    #Get result from Bing  
    def bingTest(self):
        bingUrl = 'https://api.datamarket.azure.com/Bing/Search/Web?Query=%27'+'+'.join(self.query)+'%27&$top=10&$format=json'
        #Provide your account key here
        accountKey = 'w7Hv5UCrrHE3bZysRWRvuBCbibeduPuGJSfKqM1rc7Y'

        accountKeyEnc = base64.b64encode(accountKey + ':' + accountKey)
        headers = {'Authorization': 'Basic ' + accountKeyEnc}
        req = urllib2.Request(bingUrl, headers = headers)
        response = urllib2.urlopen(req)
 	#content = response.read()
        contents = response.read()
	content = contents.encode('ascii','ignore')
        temp = json.loads(content)
        self.results = temp['d']['results']
        
    #Parse JSON into self.docs(dictionary)
    def resultParsing(self):
        if len(self.results) < 10:
            print "Sorry, the number of returned results is less than 10, please try another one."
            exit(1)
            
        for result in self.results:
            ID = result["Url"]
            if ID not in self.docs:
                content = result["Title"].lower() + " " + result["Description"].lower()
                self.docs[ID] = {"Content" : content, "Vector" : {}, "TermFrequency" : {}, "Relevant" : 0}
                words =  content.split(" ")
                for i in range(len(words)):
		#delete characters that are non-digit or letters
                    words[i] = re.sub("^[^a-z0-9]+", "", words[i])
                    words[i] = re.sub("[^a-z0-9]+$", "", words[i])
                count = Counter(words)
                if "" in count:
                    del count[""]
                self.docs[ID]["TermFrequency"] = count
                self.df += Counter(set(count))
                
    #Present results to user and get feedback
    def display(self):
        n = 1;
        rel = 0
        for result in self.results:
            print "Result " + str(n) 
            n += 1
            print "["
            print "Title:  " + result["Title"] 
            print "Url: " + result["Url"]
            print "Description: " + result["Description"]
            print "]"
            
            while True:
                r = raw_input("Relevant ?(Y/N)").lower()
                ID = result["Url"]
                if r == "y":
                    self.docs[ID]["Relevant"] = 1
                    rel += 1
                elif r == "n":
                    self.docs[ID]["Relevant"] = 0
                else:
                    print "Please Enter Y or N !"
                    continue
                break
            print "==========================================="
            print
            self.currPrecison = float(rel) / 10
        print "FEEDBABK SUMMARY" + "("+str(self.iteration) + " Times Iteration)"
        print "Query: " + str(self.query)
        print "Current precision: " + str(self.currPrecison)

        if self.currPrecison == 0:
            self.stop = 1
            print "No relevant documents!"
            return       
        elif self.currPrecison > self.precision:
            self.stop = 1
            print "Desired Precision Reached, Done!"
            return
        else:
            self.iteration += 1
                
    
    #Vector normalization
    def normalize(self, vec):
        summ = 0
        for item in vec:
            summ += item * item
        norm = math.sqrt(summ)
        i = 0
        for item in vec:
            vec[i] = item / norm
            i += 1
        
        
    #Update query       
    def update(self):
        Dr = 0 # Number of relevant documents
        for doc in self.docs.values():
            Dr += doc["Relevant"]
        #print "Debug: "+ str(Dr) 
        self.computeDocVec()
        #print "Debug: " + str(doc['Vector'].values())
        Qm = self.computeQm(Dr)
        
        for word in self.query:
            if word in Qm:
                del Qm[word]
        self.clearStopWords(Qm)
        sortedResult = sorted(Qm.items(), key = lambda x : x[1],reverse = True)
        #print "Sorted Result: "+ str(sortedResult)
        self.query.append(sortedResult[0][0])
        if(sortedResult[1][1] != 0 and sortedResult[0][1] / sortedResult[1][1] < 2):
            self.query.append(sortedResult[1][0])       
        print  "New Query: " + str(self.query)
    
    #Delete stop words from Qm
    def clearStopWords(self,Qm):
        for word in self.stopList:
            if word in Qm:
                del Qm[word]
                
    #Compute document vector        
    def computeDocVec(self):
        for doc in self.docs.values():
            for word in doc['TermFrequency'].keys():
                doc['Vector'][word]=doc['TermFrequency'][word] + math.log(len(self.docs)/self.df[word])
            self.normalize(doc['Vector'].values()) 
    
    #Compute Qm
    def computeQm(self,Dr):
        Qm = {}
        for word in self.df.keys():
            Qm[word] = 0
            for doc in self.docs.values():
                if word in doc["TermFrequency"].keys():
                    #print "Debug: "+ word
                    Qm[word] += doc["Relevant"] * doc["Vector"][word] * self.beta / Dr
                    #print "Debug: "+ str(Qm)
                    Qm[word] -= (1 - doc["Relevant"]) * doc["Vector"][word] * self.gamma / (len(self.docs) - Dr)
        return Qm
        #print "Debug2: "+ str(Qm)
