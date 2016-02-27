from threading import Thread
import math


numberOfThreadsToSpawn = 2
globalListOfResultsFromAllThreads = ['']*numberOfThreadsToSpawn

#the first position of argumentsList is the place to put your outcome
def functionToThread(argumentsList):

	if( len(argumentsList) > 0 ):

		if( argumentsList[0] < len(globalListOfResultsFromAllThreads) ):
			globalListOfResultsFromAllThreads[ argumentsList[0] ] = argumentsList[0]



#position begins at 0, n jobs, k workers
def getTasksListOfLists(n, k):

	listOfListOfindices = []
	if( n>0 and k>0 ):

		total = 0
		tasks = []

		for i in range(0, k):
			task = int(math.floor((n+i)/k))
			total = total + task
			tasks.append(task)

		cursor = -1;
		
		for i in range(0, len(tasks)):
			indices = []

			for j in range(0, tasks[i]) :
				cursor = cursor + 1
				indices.append(cursor)

			listOfListOfindices.append(indices)

	return listOfListOfindices

#spawns numberOfThreadsToSpawn targetFunction threads passing each argumentsListOfList argument 
def spawnXThread(numberOfThreadsToSpawn, targetFunction, argumentsListOfList):

	if( numberOfThreadsToSpawn > 0 and len(targetFunction) > 0 and numberOfThreadsToSpawn == len(argumentsListOfList) ):

		threads = []

		for i in range(0, numberOfThreadsToSpawn):
			
			threads.append(Thread(target=eval(targetFunction)(argumentsListOfList[i]) ))

		for t in threads :
			t.start()

		# Wait for all threads to complete
		for t in threads:
			t.join()


argumentsListOfList = []
list1 = []
list2 = []

list1.append(0)
list1.append('hello')
list1.append(1)

list2.append(1)

argumentsListOfList.append(list1)
argumentsListOfList.append(list2)

#spawnXThread('functionToThread', argumentsListOfList)
#print globalListOfResultsFromAllThreads

#e.g 10 mementos jobs, 3 worker threads
print getTasksListOfLists(10, 3)