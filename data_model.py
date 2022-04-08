# -*- coding: utf-8 -*-
"""data_model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TcwaygjYn_VBAwF3JgryX2wZtzSKX6HV
"""

""" https://secure-taiga-22138.herokuapp.com """

# INITIALIZE VARIABLES


""" userId = random.randint(1, 1000)
ToD = random.randint(0, 3)
lat = "19.24384914913549"
lng = "72.8558975474386"
ll = lat+","+lng
limit = "5" """


import sys
from time import time
import pandas as pd
import numpy as np
import random
import requests
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
userDf = pd.read_csv("LSS-Users.csv")
categoryDf = pd.read_csv("LSS-Categories.csv")
integratedDf = pd.read_csv('LSS-Integrated-Dataset.csv')

filtered_category_id_list = []
similar_categories_list = []
output_dict = []
counter = 0

cv = CountVectorizer()
countMatrix = cv.fit_transform(categoryDf["integrated_category_label"])
cosineSimilarity = cosine_similarity(countMatrix)


def get_index_from_id(categoryId):
    return categoryDf[categoryDf.integrated_category_id == categoryId]["integrated_category_index"].values[0]


def get_category_from_index(index):
    return categoryDf[categoryDf.index == index]["integrated_category_label"].values[0]


def find_similar_categories_id(filtered_category_id_list):
    for category_user_interacts_with_filtered in filtered_category_id_list:
        categoryIndex = get_index_from_id(
            category_user_interacts_with_filtered)
        similar_categories = list(enumerate(cosineSimilarity[categoryIndex]))
        sorted_similar_categories = sorted(
            similar_categories, key=lambda x: x[1], reverse=True)
        find_similar_category_labels(sorted_similar_categories)


def find_similar_category_labels(sorted_similar_categories):
    i = 0
    similar_categories_list.clear()
    for category in sorted_similar_categories:
        similar_categories_list.append(get_category_from_index(category[0]))
        i = i+1
        if i > 9:
            break


def chooseUserTime(userId, ToD):
    filtered_category_id_list.clear()

    userDF = integratedDf.loc[integratedDf['integrated_user_id'] == userId]
    timeDF = userDF.loc[integratedDf['integrated_time_of_day'] == ToD]

    ratingDF = timeDF.loc[integratedDf['integrated_rating'] >= 3]

    for filtered_category_id in ratingDF['integrated_category_id'].tolist():
        filtered_category_id_list.append(filtered_category_id)

    find_similar_categories_id(filtered_category_id_list)

    return similar_categories_list


def call_location_api_for_nearby_places(ll, limit):
    url = "https://api.foursquare.com/v3/places/search?ll="+ll+"&limit="+limit
    headers = {
        "Accept": "application/json",
        "Authorization": "fsq39jO8WFIAh3sRnTihdqXKuj5QBv4uGAT6mJIY3Lq5Oj8="
    }
    return requests.request("GET", url, headers=headers)


def filter_similar_categories_according_to_location(userId, ToD, ll, limit):

    similar_categories_list = chooseUserTime(userId, ToD)
    response = call_location_api_for_nearby_places(ll, limit)
    input_dict = json.loads(response.text)

    aaa = []
    for i in range(int(limit)-1):
        for category_name in similar_categories_list:
            # print(category_name)
            # PART OF CODE GIVING ERROR IS THIS IF STMT
            # THE ERROR IS LIST INDEX OUT OF RANGE
            if input_dict["results"][i]['categories'][0]['name'] == category_name:
                aaa.append(input_dict["results"][i])
    return aaa


""" print('For user',userId,'at',ToD,'recommendations are:')
print(filter_similar_categories_according_to_location(userId, ToD, ll, limit))

 """