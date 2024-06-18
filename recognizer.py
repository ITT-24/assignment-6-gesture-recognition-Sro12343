# $1 gesture recognizer

import numpy as np
import scipy
from datetime import datetime

from Point import Point



class Rectangle():
    def __init__(self, x, y, width, height):    
        self.X = x
        self.Y = y
        self.Width = width
        self.Height = height

   
class Result():#  constructor
    def __init__(self, name, score, ms):
        self.Name = name
        self.Score = score
        self.Time = ms

class Unistroke():
    def __init__(self,name, points):
        self.Name = name
        coords = np.array([[p.X, p.Y] for p in points])
        resampled_coords = scipy.signal.resample(coords, NumPoints)
        self.Points = [Point(x, y) for x, y in resampled_coords]
        self.radians = IndicativeAngle(self.Points)
        self.Points = RotateBy(self.Points, -self.radians)
        self.Points = ScaleTo(self.Points, SquareSize)
        self.Points = TranslateTo(self.Points, Origin)
        self.Vector = Vectorize(self.Points)
        
NumUnistrokes = 16
NumPoints = 64
SquareSize = 250.0
Origin = Point(0,0)
Diagonal = np.sqrt(SquareSize * SquareSize + SquareSize * SquareSize)
HalfDiagonal = 0.5 * Diagonal
AngleRange =   np.deg2rad(45.0)
AnglePrecision = np.deg2rad(2.0)
Phi = 0.5 * (-1.0 + np.sqrt(5.0))# Golden Ratio

class dolar_recognizer():
    def __init__(self,Unistrokes):
        self.Unistrokes = Unistrokes
    
    def Recognize(self, points, useProtractor):
    
        t0 = datetime.now()
        candidate = Unistroke("", points)

        u = -1
        b = +np.inf  
        for i in range(len(self.Unistrokes)):
            if (useProtractor):
                
                d = OptimalCosineDistance(self.Unistrokes[i].Vector, candidate.Vector)#  Protractor
            else:
                d = DistanceAtBestAngle(candidate.Points, self.Unistrokes[i], -AngleRange, +AngleRange, AnglePrecision)#  Golden Section Search (original $1)
            if d < b:
                b = d#  best (least) distance
                u = i#  unistroke index
            
        t1 = datetime.now()
        
        if u == -1:
            result = Result("No match.", 0.0, t1-t0)
        else: 
            if useProtractor:
                score = 1.0 - b
            else: 
                score = 1.0 - b / HalfDiagonal
            result = Result(self.Unistrokes[u].Name, score, t1-t0)
        return result
        
        
    def AddGesture(self,name, points):
        self.Unistrokes.append(Unistroke(name, points))#  append new unistroke
        num = 0  
        for i in range(len(self.Unistrokes)):
            if (self.Unistrokes[i].Name == name):
                num +=1
        
        return num
    
    def DeleteUserGestures(self):
        self.Unistrokes = self.Unistrokes[:NumUnistrokes]#  clear any beyond the original set
        return NumUnistrokes


def IndicativeAngle(points):
    c = Centroid(points)
    return np.arctan2(c.Y - points[0].Y, c.X - points[0].X)


def RotateBy(points, radians):#  rotates points around centroid

	c = Centroid(points)  
	cos = np.cos(radians)  
	sin = np.sin(radians)  
	newpoints = []
	for i in range(len(points)-1):
		qx = (points[i].X - c.X) * cos - (points[i].Y - c.Y) * sin + c.X
		qy = (points[i].X - c.X) * sin + (points[i].Y - c.Y) * cos + c.Y
		newpoints.append(Point(qx, qy)) 
	return newpoints  

def ScaleTo(points, size): #   non-uniform scale   assumes 2D gestures (i.e., no lines)
	B = BoundingBox(points)
	newpoints = []
	for i in range(len(points)):
		qx = points[i].X * (size / B.Width)  
		qy = points[i].Y * (size / B.Height)  
		newpoints.append(Point(qx, qy))  
	
	return newpoints  



def TranslateTo(points, pt): #   translates points' centroid
	c = Centroid(points)
	newpoints = []
	for i in range(len(points)):
		qx = points[i].X + pt.X - c.X
		qy = points[i].Y + pt.Y - c.Y
		newpoints.append(Point(qx, qy))
	return newpoints

def Vectorize(points):#  for Protractor
    sum = 0.0
    vector = []
    for i in range(len(points)):
        vector.append(points[i].X)
        vector.append(points[i].Y)
        sum += points[i].X * points[i].X + points[i].Y * points[i].Y
    magnitude = np.sqrt(sum)
    for i in range(len(vector)):
        vector[i] /= magnitude
    return vector


def OptimalCosineDistance(v1, v2):#  for Protractor
	a = 0.0  
	b = 0.0  
	for i in range(0, len(v1), 2):
		a += v1[i] * v2[i] + v1[i+1] * v2[i+1]  
		b += v1[i] * v2[i+1] - v1[i+1] * v2[i]  
	angle =  np.arctan(b / a)
	return np.arccos(a * np.cos(angle) + b * np.sin(angle))  

def DistanceAtBestAngle(points, T, a, b, threshold):
	x1 = Phi * a + (1.0 - Phi) * b  
	f1 = DistanceAtAngle(points, T, x1)  
	x2 = (1.0 - Phi) * a + Phi * b  
	f2 = DistanceAtAngle(points, T, x2)  
	while (np.abs(b - a) > threshold):
	
		if (f1 < f2):
			b = x2  
			x2 = x1  
			f2 = f1  
			x1 = Phi * a + (1.0 - Phi) * b  
			f1 = DistanceAtAngle(points, T, x1)  
		else:
			a = x1  
			x1 = x2  
			f1 = f2  
			x2 = (1.0 - Phi) * a + Phi * b  
			f2 = DistanceAtAngle(points, T, x2)  
	
	return min(f1, f2)  



def DistanceAtAngle(points, T, radians):
	newpoints = RotateBy(points, radians)
	return PathDistance(newpoints, T.Points)


def Centroid(points):
    x = 0.0 
    y = 0.0
    for i in range(len(points)):
        x += points[i].X
        y += points[i].Y
    x /= len(points)
    y /= len(points)
    return Point(x, y)

def BoundingBox(points):
    x_coords = [p.X for p in points]
    y_coords = [p.Y for p in points]
    min_x = min(x_coords)
    max_x = max(x_coords)
    min_y = min(y_coords)
    max_y = max(y_coords)
    return Rectangle(min_x, min_y, max_x-min_x, max_y-min_y)

def PathDistance(pts1, pts2):
    d = 0.0  
    for i in range(len(pts1)):#   assumes pts1.length == pts2.length
        d += Distance(pts1[i], pts2[i])  
    return d / len(pts1)

def PathLength(points):
	d = 0.0
	for i in range(len(points)):
		d += Distance(points[i - 1], points[i])
	return d

def Distance(p1, p2):
	dx = p2.X - p1.X
	dy = p2.Y - p1.Y
	return np.sqrt(dx * dx + dy * dy)  
