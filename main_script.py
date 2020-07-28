# importing libraries

import numpy as np 
import pandas as pd 
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def create_similarity():
    data = pd.read_csv('./main_data.csv')
    # creating a count matrix 
    cv = CountVectorizer()
    count_matrix = cv.fit_transform(data['comb'])
    # creating a similarity score matrix 
    similarity = cosine_similarity(count_matrix)
    return(data,similarity)

def rcmd(m):
    m = m.lower()
    try:
        data.head()
        similarity.shape
    except:
        data, similarity = create_similarity()
    if m not in data['movie_title'].unique():
        return("Sorry! The movie you requested is not in our database. Please check the spelling or try with some other movies")
    else:
        i = data.loc[data['movie_title'] == m].index[0] # i is the row position where movie is present
        lst = list(enumerate(similarity[i]))# list of enumerate obj(similar to dict which track trhe count of the similarity with respect to the index where movie is present)
        lst = sorted(lst, key = lambda x: x[1], reverse= True)
        lst = lst[1:11] # excluding first item since it is the requested movie itself
        l= []
        d={}
        col = ['director_name', 'actor_1_name', 'actor_2_name', 'actor_3_name','genres', 'movie_title', 'comb']
        for i in range(len(lst)):
            a = lst[i][0] 
            d[col[5]] = data[col[5]][a]
            d[col[4]] = data[col[4]][a]
            d[col[1]] = data[col[1]][a]
            d[col[2]] = data[col[2]][a]
            d[col[3]] = data[col[3]][a]
            d[col[0]] = data[col[0]][a]
            l.append(d)
            d={}
        df = pd.DataFrame(l)
        return(df)

m= input("\n enter the movie\n")
lis = rcmd(m)
print("the recommented movies are {}\n".format(lis))

