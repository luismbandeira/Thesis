from __future__ import division
from codecs import open
import sys, random
import csv
from math import sqrt, ceil
from pickle import *
import time

#Defines every charge
class charge(object):
	def __init__(self,x,y,q):
		self.x = x
		self.y = y
		self.q = q

	def getx(self):
		#print self.x
		return self.x

#Defines relations beetween charges
class relations(object):
		def __init__(self, first, second, path, distance, cost):
			self.first = first
			self.second = second
			self.path = path
			self.distance = distance
			self.cost = cost

#Defines every sector or district
class sector(object):
	def __init__(self,i):
		self.i = i

"""
def get_cities_coords(num_cities, xmax=15, ymax=15, qmax=15):
	#Calculate random position of a capacitated point (x,y - coord, q - demand)
	coords = []
	for i in range(num_cities):
		x = random.randint(1, xmax)
		y = random.randint(1, ymax)
		q = random.randint(1, qmax)
		#t = random.randint(0, num_cities)
		#print x
		coords.append( (float(x), float(y), float(q)))
		#print coords
	return coords


def get_attraction_matrix(coords):
	matrix = [[0 for x in range(len(coords))] for y in range(len(coords))]
	fmax = 0;
	dist= 0;
	global x1_max, y1_max, q1_max, x2_max, y2_max, q2_max, q_max, i_max, j_max
	for i, (x1, y1, q1) in enumerate(coords):
		for j, (x2, y2, q2) in enumerate(coords):
			dx = x1 - x2
			dy = y1 - y2
			q = q1 * q2
			dist = sqrt(dx*dx + dy*dy)
			#print dist
			#to prevent the calculation of coulomb's force between one point and itself
			if dist == 0:
				matrix[i][j] = 0
			else:
				F = q /(dist * dist)
				if F > fmax:
					x1_max = x1
					y1_max = y1
					q1_max = q1
					x2_max = x2
					y2_max = y2
					q2_max = q2
					i_max = i
					j_max = j
					matrix[i][j] = F
				else:
					matrix[i][j] = F
	return matrix
"""

def get_attraction(x1, x2):
	if(x1.x==x2.x & x1.y==x2.y):
		return 0
	else:
    		return (x1.q*x2.q/(pow(x1.x-x2.x,2)+pow(x1.y-x2.y,2)))

#calculate the attraction matrix between points
def get_attraction_max(coords):
	max=0;
	for i in enumerate(coords):
		for j  in enumerate(coords):
			attr = get_attraction(i, j)
			if (max<attr):
				max = attr
	return attr

"""
def get_attraction_matrix(coords):
	matrix = [[0 for x in range(len(coords))] for y in range(len(coords))]
	for i in range(0,len(coords)):
		for j in range(0,len(coords)):
			matrix[i][j] = get_attraction(coords[i], coords[j])
	return attr
"""
#calculate the attraction matrix between points
def get_attraction_matrix(coords):
	matrix = [[0 for x in range(len(coords))] for y in range(len(coords))]
	fmax = 0;
	dist= 0;
	# Returns the average euclidian distance beetween points
	average = average_euclidian(coords)
	# Returns the euclidian's distance standard deviation
	deviation = standard_deviation(coords)
	global x1_max, y1_max, q1_max, x2_max, y2_max, q2_max, q_max
	for i, (x1, y1, q1) in enumerate(coords):
		for j, (x2, y2, q2) in enumerate(coords):
			dx = coords[i][0] - coords[j][0]
			dy = coords[i][1] - coords[j][1]
			q = coords[i][2] * coords[j][2]
			dist = sqrt(dx*dx + dy*dy)
			#print dist
			#to prevent the calculation of coulomb's force between one point and itself
			if dist == 0:
				matrix[i][j] = 0
			else:
				F = q /(dist * dist)
				if F > fmax:
					fmax = F
					x1_max = coords[i][0]
					y1_max = coords[i][1]
					q1_max = coords[i][2]
					x2_max = coords[j][0]
					y2_max = coords[j][1]
					q2_max = coords[j][2]
					matrix[i][j] = F
				else:
					matrix[i][j] = F
	return matrix


