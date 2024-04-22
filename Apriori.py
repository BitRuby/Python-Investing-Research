#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


def create_l1_itemset(transactions, global_itemset):
    temp_itemsets = {}
    for index, row in transactions.iterrows():
        for key in transactions.keys():
            frozen_key = frozenset([key])
            if row[key] == 1:
                temp_itemsets[frozen_key] = temp_itemsets[frozen_key] + 1 if frozen_key in temp_itemsets else 1
                global_itemset[frozen_key] = global_itemset[frozen_key] + 1 if frozen_key in global_itemset else 1
    return temp_itemsets, global_itemset


# In[3]:


def prune(itemset, transactions, min_support, t_length):
    new_itemset = {}
    for k, v in itemset.items():
        if v/t_length >= min_support:
            new_itemset[k] = v
        else:
            for key in list(k):
                if key in transactions.columns:
                    transactions.drop(columns=key, inplace=True)
    return new_itemset, transactions


# In[4]:


from itertools import chain, combinations
def get_union(transactions, k, global_itemset):
    new_set = {}
    for index, row in transactions.iterrows():
        itemset = []
        for key in transactions.keys():
            if row[key] == 1:
                itemset.append(key)
        comb = list(combinations(itemset, k))
        for c in comb:
            key = frozenset(c)
            new_set[key] = new_set[key] + 1 if key in new_set else 1
            global_itemset[key] = global_itemset[key] + 1 if key in global_itemset else 1
    return new_set, global_itemset


# In[5]:


def powerset(s):
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s)))


# In[6]:


def get_association_rules(itemset, min_confidence, min_lift, global_itemset, t_length):
    rules = []
    for item in itemset.keys():
        support = global_itemset[item]/t_length
        subsets = powerset(item)
        for subset in subsets:
            lhs = frozenset(subset)
            rhs = frozenset(element for element in item if element not in subset)
            confidence = (global_itemset[lhs.union(rhs)]/t_length)/(global_itemset[lhs]/t_length)
            if confidence >= min_confidence:
                lift = confidence / (global_itemset[rhs]/t_length)
                if lift >= min_lift:
                    rules.append({
                       'lhs': lhs,
                        'rhs': rhs,
                        'support': support,
                        'confidence': confidence,
                        'lift': lift 
                    })
    return rules


# In[7]:


import time
def apriori(tx, min_support, max_length, min_confidence, min_lift):
    transactions = tx
    t_length = len(transactions)
    start_time = time.time()
    global_itemset = {}
    itemset, global_itemset = create_l1_itemset(transactions, global_itemset)
    k = 2
    while k <= max_length:
        itemset, transactions = prune(itemset, transactions, min_support, t_length)
        unioned, global_itemset = get_union(transactions, k, global_itemset)
        if unioned:
            itemset = unioned
            k+=1
            if k > max_length:
                itemset, transactions = prune(itemset, transactions, min_support, t_length)
        else:
            break
    rules = get_association_rules(itemset, min_confidence, min_lift, global_itemset, t_length)
    sorted_rules = sorted(rules, key=lambda x: x['lift'], reverse=True)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Elapsed time:", elapsed_time, "seconds")
    return sorted_rules


# In[ ]:




