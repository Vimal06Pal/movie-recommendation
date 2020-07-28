import pandas as pd 
import numpy as np 

# Extracting features of 2019 movies from wikipedia

link = "https://en.wikipedia.org/wiki/List_of_American_films_of_2020"

df1 = pd.read_html(link, header=0)[2]
df2 = pd.read_html(link, header=0)[3]
df3 = pd.read_html(link, header=0)[4]
df4 = pd.read_html(link, header=0)[5]


df = df1.append(df2.append(df3.append(df4,ignore_index = True),ignore_index = True),ignore_index= True)

df_2020 = df[['Title','Cast and crew']]

from tmdbv3api import TMDb
import json 
import requests
tmdb = TMDb()
tmdb.api_key = ''

from tmdbv3api import Movie
tmdb_movie = Movie()
def get_genre(x):
    genres = []
    result = tmdb_movie.search(x)
    movie_id = result[0].id
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}'.format(movie_id,tmdb.api_key))
    data_json = response.json()
    if data_json['genres']:
        genre_str = " " 
        for i in range(0,len(data_json['genres'])):
            genres.append(data_json['genres'][i]['name'])
        return genre_str.join(genres)
    else:
        np.NaN

df_2020['genres'] = df_2020['Title'].map(lambda x: get_genre(x))
df_2020.to_csv('./api_2020.csv')

df_2020 = pd.read_csv('./api_2020.csv') 

def get_director(x):
    if " (director)" in x:
        return(x.split("(director)")[0])
    elif "(directors)" in x:
        return(x.split(" (director)")[0])
    else:
        return(x.split("(director/screenplay)")[0])

df_2020["director_name"] = df_2020['Cast and crew'].map(lambda x: get_director(str(x)))


def get_actor1(x):
    return((x.split("screenplay); ")[-1].split(", ")[0]))

df_2020["actor_1_name"] = df_2020['Cast and crew'].map(lambda x: get_director(str(x)))

def get_actor2(x):
    if len((x.split("screenplay); ")[-1]).split(", ")) < 2 :
        return np.NaN
    else:
        return((x.split("screenplay); ")[-1]).split(", ")[1])

df_2020['actor_2_name'] = df_2020['Cast and crew'].map(lambda x: get_actor2(str(x)))

def get_actor3(x):
    if len((x.split("screenplay); ")[-1]).split(", ")) < 3:
        return np.NaN
    else:
        return((x.split("screenplay); ")[-1]).split(", ")[2])

df_2020['actor_3_name'] = df_2020['Cast and crew'].map(lambda x: get_actor3(str(x)))

df_2020 = df_2020.rename(columns={'Title':'movie_title'})

new_df20 = df_2020.loc[:,['director_name','actor_1_name','actor_2_name','actor_3_name','genres','movie_title']]

new_df20['comb'] = new_df20['actor_1_name'] + ' ' + new_df20['actor_2_name'] + ' ' + new_df20['actor_3_name'] + ' '+ new_df20['director_name'] + ' ' + new_df20['genres']

print(new_df20.isna().sum())

new_df20 = new_df20.dropna(how = 'any')

print(new_df20.isna().sum())

new_df20['movie_title'] = new_df20['movie_title'].str.lower()


old_df = pd.read_csv('./final_data.csv')

final_df = old_df.append(new_df20,ignore_index = True)


final_df.to_csv('./main_data.csv',index = False)
print('done')