#calculate the averageaverage euclidian distance
def average_euclidian(coords):
	total_distance = 0
	total_points = 0
	for i, (x1, y1, q1) in enumerate(coords):
		for j, (x2, y2, q2) in enumerate(coords):
			dx = x1 - x2
			dy = y1 - y2
			dist = sqrt(dx * dx + dy * dy)
			#print "Euclidian: %s" % dist
			if dist != 0:
				total_distance = total_distance + dist
				total_points = total_points + 1
				#print "Total Euclidian: %s" % total_distance
				#print "Total Points: %s" % total_points
			else:
				total_distance = total_distance
				#print "Total Euclidian: %s" % total_distance
	return (total_distance/total_points)

#calculate the standar deviation of euclidian distances
def standard_deviation(coords):
	average = average_euclidian(coords)
	total_distance = 0
	total_points = 0
	for i, (x1, y1, q1) in enumerate(coords):
		for j, (x2, y2, q2) in enumerate(coords):
			dx = x1 - x2
			dy = y1 - y2
			dist = sqrt(dx * dx + dy * dy)
		if dist != 0:
			total_distance = total_distance + ((dist-average)**2)
			total_points = total_points + 1
		# print "Total Euclidian: %s" % total_distance
		# print "Total Points: %s" % total_points
		else:
			total_distance = total_distance
	return sqrt((total_distance/total_points))


#calculate the coordinates of the new point
#calculate the new x
def new_x(x1, q1, x2, q2):
	return (x1 * (q1/(q1 + q2))) + (x2 * (q2/(q1 + q2)))

#calculate the new y
def new_y( y1, q1, y2, q2):
	return (y1 * (q1 / (q1 + q2))) + (y2 * (q2 / (q1 + q2)))

#calculate the new quantity
def new_q(q1, q2):
	return q1 + q2

"""
num_cities = 3
coords = []
dist_matrix = []
coords = [(1.0, 13.0, 10.0), (2.0, 6.0, 4.0), (2.0, 2.0, 3.0)]

average = average_euclidian(coords)
force = get_attraction_matrix(coords)
deviation = standard_deviation(coords)

print "Force: %s" % force
print "Coords: %s" % coords
print "Average Euclidian Distance: %s" % average
print "Standard Deviation: %s" % deviation

print "X1 Max: %s" % x1_max
print "Y1 Max: %s" %y1_max
print "Q1 Max: %s" %q1_max
#print i_max
print "X2 Max: %s" %x2_max
print "Y2 Max: %s" %y2_max
print "Q2 Max: %s" %q2_max
#print j_max

n_x = new_x(x1_max, y1_max, q1_max, x2_max, y2_max, q2_max)
print "New X: %s" % n_x

n_y = new_y(x1_max, y1_max, q1_max, x2_max, y2_max, q2_max)
print "New Y: %s" % n_y

n_q = new_q(q1_max, q2_max)
print "New Q: %s" % n_q
"""

#Define the current charges Data-set#
"""
n_charges = 3
charges = [charge(0,0,0) for i in range(n_charges)]
charges[0] = (1,13,10)
charges[1] = (2,6,4)
charges[2] = (2,2,3)
"""

n_charges = 0
#Open Data-set file - named 'test.csv - this format has x,y and q'
f = open('test.csv', "r", "utf-8-sig")
for line in f:
	n_charges = n_charges + 1

nip = n_charges

#print "NIP: %s" %nip
#print n_charges
f.seek(0)

charges=[]
data=[]
#Creates copy of data-set#
#important to always keep track of original charge's indexes#
for line in f:
	charges.append(map(int, line.strip().split(',')))
	data.append(map(int, line.strip().split(',')))

#Returns the average euclidian distance beetween points
average = average_euclidian(data)

#Returns the euclidian's distance standard deviation
deviation = standard_deviation(data)

#Returns the attraction force matrix - following coulomb law
force = get_attraction_matrix(data)

#Prints the pair of most attracted points: X,Y,Q and I index in "charges" list
"""
print "X1 Max: %s" %x1_max
print "Y1 Max: %s" %y1_max
print "Q1 Max: %s" %q1_max

print "X2 Max: %s" %x2_max
print "Y2 Max: %s" %y2_max
print "Q2 Max: %s" %q2_max
"""

#Calculates new charge, as result of previous both points junction
#Print new point
new_x = new_x(x1_max, q1_max, x2_max, q2_max)
#print "New X: %s" % new_x

new_y= new_y(y1_max, q1_max, y2_max, q2_max)
#print "New Y: %s" % new_y

new_q = new_q(q1_max, q2_max)
#print "New Q: %s" % new_q

