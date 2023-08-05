'''
    __author__ = 'sladesal'
    __time__ = '20171128'
    __bolg__ = 'www.shataowei.com'
'''
# -*- coding:utf-8 -*-
import random as rd
import math as ma
from sklearn.feature_selection import VarianceThreshold
import numpy as np
import pandas as pd
import sys
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import SelectFromModel
from sklearn.ensemble import GradientBoostingClassifier
import matplotlib as mat

'''
    k_var : 方差选择需要满足的最小值
    pearson_value_k : 想剔除的feature个数
    vif_k ： 想剔除的feature个数
    wrapper_k ：想保留的feature个数
    way ： 'l1'正则或者'l2'正则
    C_0 : 惩罚力度
'''


class feature_filter:
    def __init__(self, k_var=None, pearson_value_k=None, vif_k=None, wrapper_k=None, C_0=0.1, way='l2'):
        self.k_var = k_var
        self.pearson_value_k = pearson_value_k
        self.vif_k = vif_k
        self.wrapper_k = wrapper_k
        self.way = way
        self.C_0 = C_0

    # 方差选择法
    def var_filter(self, data):
        k = self.k_var
        var_data = data.var().sort_values()
        if k is not None:
            new_data = VarianceThreshold(threshold=k).fit_transform(data)
            return var_data, new_data
        else:
            return var_data

    # 线性相关系数衡量
    def pearson_value(self, data, label):
        k = self.pearson_value_k
        label = str(label)
        # k为想删除的feature个数
        Y = data[label]
        x = data[[x for x in data.columns if x != label]]
        res = []
        for i in range(x.shape[1]):
            data_res = np.c_[Y, x.iloc[:, i]].T
            cor_value = np.abs(np.corrcoef(data_res)[0, 1])
            res.append([label, x.columns[i], cor_value])
        res = sorted(np.array(res), key=lambda x: x[2], reverse=True)
        if k is not None:
            if k < len(res):
                new_c = []  # 保留的feature
                for i in range(len(res) - k):
                    new_c.append(res[i][1])
                return res, new_c
            else:
                print('feature个数越界～')
        else:
            return res

    # 共线性检验
    def vif_test(self, data, label):
        label = str(label)
        # k为想删除的feature个数
        x = data[[x for x in data.columns if x != label]]
        res = np.abs(np.corrcoef(x.T))
        vif_value = []
        for i in range(res.shape[0]):
            for j in range(res.shape[0]):
                if j > i:
                    vif_value.append([x.columns[i], x.columns[j], res[i, j]])
        vif_value = sorted(vif_value, key=lambda x: x[2])
        if k is not None:
            if k < len(vif_value):
                new_c = []  # 保留的feature
                for i in range(len(x)):
                    if vif_value[-i][1] not in new_c:
                        new_c.append(vif_value[-i][1])
                    else:
                        new_c.append(vif_value[-i][0])
                    if len(new_c) == k:
                        break
                out = [x for x in x.columns if x not in new_c]
                return vif_value, out
            else:
                print('feature个数越界～')
        else:
            return vif_value

    # Mutual Information
    def MI(self, X, Y):
        # len(X) should be equal to len(Y)
        # X,Y should be the class feature
        total = len(X)
        X_set = set(X)
        Y_set = set(Y)
        if len(X_set) > 10:
            print('%s非分类变量，请检查后再输入' % X_set)
            sys.exit()
        elif len(Y_set) > 10:
            print('%s非分类变量，请检查后再输入' % Y_set)
            sys.exit()
        # Mutual information
        MI = 0
        eps = 1.4e-45
        for i in X_set:
            for j in Y_set:
                indexi = np.where(X == i)
                indexj = np.where(Y == j)
                ijinter = np.intersect1d(indexi, indexj)
                px = 1.0 * len(indexi[0]) / total
                py = 1.0 * len(indexj[0]) / total
                pxy = 1.0 * len(ijinter) / total
                MI = MI + pxy * np.log2(pxy / (px * py) + eps)
        return MI

    def mic_entroy(self, data, label):
        label = str(label)
        # k为想删除的feature个数
        x = data[[x for x in data.columns if x != label]]
        Y = data[label]
        mic_value = []
        for i in range(x.shape[1]):
            if len(set(x.iloc[:, i])) <= 10:
                res = self.MI(Y, x.iloc[:, i])
                mic_value.append([x.columns[i], res])
        mic_value = sorted(mic_value, key=lambda x: x[1])
        return mic_value

    # 递归特征消除法
    def wrapper_way(self, data, label):
        k = self.wrapper_k
        # k 为要保留的数据feature个数
        label = str(label)
        label_data = data[label]
        col = [x for x in data.columns if x != label]
        train_data = data[col]
        res = pd.DataFrame(
            RFE(estimator=LogisticRegression(), n_features_to_select=k).fit_transform(train_data, label_data))
        res_c = []
        for i in range(res.shape[1]):
            for j in range(data.shape[1]):
                if (res.iloc[:, i] - data.iloc[:, j]).sum() == 0:
                    res_c.append(data.columns[j])
        res.columns = res_c
        return res

    # l1/l2正则方法
    def embedded_way(self, data, label):
        way = self.way
        C_0 = self.C_0
        label = str(label)
        label_data = data[label]
        col = [x for x in data.columns if x != label]
        train_data = data[col]
        res = pd.DataFrame(
            SelectFromModel(LogisticRegression(penalty=way, C=C_0)).fit_transform(train_data, label_data))
        res_c = []
        for i in range(res.shape[1]):
            for j in range(data.shape[1]):
                if (res.iloc[:, i] - data.iloc[:, j]).sum() == 0:
                    res_c.append(data.columns[j])
        res.columns = res_c
        return res

    # 基于树模型特征选择
    def tree_way(self, data, label):
        label = str(label)
        label_data = data[label]
        col = [x for x in data.columns if x != label]
        train_data = data[col]
        res = pd.DataFrame(SelectFromModel(GradientBoostingClassifier()).fit_transform(train_data, label_data))
        res_c = []
        for i in range(res.shape[1]):
            for j in range(data.shape[1]):
                if (res.iloc[:, i] - data.iloc[:, j]).sum() == 0:
                    res_c.append(data.columns[j])
        res.columns = res_c
        return res


