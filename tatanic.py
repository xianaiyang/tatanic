# -*- coding: utf-8 -*-
"""
Created on Fri Jan 23 10:06:21 2015

@author: Administrator
"""
from numpy import *
from PIL import Image
from matplotlib.pylab import *
import csv as csv
from math import log
def load_csv(filename):
    csv_file_object = csv.reader(open(filename,'rb'))
    csv_head = csv_file_object.next() #ignore the first line including list head
    data = []
    for row in csv_file_object:
        data.append(row)
    data = array(data)
    return data
def inform_entrop(label):
    n = len(label)
    plus_count = 0
    for i in label:
        if int(i) == 1:
            plus_count += 1
    prob_plus = float(plus_count)/n
    return -prob_plus*log(prob_plus) - (1-prob_plus)*log(1-prob_plus)
def gini_ind(label):
    plus_count = sum(label==1)
    n = len(label)
    plus_count = 0
    for i in label:
        if label[i] == 1:
            plus_count += 1
    prob_plus = float(plus_count)/n
    return prob_plus*(1-prob_plus)
def finite_feature_filter(data):
    data = array(data)
    result = []
    for i in range(len(data[0]) - 1):
        if len(set(data[:,i])) < 8:
            result.append(data[:,i])
    result.append(data[:,-1])
    result = array(result).transpose()
    return result