#Print previous funciotns results
#print "Force: %s" % force
#print "Charges: %s" % charges
#print "Data: %s" % data
#print "Average Euclidian Distance: %s" % average
#print "Standard Deviation: %s" % deviation

#Cretates list of sectors#
limitq = 8
district = []
#district = [sector(0) for i in range(n_charges)]


district.append((charges.index([x1_max,y1_max,q1_max]),charges.index([x2_max,y2_max,q2_max])))
print "District: %s" %district
print "District[0]: %s" %str(district[0])


#To append an element do district[0] structure
"""
obj1 = list(district[0])
obj1.append(j_max)
district[0] = tuple(obj1)
print district[0]
print district
"""

#funcao para avaliar a atraccao com os pontos pertencentes a um setor
def atraction(sector,charges,x,y,q):
	matrix = [[0 for x in range(len(coords))] for y in range(len(coords))]
	fmax = 0;
	dist = 0;
	return matrix

#funcao que remove os pontos da copia do data-set original
def remove_charge(dots,i,j):
	dots.pop(i)
	dots.pop((j-1))
	return dots

#adiocionar o novo ponto, resultante, dos maximos, na copia do data-set
def insert_charge(dots,x,y,q):
	dots.append((x,y,q))
	return dots

data = remove_charge(data,charges.index([x1_max,y1_max,q1_max]),charges.index([x2_max,y2_max,q2_max]))
#data = insert_charge(data,new_x,new_y,new_q)
#print data

#ver quais os pontos que estao no setor
def read_sector(charges,sector):
	district = []
	a = 0
	j= 0
	for i in enumerate(sector):
		a = sector[j]
		#print a
		obj1 = list(charges[a])
		#print obj1
		district.append(tuple(obj1))
		j=j+1
	return district

district_read = read_sector(charges, district[0])
print "District Read: %s" %district_read


#print "Updated Charges: %s" %charges
#print "Updated Data: %s" %data

#definir o valor de nit...n_charges - numero de setores
def nit(n,district):
	j = 0
	for i in enumerate(district):
		n = n-1
	return n

#NIT paramether --> heuristic
nit = nit(n_charges,district)
#print  "NIT apos setorizacao: %s" %nit




#returns TOTAL QUANTITY in a district or sector
def district_q(district):
	total = 0
	for i, (x1, y1, q1) in enumerate(district):
		#print "X1: %s" %x1
		total = total + q1
	return total

district_totalquantity = district_q(district_read)
print "District Total Quantity: %s" % district_totalquantity

#returns de district centroid's X
def district_centroid_x(district,total_quantity):
	total = 0
	for i, (x1, y1, q1) in enumerate(district):
		#print "X1 - %s" %x1
		total = total + ((x1*q1)/total_quantity)
	return total

centroid_x = district_centroid_x(district_read,district_totalquantity)
print "Centroid X: %s" %centroid_x

#returns de district centroid's Y
def district_centroid_y(district,total_quantity):
	total = 0
	for i, (x1, y1, q1) in enumerate(district):
		#print "Y1 - %s" %y1
		total = total + ((y1*q1)/total_quantity)
	return total

centroid_y = district_centroid_y(district_read,district_totalquantity)
print "Centroid Y: %s" %centroid_y

#SECOND ITERATION#
#calculates attraction between data and district
def second_iteration(data):
	matrix = [[0 for x in range(len(data))] for y in range(len(data))]
	fmax = 0;
	dist= 0;
	global x3_max, y3_max, q3_max, x4_max, y4_max, q4_max, i2_max, j2_max, data_force
	for i, (x1, y1, q1) in enumerate(data):
		for j, (x2, y2, q2) in enumerate(data):
			dx = data[i][0] - data[j][0]
			dy = data[i][1] - data[j][1]
			q = data[i][2] * data[j][2]
			dist = sqrt(dx*dx + dy*dy)
			#print dist
			#to prevent the calculation of coulomb's force between one point and itself
			if dist == 0:
				matrix[i][j] = 0
			else:
				F = q /(dist * dist)
				if F > fmax:
					fmax = F
					x3_max = data[i][0]
					y3_max = data[i][1]
					q3_max = data[i][2]
					x4_max = data[j][0]
					y4_max = data[j][1]
					q4_max = data[j][2]
					matrix[i][j] = F
					data_force = F
				else:
					matrix[i][j] = F
	return matrix


