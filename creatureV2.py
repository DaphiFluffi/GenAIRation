# -*- coding: utf-8 -*-

#imports
from __future__ import division
import numpy as np
from numpy import random as rng
import copy
import logging

#create logger
logger = logging.getLogger("Creature")
logging.basicConfig(level=logging.DEBUG)

#settings
start = {"facing" : 0.0, "spread" : 90}	#in degree
goal = {"coord" : (800,200) , "size" : (20,20)}
length_zoom = 1	#float ( <0 will invert coords)
step_cap = 10	#in steps
LR_ratio = 0.5	#in [0;1]
outlier_rate = 0.005	#in [0;1]
rating_number = 1	#must be a valid number

########### COORDINATEN KLASSE ###########
class Coord(object):
	''' Koordinaten Umrechner '''
	
	def __init__(self, width=1280, height=720, zoom=1):
		''' setzt wichtige Daten fest '''
		
		self.width = width
		self.height = height
		self.zoom = zoom
	
	def sim2turt(self, x1, x2=None, **args):
		''' Umrechner von Simulation zu Turtle '''
		
		if args == {}:
			args = {"function" : "coordinates"}
		
		if args.has_key("function"):
			''' fügt der Umrechnung eine Bedeutung hinzu '''
			if args["function"] == "distance":
				''' umrechnen von Distanzen '''
				try:
					return distance(x1,x2)/self.zoom
				except:
					return distance(x1)/self.zoom
			
			elif args["function"] == "coordinates":
				''' umrechnen von Koordinaten '''
				try:	#falls x1 ein tupel
					return ((x1[0])/self.zoom-self.width/3,(x1[1]-goal["coord"][1]/2)/self.zoom)
				except:	#falls x1 = x
					return ((x1/self.zoom)-self.width/3,(x2-goal["coord"][1]/2)/self.zoom)
			else:
				raise NameError("modul 'function' has a wrong attribute!")
		else:
			raise NameError("wrong argument! Please use: 'function'")

########### RATING SAMMLUNG ##############
def ratingRegister(self,R):
	''' Register aller Ratings die zur Verfügung stehen '''
	
	def r_intensity():
		''' Kreatur wird nach Intensität bewertet '''
		
		if not self.stats["dead"]:
			''' wird nach jeder Bewegung ausgeführt '''
			self.career["score"] += 100 - (distance(self.stats["pos"], goal["coord"])/distance(goal["coord"])*100)
		
		elif self.stats["dead"]:
			''' wird nach dem Tod erstellt '''
			self.career["time_stamp"] = self.stats["step_counter"]
			
			logging.debug("	End-Ergebnis:	%i" %(self.career["score"]))
			
			return self.career["score"]
	
	def r_intensityV2():
		''' Kreatur wird nach Intensität bewertet und zusätzlich nach dem Tod gekürzt '''
		
		if not self.stats["dead"]:
			''' wird nach jeder Bewegung ausgeführt '''
			x = 100 - (distance(self.stats["pos"], goal["coord"])/distance(goal["coord"])*100)
			
			self.career["score"] += x
			
			if x > self.career["best"]:
				self.career["best"] = x
				self.career["time_stamp"] = self.stats["step_counter"]
		
		elif self.stats["dead"]:
			''' wird nach dem Tod erstellt '''
			logging.debug("	End-Ergebnis:	%i" %(self.career["score"]))
			
			return self.career["score"]
	
	#rating Zuweisung
	if R == 0:
		return r_intensity
	elif R == 1:
		return r_intensityV2
	else:
		logging.error("	Kein gültiges Rating wurde gewählt!")
		raise AttributeError()

