from __future__ import division
from codecs import open
import sys, random
import csv
from math import sqrt, ceil
from pickle import *
import time

limit_qtt=350

#NIP and NIT values
nip = 0
nit = 0


#Defines every charge
class charge(object):

	def __init__(self,lista):
		self.x = lista[0]
		self.y = lista[1]
		self.q = lista[2]

	def __str__(self):
            return "x->%s y->%s q->%s" %(self.x,self.y,self.q)


# Defines every sector or district
class sector(object):
    def __init__(self):
        self.nodes=[]
        self.centx = 0
        self.centy = 0
        self.sumq = 0

    def secprint(self):
        str=""
        str= "x->%s y->%s q->%s n->%s\n" %(self.centx,self.centy,self.sumq,len(self.nodes))
        for p in self.nodes:
            str = str + "- x->%s y->%s q->%s\n" %(p.x,p.y,p.q)
        return str

    def new_sector(self,i,j):
        self.centx = (i.q*i.x+j.q*j.x)/(i.q+j.q)
        self.centy = (i.q*i.y+j.q*j.y)/(i.q+j.q)
        self.sumq = i.q+j.q
        self.nodes.append(charge((i.x,i.y,i.q)))
        self.nodes.append(charge((j.x,j.y,j.q)))

    def add_to_sector(self, i):
        self.nodes.append(charge((i.x, i.y, i.q)))
        self.centx = 0
        self.centy = 0
        self.sumq = 0
        for p in self.nodes:
            self.centx = self.centx + p.x * p.q
            self.centy = self.centy + p.y * p.q
            self.sumq = p.q + self.sumq
        self.centx = self.centx / self.sumq
        self.centy = self.centy / self.sumq


def get_attraction(x1, x2):
    if (x1.x == x2.x and x1.y == x2.y):
        return 0
    else:
        return (x1.q * x2.q / (pow(x1.x - x2.x, 2) + pow(x1.y - x2.y, 2)))


# calculate the attraction matrix between points
#uso sempre
def get_attraction_max(coords):
    max = 0
    maxx = 0
    maxy = 0
    for i in range(0, len(coords)):
        for j in range(0, len(coords)):
            attr = get_attraction(coords[i], coords[j])
            if (max < attr):
                max = attr
                maxx = i
                maxy = j
    return maxx,maxy,max

def get_attraction_max_sector(coords,sectors):
    max = 0
    maxx = 0
    maxy = 0
    for i in range(0, len(coords)):
        for j in range(0, len(sectors)):
            if(sectors[j].sumq + coords[i].q < limit_qtt):
                c=charge((sectors[j].centx,sectors[j].centy,sectors[j].sumq))
                attr = get_attraction(coords[i], c)
                if (max < attr):
                    max = attr
                    maxx = i
                    maxy = j
    return maxx,maxy,max

#uso apenas para imprimir
def get_attraction_matrix(coords):
    matrix = [[0 for x in range(len(coords))] for y in range(len(coords))]
    for i in range(0, len(coords)):
        for j in range(0, len(coords)):
            matrix[i][j] = get_attraction(coords[i], coords[j])
    return matrix


#Open Data-set file - named 'test.csv - this format has x,y and q'
f = open('test.csv', "r", "utf-8-sig")
charges=[]
data=[]
sectors=[]
#Creates copy of data-set#
#important to always keep track of original charge's indexes#
for line in f:
    c=charge(map(int, line.strip().split(',')))
    if(c.q!=0):
        charges.append(c)
        #data.append(c)


#for p in charges:
#   print p
#print get_attraction_max(charges)
data=charges

i=0

#for p in data:
#   print p

while len(data)>0:
    x, y, max = get_attraction_max(data)
    xs, ys, maxs = get_attraction_max_sector(data, sectors)
    #print max, maxs
    if(max>=maxs):
        s=sector()
        s.new_sector(data[x],data[y])
        sectors.append(s)
        data.pop(x)
        data.pop(y-1)
    else:
        sectors[ys].add_to_sector(data[xs])
        print data[xs]
        data.pop(xs)


#DEBUG PRINTING
#print sectors
for p in sectors:
    print p.secprint()
    print p.sumq
#print charges
#for p in charges:
#  print p

#print data after sectorization
#for p in data:
#    print data


#EVALUTE THE SOLUTION#
#Calculate CVq#
#print "CVQ"

def cvq(sectors):
    qi= 0
    k = 0
    cvq = 0
    error = 0
    sq = 0
    q_average = 0

    for p in sectors:
        qi = qi + p.sumq
        k = k + 1
        print "Qi: %s" %qi

    q_average = qi / k
    print "Average Q: %s" %q_average

    for p in sectors:
        error = error + (( p.sumq - q_average) **2)

    sq = sqrt((1/(k-1))*error)
    print "SQ: %s" %sq
    cvq = sq / q_average
    return cvq

cvq = cvq(sectors)
print "CVq: %s" %cvq

#Calculate CVd#
def cvd(sectors):
    qi = 0
    k = 0
    error = 0
    sd = 0
    cvd = 0
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

    for p in sectors:
        k = k + 1
        for i in p.nodes:
            dist = pow(i.x - p.centx, 2) + pow(i.y - p.centy, 2)
            if dist >= dist_max:
                dist_max = dist
            else:
                dist_max = dist_max
        di = p.sumq/dist_max
        di_sum = di_sum + di

    di_average = di_sum / k

    for a in sectors:
        for j in a.nodes:
            dist2 = pow(j.x - a.centx, 2) + pow(j.y - a.centy, 2)
            if dist2 >= dist_max2:
                dist_max2 = dist2
            else:
                dist_max2 = dist_max2
        di2 = a.sumq/dist_max2
        #print di2
        di_sum2 = di_sum2 + ((di2-di_average)**2)
    #print "Qij: %s" %qi

    sd = sqrt((1/(k-1))*di_sum2)
    #print "SD: %s" %sd
    cvd = sd/di_average
    return cvd

cvd = cvd(sectors)
print "CVd: %s" %cvd

#Objective Function Value#
def objective(cvq,cvd):
	objective = (0.3*cvq) + (0.7*cvd)
	return objective

value = objective(cvq,cvd)
print "Objective: %s" %value
