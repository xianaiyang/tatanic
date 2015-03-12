# -*- coding: utf-8 -*-
"""
Created on Mon Feb 02 17:04:35 2015

@author: Administrator
"""
from tatanic import inform_entrop,gini_ind,finite_feature_filter
class tree_node:
    def __init__(self,value,leaf):
        self.value = []
        for data in value:
            self.value.append(data)
        self.leaf = leaf
        self.left_child = None
        self.right_slib = None
def tree_build(xy):
    label = [m[-1] for m in xy]
    xx = [m[:-1] for m in xy]
    labelset = set(label)
    if len(labelset) == 1:
        return tree_node([label[0]],True)
    elif unseprable(xx):
        plus_count = 0
        for data in label:
            if data == 1:
                plus_count += 1
        if plus_count >= len(label):
            return tree_node([1],True)
    else:
        discrete_feature = finite_feature_filter(xy)
    return 0
        
def unseprable(xx):
    for data in xx:
        if xx[0] != data: return False
    return True        
def major(a):
    #calculate the majority of a dictionary and return the key
    keys = set(a)
    dic = {}
    for key in keys:
        dic.setdefault(key,0)
    for m in a:
        dic[m] += 1
    maxkey = a[0]
    for key in keys:
        if dic[key] > dic[maxkey]:
            maxkey = key
    return maxkey
def feature_selcet_discrete(xy):
    #select the largest information gain for the finite values feature
    xx = [m[0:-1] for m in xy]
    ylabel = [m[-1] for m in xy]
    entro_before = inform_entrop(ylabel)
    print entro_before
    max_inform_gain = 0
    best_feature = -float('inf')
    for i in range(len(xx[0])):
        featurei = [m[i] for m in xx]
        values = set(featurei)
        if len (values) == 1:
            entrop = entro_before
        else:
            sep_x = []
            entrop = 0
            for branch in values:
                branch_x = []
                for data in xy:
                    if data[i] == branch:
                        branch_x.append(data)
                sep_x.append(branch_x)
                entrop += float(len(branch_x))/len(ylabel)*inform_entrop([m[-1] for m in branch_x])
        if entro_before - entrop > max_inform_gain:
            max_inform_gain = entro_before - entrop
            best_feature = i
    return best_feature
def feature_select_continue(xy):
    xx = [m[0:-1] for m in xy]
    ylabel = [m[-1] for m in xy]
    gini_before = gini_ind(ylabel)
    max_gini_gain = 0
    best_feature = -float('inf')
    best_theta = -float('inf')
    for i in range(len(xx[0])):
        featurei = [[xy[i],xy[-1]] for m in xy] #the feature label list
        featurei.sort()
        for j in range(len(featurei) - 1):
            thetaj = (featurei[j][0] + featurei[j + 1][0])/2.0
            ginij = float(j + 1)/len(featurei)*gini_ind(featurei[:j+1][1]) \
                + float(len(featurei) - j - 1)/len(featurei)*gini_ind(featurei[j+1:][1])
            if max_gini_gain < gini_before - ginij:
                max_gini_gain = gini_before - ginij
                best_theta = thetaj
                best_feature = i
    return (best_theta,best_feature)
                
    