class null_dealing(object):
    def __init__(self):
        ''''this is my pleasure , slade sal!'''

    def Key_Dealing(self, data_input, key_value=0.95):
        data_union = []
        data_union = pd.DataFrame(data_union)
        x = data_input
        y = key_value
        for i in range(len(x.columns)):
            data1 = x.iloc[:, i].dropna(how='any')
            key = data1.quantile(y)
            data2 = x.iloc[:, i]
            data2 = data2.fillna(value=key)
            data2[data2 > key] = key
            data_union = pd.concat([data_union, data2], axis=1)
        return data_union

    def Value_Dealing(self, data_input, Value):
        data_union = []
        data_union = pd.DataFrame(data_union)
        x = data_input
        y = Value
        for i in range(len(x.columns)):
            key = y
            data2 = x.iloc[:, i]
            data2 = data2.fillna(value=key)
            data2[data2 > key] = key
            data_union = pd.concat([data_union, data2], axis=1)
        return data_union

    def Value_Mode(self, data_input, key_value=0.95):
        data_union = []
        data_union = pd.DataFrame(data_union)
        x = data_input
        y = key_value
        for i in range(len(x.columns)):
            data1 = x.iloc[:, i].dropna(how='any')
            data1 = data1.copy()
            key = data1.value_counts().argmax()
            data2 = data1.copy()
            key1 = data2.quantile(y)
            data3 = x.iloc[:, i]
            data3[data3 > key1] = key1
            data3 = data3.fillna(value=key)
            data_union = pd.concat([data_union, data3], axis=1)
        return data_union


