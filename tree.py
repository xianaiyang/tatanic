# -*- coding: utf-8 -*-
"""
Created on Mon Feb 02 17:04:35 2015

@author: Xiaoxian
@version: 0.0
"""
from tatanic import inform_entrop,gini_ind,finite_feature_filter, load_csv
import random
class tree_node:
    def __init__(self,feature,leaf,lable):
        self.feature = feature
        self.leaf = leaf
        self.child = {lable:{}}
def tree_build(xy,lab,feature_index):
    label = [int(m[-1]) for m in xy]
    xx = [m[:-1] for m in xy]
    labelset = set(label)
    if len(labelset) == 1:
        return tree_node(label[0],True,None)
    elif unseprable(xx) or len(xx) == 0:
        plus_count = 0
        for data in label:
            if data == 1:
                plus_count += 1
        if plus_count >= float(len(label))/2.0:
            return tree_node(1,True,None)
        else:
            return tree_node(0,True,None)
    else:
        best_feature = feature_selcet_discrete(xy)
        feature_value = lab[best_feature]
        featurei = [m[best_feature] for m in xy]
        values = set(featurei)
        values_list = []
        for data in values:
            values_list.append(data)
        root = tree_node(feature_index[feature_value],False,feature_value) # tree root
        for value in values_list:
            child_data = []
            for data in xy:
                if data[best_feature] == value:
                    reduc_data = []
                    for number in data[:best_feature]:
                        reduc_data.append(number)
                    reduc_data.extend(data[best_feature+1:])
                    child_data.append(reduc_data[:])
                    reduc_feature = lab[:best_feature]
                    reduc_feature.extend(lab[best_feature+1:])
            root.child[feature_value][value] = tree_build(child_data,reduc_feature,feature_index)
    return root
        
def unseprable(xx):
    for data in xx:
        for index in range(len(data) - 1):
            if xx[0][index] != data[index]: return False
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
    ylabel = [int(m[-1]) for m in xy]
    entro_before = inform_entrop(ylabel)
    max_inform_gain = 0
    best_feature = 0
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
                label = [int(m[-1]) for m in branch_x]
                entrop += float(len(branch_x))/len(ylabel)*inform_entrop(label)
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
def train(trainfile):
    (data,feature,feature_index) = load_csv(trainfile)
    (data_filter,feature_filter) = finite_feature_filter(data,feature)
    data_random = []
    for i in range(len(data)):
        k = random.randint(0,len(data_filter) -1)
        data_random.append(data_filter[k][:])
    tree_root = tree_build(data_random,feature_filter,feature_index)
    return tree_root
def predict(root,testfile):
    (xx,lable,feature_index) = load_csv(testfile)
    result = []
    for data in xx:
        temp = root
        while temp.leaf == False:
            if data[temp.feature] not in temp.child[lable[temp.feature]].keys():
                break
            temp = temp.child[lable[temp.feature]][data[temp.feature]]
        if temp.leaf == True:
            result.append(temp.feature)
        else:
            result.append(0)
    return result
def rate(result,lable):
    right = 0
    for i in range(len(result)):
        if result[i] == lable[i]:
            right += 1
    return float(right)/len(result)
def randomforest(trainfile,testfile):
        root = train(trainfile)
        pred = array(predict(root,testfile))
        for i in range(300):
            root = train(trainfile)
            pred = pred + array(predict(root,testfile))
        pred = pred/float(301)
        result = []
        for data in pred:
            if data >= 0.5:
                result.append(1)
            else:
                result.append(0)
        return result
            
        
    