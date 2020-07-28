import pandas as pd 
import numpy as np 

# Extracting features of 2019 movies from wikipedia

link = "https://en.wikipedia.org/wiki/List_of_American_films_of_2018"

df1 = pd.read_html(link, header=0)[2]
df2 = pd.read_html(link, header=0)[3]
df3 = pd.read_html(link, header=0)[4]
df4 = pd.read_html(link, header=0)[5]



df = df1.append(df2.append(df3.append(df3.append(df4,ignore_index = True),
ignore_index = True),ignore_index = True),ignore_index = True)
print(df.columns)

# extracting features of the movie from TMDb using api

from tmdbv3api import TMDb
import json 
import requests
tmdb =TMDb()
tmdb.api_key = ''

from tmdbv3api import Movie
tmdb_movie = Movie()

def get_genres(x):
    genres = []
    result = tmdb_movie.search(x)
    movie_id = result[0].id 
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key={}'.format(movie_id,tmdb.api_key))
    data_json = response.json()
    if data_json['genres']:
        genres_str = ""
        for i in range(0,len(data_json['genres'])):
            genres.append(data_json['genres'][i]['name'])
        return genres_str.join(genres)
    else:
        np.NaN



df['genres'] = df['Title'].map(lambda x: get_genres(str(x)))
print(df.columns)
df.to_csv('./api_data.csv')

df1_2018 = pd.read_csv('./api_data.csv')
df_2018 = df1_2018[['Title','Cast and crew','genres']]
# print(df_2018['Cast and crew'][0])

def get_director(x):
    if "(director)" in x:
        return(x.split(" (director)")[0])
    elif("(directors)" in x):
        return(x.split(" (director)")[0])

df_2018["director_name"] = df_2018["Cast and crew"].map(lambda x: get_director(x))


def get_actor1(x):
    return((x.split('screenplay); ')[-1]).split(",")[0])

df_2018['actor_1_name'] = df_2018['Cast and crew'].map(lambda x: get_actor1(x))
print(df_2018['actor_1_name'])

def get_actor2(x):
    if len((x.split('screenplay); ')[-1]).split(", ")) < 2:
        return np.NaN
    else:
        return((x.split("screenplay); ")[-1]).split(", ")[1])

df_2018['actor_2_name'] = df_2018['Cast and crew'].map(lambda x:get_actor2(x))
print(df_2018['actor_2_name'])

def get_actor3(x):
    if len((x.split('screenplay); ')[-1]).split(", ")) < 3:
        return np.NaN
    else:
        return((x.split("screenplay); ")[-1]).split(", ")[2])

df_2018['actor_3_name'] = df_2018['Cast and crew'].map(lambda x:get_actor3(x))
# print(df_2018['actor_3_name'])

df_2018['actor_2_name'] = df_2018['actor_2_name'].replace(np.NaN,'unknown')
df_2018['actor_3_name'] = df_2018['actor_3_name'].replace(np.NaN,'unknown')

df_2018 = df_2018.rename(columns = {'Title':'movie_title'})

new_df18 = df_2018.loc[:,['director_name','actor_1_name','actor_2_name','actor_3_name','genres','movie_title']]
print(new_df18)

new_df18['movie_title'] = new_df18['movie_title'].str.lower()

new_df18['comb'] = new_df18['actor_1_name'] + ' ' + new_df18['actor_2_name'] + ' ' + new_df18['actor_3_name'] + ' '+ new_df18['director_name'] + ' ' + new_df18['genres']

print(new_df18.columns)    

# Extracting features of 2019 movies from wikipedia


link = "https://en.wikipedia.org/wiki/List_of_American_films_of_2019"

df1 = pd.read_html(link,header = 0)[3]
df2 = pd.read_html(link,header = 0)[4]
df3 = pd.read_html(link,header = 0)[5]
df4 = pd.read_html(link,header = 0)[6]

df = df1.append(df2.append(df3.append(df3.append(df4,ignore_index = True),
ignore_index = True),ignore_index = True),ignore_index = True)
print(df)

df['genres'] = df['Title'].map(lambda x: get_genres(str(x)))
df.to_csv('./api_csv_2019')

df1_2019 = pd.read_csv("./api_csv_2019")
df_2019 = df1_2019[['Title','Cast and crew','genres']]


df_2019["director_name"] = df_2019["Cast and crew"].map(lambda x: get_director(x))

df_2019['actor_1_name'] = df_2019['Cast and crew'].map(lambda x: get_actor1(x))

df_2019['actor_2_name'] = df_2019['Cast and crew'].map(lambda x: get_actor2(x))

df_2019['actor_3_name'] = df_2019['Cast and crew'].map(lambda x: get_actor3(x))

df_2019['actor_2_name'] = df_2019['actor_2_name'].replace(np.NaN,'unknown')
df_2019['actor_3_name'] = df_2019['actor_3_name'].replace(np.NaN,'unknown')

df_2019 = df_2019.rename(columns = {'Title':'movie_title'})

new_df19 = df_2019.loc[:,['director_name','actor_1_name','actor_2_name','actor_3_name','genres','movie_title']]
# print(new_df19)

new_df19['movie_title'] = new_df19['movie_title'].str.lower()

new_df19['comb'] = new_df19['actor_1_name'] + ' ' + new_df18['actor_2_name'] + ' ' + new_df18['actor_3_name'] + ' '+ new_df18['director_name'] + ' ' + new_df18['genres']

my_df = new_df18.append(new_df19,ignore_index = True)


old_df = pd.read_csv('./new_data.csv')

final_df = old_df.append(my_df,ignore_index = True)


final_df = final_df.dropna(how = 'any')

final_df.to_csv('./final_data.csv',index = False)
print('done')
