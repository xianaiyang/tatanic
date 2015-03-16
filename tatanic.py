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
    feature_index = {}
    for index in range(len(csv_head)):
        feature_index[csv_head[index]] = index
    return (data, csv_head, feature_index)
def inform_entrop(label):
    n = len(label)
    plus_count = 0
    for i in label:
        if i == 1:
            plus_count += 1
    prob_plus = float(plus_count)/n
    if prob_plus >= 1.0 - 1.0e-8 or prob_plus <= 1.0e-8:
        return 0
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
def finite_feature_filter(data,lable):
    data = array(data)
    result = []
    labl = []
    for i in range(len(data[0]) - 1):
        if len(set(data[:,i])) < 8:
            result.append(data[:,i])
            labl.append(lable[i])
    result.append(data[:,-1])
    labl.append(lable[-1])
    result = array(result).transpose()
    return (result,labl)
