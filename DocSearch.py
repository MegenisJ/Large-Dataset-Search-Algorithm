#### c1729929 #### time on set 3 30.0seconds on my device 
import numpy as np 
import math
from timeit import default_timer as timer

#Generates a dictionary of words along with an inverted index for each of them.
#uniqueWords is the dictionary with the inverted index stored as the value for the word reference in the dictionary.
def fillDictionary(uniqueWords):
	DocumentID = 0 #Document ID is essentially a line counter
	with open("docs.txt","r") as f:
		for line in f: #reads each line of the file 
			DocumentID += 1 #incriments the document counter
			for word in line.split(): #takes each word from the line
				WordFriequency = line.split().count(word) #Checks the friequency of each word in the line 
				if word not in uniqueWords:#If no value has been generated 
					uniqueWords[word] = {} #assigns it to an empty dictionary
				uniqueWords[word].update({DocumentID:WordFriequency}) #Updates inverted index for word 
	print("Words in dictionary: " + str(len(uniqueWords)))
	return uniqueWords
	
def Query(uniqueWords):
	#keys = uniqueWords.keys()
	keys = list(uniqueWords) #Generates a list of all the words in order in list form so it can be used as a reference
	with open("queries.txt","r") as f: 
		for line in f: # means the entire functions code repeats for each query
			#Generating / Clearing values as this code is repeated over multiple lines of a file  
			queryWordsList = []
			keyslist = []
			Match = []
			Angles = {}
			for word in line.split(): #splits the query into indevidual words and itterates through them 
				if word in uniqueWords: #check if the word is in docs.txt
					queryWordsList.append(word) #if it is add to list of words that are to be used as search te									rms 

			#Printing out the query in correct form
			QueryString = ""
			for i in queryWordsList:
				QueryString += i + " "
			print("Query: " + QueryString)

			keyslist = generateKeyslist(uniqueWords,keyslist,queryWordsList)#generates a list of docuements for every search term 
			Match = generateMatchingDocuments(Match,keyslist)	#Checks which documents are in every search term and creates a list of all documents in all
			QueryVector = generateQueryVector(uniqueWords,keys,queryWordsList)#Generates a vector list based on the query
			
			#output the matching documents in correct form 
			matchesoutputstr = ""
			for i in Match:
				matchesoutputstr += str(i) + " "
			print("Relevant Documents: " + matchesoutputstr) 
			
			print("Generating Document Order...")
			
			DocumentVector = [0] * len(uniqueWords)#generate empty vector values 
			#for x, i in itertools.product(Match,keys):#( woukd appreciate feedback on why this was slower than nested for loops )
			for x in Match:
				for i in keys:
					if x  in uniqueWords[i].keys():#check if document contains the word
						DocumentVector[keys.index(i)] = uniqueWords[i][x] #if it does change the value in the vector to
																		  #the value from the inverted index
				Angles[x] = CalcAngle(DocumentVector,QueryVector)	
				DocumentVector = [0] * len(uniqueWords)#clears values in DocVector for next document
			for w in sorted(Angles, key=Angles.get, reverse=False):
  				print (str(w) + " " +  str(Angles[w]))
			print("")#Just prints a blank line at the end of each search for better layout
def generateKeyslist(uniqueWords,keyslist, queryWordsList):
	
	for i in range(len(queryWordsList)): 
		keyslist.append(uniqueWords[queryWordsList[i]].keys())	
	return keyslist	

def generateMatchingDocuments(Match,keyslist):		
 
	inAllDocuments = True
	for x in keyslist[0]:  
		inAllDocuments = True
		for i in range(len(keyslist)):
			if x not in keyslist[i]:
				inAllDocuments = False
		if inAllDocuments == True:
			Match.append(x) #Match is a list of all the documents that math the search terms 
	return(Match)

def generateQueryVector(uniqueWords,keys,queryWordsList):
	QueryVector = [0] * len(uniqueWords)
	for x in queryWordsList:  #For every search word assigns that value to 1 
		QueryVector[keys.index(x)] = 1
		#norrm_y = np.lanalg.norm(QueryList)
	return(QueryVector)

def CalcAngle(x,y):
	norm_x = np.linalg.norm(x)
	norrm_y = np.linalg.norm(y)
	cos_theta = np.dot(x,y) / (norm_x * norrm_y)
	theta = math.degrees(math.acos(cos_theta))
	#np.around(theta,2)
	return (theta)

def Main():
	uniqueWords = {}
	uniqueWords = fillDictionary(uniqueWords)
	Query(uniqueWords)

start = timer()
Main()
end  =timer() 
print("Time : " + str(end - start))

