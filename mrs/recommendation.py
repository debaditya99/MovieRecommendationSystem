import numpy as np
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
#from sklearn.feature_extraction.text import CountVectorizer

from sklearn.metrics.pairwise import cosine_similarity
from urllib.request import urlopen
import json

from django.conf import settings
import os

base_dir =settings.MEDIA_ROOT    
my_file = os.path.join(base_dir, 'final_data.csv')

data=pd.read_csv(my_file)
data.drop(columns=['Unnamed: 0'], inplace=True)
data=data.iloc[0:12000]
# creating a count matrix
cv = TfidfVectorizer(stop_words='english')
count_matrix = cv.fit_transform(data['comb'])

count_matrix=count_matrix.astype('float32')

'''#dimensionality reduction
from sklearn.decomposition import TruncatedSVD

svd=TruncatedSVD(n_components=1000)
lat_mat=svd.fit_transform(count_matrix)
'''

# creating a similarity score matrix
similarity = cosine_similarity(count_matrix)

def recommend(m):
    m = m.lower()
    if m not in data['movie_title'].unique():
        return('Please check the spelling or try with some other movies')
    else:
        i = data.loc[data['movie_title']==m].index[0]
        lst = list(enumerate(similarity[i]))
        lst = sorted(lst, key = lambda x:x[1] ,reverse=True)
        lst = lst[1:11] # not taking 1st item as it's the movie itself
        l = []
        for i in range(len(lst)):
            a = lst[i][0]
            l.append(data['movie_title'][a])
        return l

api="83974895e4ad671936671f04f559f146"
def input(movie): 
    try:
        movie=movie.lower()
        #Initializing the recommendation engine
        rcmd=recommend(movie)

        #Checking the condition
        if rcmd=='Please check the spelling or try with some other movies':
            return rcmd

        #Completing the search query
        data=movie.replace(" ","%20")

        #Searching for the exact movie name from the results
        #Searching for the movie_id and title to get other details
        result=urlopen("https://api.themoviedb.org/3/search/movie?api_key="+api+"&query=" + data).read().decode('utf-8')
        result=json.loads(result)
        #peint(result)
        title=""
        mid=0

        for i in range(0,3):
            if movie==result['results'][i]['original_title'].lower():
                mid=result['results'][i]['id']
                title=result['results'][i]['original_title']
                break

        '''for i in range(0,5):
            if movie==result['results'][i]['original_title'].lower():
                title=result['results'][i]['original_title']
                mid=result['results'][i]['id']
        '''
        if movie==title.lower():
            pass
        else:
            title=result['results'][0]['original_title']
            mid=result['results'][0]['id']

        #Fetching the movie details from the movie_id
        result=urlopen("https://api.themoviedb.org/3/movie/" + str(mid) + "?api_key="+api+"&language=en-US").read().decode('utf-8')
        result=json.loads(result)

        overview=result['overview']
        status=result['status']
        date=result['release_date']
        runtime=result['runtime']
        revenue=result['revenue']
        link=result['homepage']
        poster="https://image.tmdb.org/t/p/original/" + result['poster_path']

        m_details=[title.upper(),overview,status,date,runtime,revenue,link,poster]

        #Fetching the cast_id and name from movie_id
        result=urlopen("https://api.themoviedb.org/3/movie/" + str(mid) + "/credits?api_key="+api+"&language=en-US").read().decode('utf-8')
        result=json.loads(result)

        cid=[]
        name=[]
        character=[]
        for i in range(0,5):
            cid.append(result['cast'][i]['id'])
            name.append(result['cast'][i]['name'])
            character.append(result['cast'][i]['character'])

        #Fetching the cast data from cast_id
        bio=[] 
        profiles=[]
        for i in range(0,5):
            result=urlopen("https://api.themoviedb.org/3/person/" + str(cid[i]) + "?api_key="+api+"&language=en-US").read().decode('utf-8')
            result=json.loads(result)
            bio.append(result['biography'])
            profiles.append("https://image.tmdb.org/t/p/original/" + result['profile_path'])

        c_details=[name,character,bio]

        #Fetching the posters of recommended movies by first getting the movie_id(s)
        names=[]
        mids=[]
        posters=[]
        for m in rcmd:
            m=m.lower()
            m=m.replace(" ","%20")

            result=urlopen("https://api.themoviedb.org/3/search/movie?api_key="+api+"&query=" + m).read().decode('utf-8')
            result=json.loads(result)

            names.append(result['results'][0]['original_title'])
            mids.append(result['results'][0]['id'])

        for ids in mids:
            result=urlopen("https://api.themoviedb.org/3/movie/" + str(ids) + "?api_key="+api+"&language=en-US").read().decode('utf-8')
            result=json.loads(result)
            posters.append("https://image.tmdb.org/t/p/original/" + result['poster_path'])

        r_details=[names, posters]
    
        
        return m_details, c_details, r_details, profiles
    
    except:
           return('Please check the spelling or try with some other movies')
