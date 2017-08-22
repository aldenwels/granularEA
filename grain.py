import numpy as np

class Grain:
  def __init__(self, sel, spd,l,amp):
    self.selection = sel
    self.speed = spd
    self.length = l
    self.amp = amp
    self.mat = [self.selection,self.speed,self.length,self.amp]
    self.fitness = 0.0
