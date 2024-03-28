#!/usr/bin/env python
# coding: utf-8

# In[1]:


global_itemset = {}


# In[2]:


def create_l1_itemset(transactions):
    temp_item_set = {}
    for item_set in transactions:
        for item in item_set:
            key = frozenset([item])
            temp_item_set[key] = temp_item_set[key] + 1 if key in temp_item_set else 1
            global_itemset[key] = global_itemset[key] + 1 if key in global_itemset else 1
    return temp_item_set


# In[3]:


def prune(itemset, transactions, min_support, transactions_length):
    new_itemset = {}
    for k, v in itemset.items():
        if v/transactions_length >= min_support:
            new_itemset[k] = v
        else:
            transactions = [[item for item in row if item not in list(k)] for row in transactions]
    return new_itemset, transactions


# In[4]:


from itertools import chain, combinations
def get_union(transactions, k):
    new_set = {}
    for itemSet in transactions:
        comb = list(combinations(itemSet, k))
        for c in comb:
            key = frozenset(c)
            new_set[key] = new_set[key] + 1 if key in new_set else 1
            global_itemset[key] = global_itemset[key] + 1 if key in global_itemset else 1
    return new_set


# In[5]:


def powerset(s):
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s)))


# In[6]:


def get_association_rules(itemset, min_confidence, min_lift, transactions_length):
    rules = []
    for item in itemset.keys():
        support = global_itemset[item]/transactions_length
        subsets = powerset(item)
        for subset in subsets:
            lhs = frozenset(subset)
            rhs = frozenset(element for element in item if element not in subset)
            confidence = (global_itemset[lhs.union(rhs)]/transactions_length)/(global_itemset[lhs]/transactions_length)
            if confidence >= min_confidence:
                lift = confidence / (global_itemset[rhs]/transactions_length)
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


def apriori(transactions, min_support, max_length, min_confidence, min_lift):
    itemset = create_l1_itemset(transactions)
    k = 2
    while k <= max_length:
        itemset, transactions = prune(itemset, transactions, min_support, len(transactions))
        unioned = get_union(transactions, k)
        if unioned:
            itemset = unioned
            k+=1
        else:
            break
    rules = get_association_rules(itemset, min_confidence, min_lift, len(transactions))
    sorted_rules = sorted(rules, key=lambda x: x['lift'], reverse=True)
    return sorted_rules

