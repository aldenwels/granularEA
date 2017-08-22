from scipy.spatial import distance
import numpy as np
from grain import Grain
import random
from pythonosc import osc_message_builder
from pythonosc import udp_client
from pythonosc import dispatcher as dispatch
from pythonosc import osc_server
import argparse






selectionMinMax = np.array([248040.5,273266.0])
speedMinMax = np.array([0.0,100.0])
lengthMinMax = np.array([0.0,1000.0])
ampMinMax = np.array([0.0,1.0])
highestPossibleScore = (selectionMinMax[1]-selectionMinMax[0]) + speedMinMax[1] + lengthMinMax[1] + 1.0

population = []
populationLimit = 4
target = Grain(np.array([268040.5,269533.5]),np.array([12.0,62.0]),
  np.array([500.,600.]),np.array([.58,.94]))


def getBestInPopulation(unused_addr,*args):
  global population
  if(len(population) == 0):
    generateParents()
  else:
    for i in range(0,len(population)):
      twoDimensionalFitness(population[i])
    population.sort(key=lambda x: x.fitness)

    reproduce(population[0],population[1])

  remove()
  print(len(population))
  for i in range(0,len(population)):
    print(population[i].fitness)
  messages = []
  client = udp_client.UDPClient("127.0.0.1", 5005)
  dispatcher = dispatch.Dispatcher()
  hold = "" 
  for i in range(len(population[0].mat)):
    hold += str(population[0].mat[i][0]) + " " + str(population[0].mat[i][1]) + " "

  message = osc_message_builder.OscMessageBuilder(address = "/population")
  message.add_arg(hold)
  message = message.build()
  client.send(message)


def twoDimensionalFitness(p2):
  fitnessSum = 0
  for i in range(0,4):
    d = (target.mat[i]-p2.mat[i])**2
    d = d.sum(axis=-1)
    d = np.sqrt(d)
    print('fitness for a,b')
    print('a')
    print(target.mat[i])
    print('b')
    print(p2.mat[i])
    print('score')
    print(d)
    fitnessSum += d
  p2.fitness = fitnessSum

def generateParents():
  global population
  for i in range(2):
    selx = random.uniform(selectionMinMax[0],selectionMinMax[1])
    sely = random.uniform(selx,selectionMinMax[1])
    speedx = random.uniform(speedMinMax[0],speedMinMax[1])
    speedy = random.uniform(speedx,speedMinMax[1])
    lengthx = random.uniform(lengthMinMax[0],lengthMinMax[1])
    lengthy = random.uniform(lengthx,lengthMinMax[1])
    ampx = random.uniform(ampMinMax[0],ampMinMax[1])
    ampy = random.uniform(ampx,ampMinMax[1])
    hold = Grain(np.array([selx,sely]),np.array([speedx,speedy]),np.array([lengthx,lengthy]),
           np.array([ampx,ampy]))
    print(hold)
    population.append(hold)


def reproduce(p1,p2):
  children = crossover(p1,p2)
  mutate(children)


def crossover(p1,p2):
  childa = Grain(p1.selection,p1.speed,p2.length,p2.amp)
  childb = Grain(p2.selection,p2.speed,p1.length,p1.amp)
  return [childa,childb]

def mutate(children):
  for i in range(0,2):
    g = random.randint(0, 3)
    if(g == 0):
      selx = random.uniform(selectionMinMax[0],selectionMinMax[1])
      sely = random.uniform(selx,selectionMinMax[1])
      children[i].selection = np.array([selx,sely])
    elif(g == 1):
      speedx = random.uniform(speedMinMax[0],speedMinMax[1])
      speedy = random.uniform(speedx,speedMinMax[1])
      children[i].speed = np.array([speedx,speedy])
    elif(g == 2):
      lengthx = random.uniform(lengthMinMax[0],lengthMinMax[1])
      lengthy = random.uniform(lengthx,lengthMinMax[1])
      children[i].length = np.array([lengthx,lengthy])
    elif(g == 3):
      ampx = random.uniform(ampMinMax[0],ampMinMax[1])
      ampy = random.uniform(ampx,ampMinMax[1])
      children[i].amp = np.array([ampx,ampy])

    population.append(children[i])

def remove():
  global population
  if(len(population) > populationLimit):
    population = population[:50]

def main():
  
  #client
  dispatcher = dispatch.Dispatcher()


    #set up server to listen for udp commands
  parser = argparse.ArgumentParser()
  parser.add_argument("--initial",default="random", help="Initial state")
  parser.add_argument("--ip",
  default="127.0.0.1", help="The ip to listen on")
  parser.add_argument("--port",
  type=int, default=5006, help="The port to listen on")
  args = parser.parse_args()
  #generate new states on end of counter
  server = osc_server.ThreadingOSCUDPServer(
  (args.ip, args.port), dispatcher)
  print("Serving on {}".format(server.server_address))
  dispatcher.map("/getPopulation",getBestInPopulation)
  server.serve_forever()
  '''
  print(target.mat)
  generateParents()
  reproduce(population[0],population[1])
  


  while(len(population) < 50):
    for i in range(0,len(population)):
      twoDimensionalFitness(population[i])
    population.sort(key=lambda x: x.fitness)
    print('using this is a parent 0')
    print(population[0].fitness)
    reproduce(population[0],population[1])
    remove()

  "population.sort(key=lambda x: x.fitness)"
  print('highest fitness')
  print(population[0].fitness)

  for i in range(0,len(population)):
    fitness = population[i].fitness
    print(fitness)
    print('index ')
    print(i)
    print("{:.1%}".format(fitness/highestPossibleScore))

  print(target.mat)
  print(population[0].mat)
  print(population[0].fitness)
  
  '''



if __name__ == "__main__":
    main()