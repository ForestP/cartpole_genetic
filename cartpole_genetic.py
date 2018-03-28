# This is my first project with open ai gym to teach an ai cartpole with a genetic algorithm

# create environment
import gym
import random
import numpy as np
from statistics import mean, median
from collections import Counter
import operator
from operator import itemgetter


env = gym.make('CartPole-v0')
env.reset() # This gets us the image

populationSize = 1000
goalSteps = 200 # number of stpes or actions to take
bestSample = 450
luckyRandom = 50
currentGen = 0

def generateFirstPopulation():
	population = []
	# generate population
	for _ in range(populationSize):
		score = 0
		actions = []
		# generate 1 run
		for i in range(goalSteps):
			action = env.action_space.sample() # do a random action
			observation, reward, done, info = env.step(action)
			
			score += reward # saving score
			actions.append(action)
			# done at 200 steps, leaving view, or too much tilt
			if done:
				break

		# save run to population with its score and actions
		population.append([score, actions])
		env.reset()

	return sorted(population, key=itemgetter(0), reverse=True)

def scoreNewGeneration(population):
	scoredPopulation = []
	for individualActions in population:
		score = 0
		for action in individualActions:
			observation, reward, done, info = env.step(action)

			score += reward
			if done:
				break
		scoredPopulation.append([score, individualActions])
		env.reset()

	return sorted(scoredPopulation, key=itemgetter(0), reverse=True)

def selectFromPopulation(sortedPop):
	nextGeneration = []
	for i in range(bestSample):
		nextGeneration.append(sortedPop[i][1]) # gives its actions to new generation

	for i in range(luckyRandom):
		nextGeneration.append(random.choice(sortedPop)[1]) # gives actions of randomly selected

	random.shuffle(nextGeneration)
	return nextGeneration

# DEPRECIATED FUNCTION FOR CREATING A CHILD #

def createChild(actions1,actions2):
	childActions = []

	for i in range(200):
		# cut off last 3 actions because thats when they failed
		if i < (len(actions1) - 3):
			childActions.append(actions1[i])
		elif i > (len(actions2) - 3) :
			childActions.append(random.randint(0,1)) # weve used all of breeder 1 and 2 actions
		else:
			childActions.append(actions2[i])
	return childActions

def createChildren(breeders):
	newPopulation = []
	for i in range(len(breeders)//2):
		# each pair of breeders make 2 children
		for j in range(2): 
			newPopulation.append(createChild(breeders[i], breeders[len(breeders)-1-i]))
	return newPopulation

def mutateActions(individual):
	actionToMutate = int(random.random() * len(individual))
	# if (actionToMutate == 0):
	# 	individual[] = int(random.randint(0,1) + individual[1:])
	# else:
	# 	individual = individual[:actionToMutate] + random.randint(0,1) + individual[actionToMutate+1:]
	individual[actionToMutate] = random.randint(0,1)
	return individual

def mutatePopulation(population, chanceOfMutation):
	for i in range(len(population)):
		if random.random() * 100 < chanceOfMutation:
			population[i] = mutateActions(population[i])
	return population

def runGeneticAlgorithm(evolutions):
	currentScoredGeneration = []
	currentGen = []
	initialPop = generateFirstPopulation()
	for i in range(0, evolutions):
		if i == 0:
			currentScoredGeneration = initialPop
		else:
			currentScoredGeneration = scoreNewGeneration(currentGen)

		print("Mean: ", calculateMeanScore(currentScoredGeneration)) # prints out the mean score of the current gen
		print("Num beat goal: ", calculateNumOverGoal(currentScoredGeneration))
		# generation scored, create a new one
		# select the best and a few randoms from current gen
		selectedBreeders = selectFromPopulation(currentScoredGeneration)
		unmutatedGen = createChildren(selectedBreeders)
		currentGen = mutatePopulation(unmutatedGen, 5)

		
def calculateMeanScore(population):
	sums = 0
	for individual in population:
		sums += individual[0]
	avg = sums / len(population)
	return avg

def calculateNumOverGoal(population):
	count = 0
	for individual in population:
		if individual[0] > 100:
			print(individual[0])
			count += 1
	return count

runGeneticAlgorithm(100)