########### KREATUREN KLASSE #############
class Creature(object):
	''' Kreaturen Hauptklasse '''
	
	def __init__(self, species=0, ancestor_way=[]):
		''' Kreatur wird erstellt '''
		
		#Spezienzuweisung
		if species == 0:
			self.traits = {"specie" : species , "tendency" : 66 , "arc" : (22.5,17.5) , "path_length" : 7 , "mutation_rate" : 2}
		elif species == 1:
			self.traits = {"specie" : species , "tendency" : 40 , "arc" : (42.5,27.5) , "path_length" : 6 , "mutation_rate" : 1}
		elif species == 2:
			self.traits = {"specie" : species , "tendency" : 86 , "arc" : (17.5,17.5) , "path_length" : 10 , "mutation_rate" : 4}
		elif species == 3:
			self.traits = {"specie" : species , "tendency" : 99 , "arc" : (30.0,10.0) , "path_length" : 5 , "mutation_rate" : 5}
		elif species == 4:
			self.traits = {"specie" : species , "tendency" : 66 , "arc" : (20.0,10.0) , "path_length" : 8 , "mutation_rate" : 4}
		elif species == 5:
			self.traits = {"specie" : species , "tendency" : 50 , "arc" : (25.0,0.0) , "path_length" : 8 , "mutation_rate" : 0}
		elif species == 6:
			self.traits = {"specie" : species , "tendency" : 10 , "arc" : (90.0,0.0) , "path_length" : 5 , "mutation_rate" : 7}
		elif species == 7:
			self.traits = {"specie" : species , "tendency" : 66 , "arc" : (45.0,10.0) , "path_length" : 10 , "mutation_rate" : 1}
		elif species == 8:
			self.traits = {"specie" : species , "tendency" : 75 , "arc" : (22.5,17.5) , "path_length" : 6 , "mutation_rate" : 3}
		elif species == 9:
			self.traits = {"specie" : species , "tendency" : 81 , "arc" : (35.0,12.5) , "path_length" : 10 , "mutation_rate" : 2}
		elif species == 10:
			self.traits = {"specie" : species , "tendency" : 100 , "arc" : (90.0,0.0) , "path_length" : 20 , "mutation_rate" : 0}
		else:
			self.traits = {"specie" : species , "tendency" : 66 , "arc" : (20.0,0.0) , "path_length" : 8 , "mutation_rate" : 5}
		
		#erste Generation startet innerhalb eines parametisierten Winkels
		if ancestor_way == [] and start["spread"] != 0:
			ancestor_way = [rng.randint(start["spread"])-start["spread"]/2]
		
		#Attributzuweisung
		self.briefing = []
		self.ancestor_way = ancestor_way
		self.rating = ratingRegister(self,rating_number)
		self.stats = {"pos" : (0.0,0.0) , "viewpoint" : start["facing"] , "step_counter" : 0 , "dead" : False , "success" : False}
		self.career = {"best" : 0.0 , "time_stamp" : 0 , "score" : 0}
	
	def appendWay(self):
		''' briefing wird erweitert '''
		
		#checken ob Input von Eltern oder nicht
		if self.stats["step_counter"] < len(self.ancestor_way) and rng.random() >= outlier_rate:	#Input wird mit parametesierter Wahrscheinlichkeit ignoriert
			r = self.ancestor_way[self.stats["step_counter"]]
			
			# MUTATION VON R
			#r begrenzen
			if r < (self.traits["arc"][0]+self.traits["arc"][1])*-2:
				r += rng.random()*self.traits["mutation_rate"]
			elif r > (self.traits["arc"][0]+self.traits["arc"][1])*2:
				r -= rng.random()*self.traits["mutation_rate"]
			
			#ansonsten Mutation freien Lauf lassen
			elif rng.random() < LR_ratio:
				r += rng.random()*self.traits["mutation_rate"]
			else:
				r -= rng.random()*self.traits["mutation_rate"]
			
			self.briefing.append(r)
		
		#ohne Input nach Eigenschaften gehen
		else:
			if rng.random()*100 > self.traits["tendency"]:
				self.briefing.append(0)
			elif rng.random() < LR_ratio:
				self.briefing.append(rng.randint(self.traits["arc"][0]-self.traits["arc"][1],
													self.traits["arc"][0]+self.traits["arc"][1]+1))
			else:
				self.briefing.append(-(rng.randint(self.traits["arc"][0]-self.traits["arc"][1],
													self.traits["arc"][0]+self.traits["arc"][1]+1)))
	
	def nextStep(self, r):
		''' bewegt die Kreatur einen Schritt '''
		
		if self.stats["dead"]:
			''' Kreatur bereits gestorben -> Bewegung gestoppt '''
			return
		
		self.stats["viewpoint"] += r
		
		#auf dem kreis bleiben:
		if self.stats["viewpoint"] > 359:
			self.stats["viewpoint"] -= 360
		elif self.stats["viewpoint"] < 0:
			self.stats["viewpoint"] += 360
		
		#eigentliche Bewegung im Koordinatensystem
		self.stats["pos"] = (self.stats["pos"][0] + length_zoom*(self.traits["path_length"]) * np.cos(self.stats["viewpoint"]/180*np.pi),
								self.stats["pos"][1] + length_zoom*(self.traits["path_length"]) * np.sin(self.stats["viewpoint"]/180*np.pi))
		
		self.stats["step_counter"] += 1
		self.checkEnd()
		
		#Ab hier wird sich das Rating ausgesucht
		self.rating()
	
	def movement(self):
		''' Kreatur bewegt sich vollständig bis zum Ende '''
		
		self.appendWay() #erster Bewegungsbefehl
		
		#eigentliche Bewegung
		for e in self.briefing:
			self.nextStep(e)
			if self.stats["step_counter"] < step_cap and not self.stats["dead"]:
				self.appendWay()
		
		self.stats["dead"] = True
		self.rating()
		
		logging.debug("	Kreatur endete auf:	%i ,	%i" %(self.stats["pos"][0],self.stats["pos"][1]))
	
	def checkEnd(self):
		''' Ende der Kreatur wird überprüft '''
		
		if self.stats["pos"][0] > goal["coord"][0]-goal["size"][0] and self.stats["pos"][0] < goal["coord"][0]+goal["size"][0] and self.stats["pos"][1] > goal["coord"][1]-goal["size"][1] and self.stats["pos"][1] < goal["coord"][1]+goal["size"][1]:
			''' Kreatur erreicht Ziel '''
			logging.info("	Kreatur hat Ziel erreicht!")
			self.stats["dead"] = True
			self.stats["success"] = True
	
	def legacy(self):
		''' Vererbung für die nächste Generation wird vorbereitet '''
		
		return self.briefing[0:self.career["time_stamp"]]

########### WEITERE FUNKTIONEN ###########
def procreation(ancestor):
	''' Zeugt eine neue Kreatur, die von der übergebenen erbt '''
	
	return Creature(species = ancestor.traits["specie"], ancestor_way = copy.deepcopy(ancestor.legacy()))

def distance(pos1, pos2=(0,0)):
	''' berechnet die Distanz zwischen zwei Punkten (bzw. zum Ursprung) '''
	
	return np.linalg.norm(np.array(pos1) - np.array(pos2))

def angle(pos1, pos2=(0,0)):
	''' berechnet den Winkel zwischen zwei Punkten (bzw. zum Ursprung) zur x-Achse '''
	
	array = np.array(pos1) - np.array(pos2)
	return np.degrees(np.arctan2(array[1],array[0]))

########### SONSTIGES ZEUG ###############
if __name__ == "__main__":
	c = Creature()
	c.movement()
	print c.briefing