class sample(object):
    def __init__(self):
        ''''this is my pleasure'''

    def group_sample(self, data_set, label, percent=0.1):
        # 分层抽样
        # data_set:数据集
        # label:分层变量
        # percent:抽样占比
        # q:每次抽取是否随机,null为随机
        # 抽样根据目标列分层，自动将样本数较多的样本分层按percent抽样，得到目标列样本较多的特征欠抽样数据
        x = data_set
        y = label
        z = percent
        diff_case = pd.DataFrame(x[y]).drop_duplicates([y])
        result = []
        result = pd.DataFrame(result)
        for i in range(len(diff_case)):
            k = np.array(diff_case)[i]
            data_set = x[x[y] == k[0]]
            nrow_nb = data_set.iloc[:, 0].count()
            data_set.index = range(nrow_nb)
            index_id = rd.sample(range(nrow_nb), int(nrow_nb * z))
            result = pd.concat([result, data_set.iloc[index_id, :]], axis=0)
        new_data = pd.Series(result['label']).value_counts()
        new_data = pd.DataFrame(new_data)
        new_data.columns = ['cnt']
        k1 = pd.DataFrame(new_data.index)
        k2 = new_data['cnt']
        new_data = pd.concat([k1, k2], axis=1)
        new_data.columns = ['id', 'cnt']
        max_cnt = max(new_data['cnt'])
        k3 = new_data[new_data['cnt'] == max_cnt]['id']
        result = result[result[y] == k3[0]]
        return result

    def under_sample(self, data_set, label, percent=0.1, q=1):
        # 欠抽样
        # data_set:数据集
        # label:抽样标签
        # percent:抽样占比
        # q:每次抽取是否随机
        # 抽样根据目标列分层，自动将样本数较多的样本按percent抽样，得到目标列样本较多特征的欠抽样数据
        x = data_set
        y = label
        z = percent
        diff_case = pd.DataFrame(pd.Series(x[y]).value_counts())
        diff_case.columns = ['cnt']
        k1 = pd.DataFrame(diff_case.index)
        k2 = diff_case['cnt']
        diff_case = pd.concat([k1, k2], axis=1)
        diff_case.columns = ['id', 'cnt']
        max_cnt = max(diff_case['cnt'])
        k3 = diff_case[diff_case['cnt'] == max_cnt]['id']
        new_data = x[x[y] == k3[0]].sample(frac=z, random_state=q, axis=0)
        return new_data

    def combine_sample(self, data_set, label, number, percent=0.35, q=1):
        # 组合抽样
        # data_set:数据集
        # label:目标列
        # number:计划抽取多类及少类样本和
        # percent：少类样本占比
        # q:每次抽取是否随机
        # 设定总的期待样本数量，及少类样本占比，采取多类样本欠抽样，少类样本过抽样的组合形式
        x = data_set
        y = label
        n = number
        p = percent
        diff_case = pd.DataFrame(pd.Series(x[y]).value_counts())
        diff_case.columns = ['cnt']
        k1 = pd.DataFrame(diff_case.index)
        k2 = diff_case['cnt']
        diff_case = pd.concat([k1, k2], axis=1)
        diff_case.columns = ['id', 'cnt']
        max_cnt = max(diff_case['cnt'])
        k3 = diff_case[diff_case['cnt'] == max_cnt]['id']
        k4 = diff_case[diff_case['cnt'] != max_cnt]['id']
        n1 = p * n
        n2 = n - n1
        fre1 = n2 / float(x[x[y] == k3[0]]['label'].count())
        fre2 = n1 / float(x[x[y] == k4[1]]['label'].count())
        fre3 = ma.modf(fre2)
        new_data1 = x[x[y] == k3[0]].sample(frac=fre1, random_state=q, axis=0)
        new_data2 = x[x[y] == k4[1]].sample(frac=fre3[0], random_state=q, axis=0)
        test_data = pd.DataFrame([])
        if int(fre3[1]) > 0:
            i = 0
            while i < (int(fre3[1])):
                data = x[x[y] == k4[1]]
                test_data = pd.concat([test_data, data], axis=0)
                i += 1
        result = pd.concat([new_data1, new_data2, test_data], axis=0)
        return result