#for i, (x1, y1, q1) in enumerate(data):
zzz = second_iteration(data)
#print "Force Matrix Second Iteration:"
#print zzz

"""
print "X1 Max: %s" %x3_max
print "Y1 Max: %s" %y3_max
print "Q1 Max: %s" %q3_max
#print "I Max: %s" %i2_max

print "X2 Max: %s" %x4_max
print "Y2 Max: %s" %y4_max
print "Q2 Max: %s" %q4_max
#print "J Max: %s" %j2_max
"""

print "Data Force: %s" %data_force

def data_district(data,x,y,q):
	fmax = 0;
	dist = 0;
	for i, (x1, y1, q1) in enumerate(data):
		dx = data[i][0] - x
		dy = data[i][1] - y
		charge = data[i][2] * q
		dist = sqrt(dx * dx + dy * dy)
		if dist == 0:
			return 0
		else:
			F = charge / (dist * dist)
			return F

district_force = data_district(data,centroid_x,centroid_y,district_totalquantity)
print "District - Data Force: %s" %district_force

district.append((charges.index([x3_max,y3_max,q3_max]),charges.index([x4_max,y4_max,q4_max])))
print "Districts"
print district




#EVALUTE THE SOLUTION#
#Calculate CVq#
#print "CVQ"
def cvq(sectors,charges):
	qi= 0
	k = 0
	cvq = 0
	error = 0
	sq = 0
	q_average = 0
	for i, (j,z) in enumerate(sectors):
		district_read = read_sector(charges, district[i])
		qi = qi + district_q(district_read)
		k = k + 1
		#print "Qi: %s" %qi

	q_average = qi / k
	print "Average Q: %s" %q_average

	for i, (j,z) in enumerate(sectors):
		district_read = read_sector(charges, district[i])
		error = error + ((district_q(district_read) - q_average) **2)

	sq = sqrt((1/(k-1))*error)
	print "SQ: %s" %sq
	cvq = sq / q_average
	return cvq

cvq = cvq(district,charges)
print "CVq: %s" %cvq

#Calculate CVd#
def cvd(sectors,charges):
	qi = 0
	k = 0
	error = 0
	sd = 0
	cvd = 0
	x = 0
	y = 0
	q = 0
	dist = 0
	dist_max = 0
	di = 0
	di_sum = 0
	di_sum2 = 0
	di_average = 0

	qi2 = 0
	x2 = 0
	y2 = 0
	q2 = 0
	dist2 = 0
	dist_max2 = 0
	di2 = 0
	di_sum2 = 0


	for i, (j,z) in enumerate(sectors):
		district_read = read_sector(charges, district[i])
		qi = district_q(district_read)
		x =  district_centroid_x(district_read,qi)
		#print x
		y = district_centroid_y(district_read, qi)
		#print y
		k = k + 1
		for a, (x2, y2, q2) in enumerate(district_read):
			dx = district_read[a][0] - x
			dy = district_read[a][1] - y
			dist = sqrt(dx*dx + dy*dy)
			if dist >= dist_max:
				dist_max = dist
			else:
				dist_max = dist_max
		di = qi/dist_max
		#print "Di: %s" %di
		di_sum = di_sum + di
		#print "Qij: %s" %qi

	di_average = di_sum / k

	for i, (j,z) in enumerate(sectors):
		district_read = read_sector(charges, district[i])
		qi2 = district_q(district_read)
		x2 =  district_centroid_x(district_read,qi2)
		#print x
		y2 = district_centroid_y(district_read, qi2)
		#print y
		for a, (x, y, q) in enumerate(district_read):
			dx2 = district_read[a][0] - x2
			dy2 = district_read[a][1] - y2
			dist2 = sqrt(dx2*dx2 + dy2*dy2)
			if dist2 >= dist_max2:
				dist_max2 = dist2
			else:
				dist_max2 = dist_max2
		di2 = qi2/dist_max2
		#print di2
		di_sum2 = di_sum2 + ((di2-di_average)**2)
		#print "Qij: %s" %qi
	sd = sqrt((1/(k-1))*di_sum2)
	#print "SD: %s" %sd
	cvd = sd/di_average
	return cvd

cvd = cvd(district,charges)
print "CVd: %s" %cvd

#Objective Function Value#
def objective(cvq,cvd):
	objective = (0.3*cvq) + (0.7*cvd)
	return objective

value = objective(cvq,cvd)
print "Objective: %s" %value