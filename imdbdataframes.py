import seaborn as sbs
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#trysplit function that deals with list of genres
def trysplit(x):
    try:
        return x.split(',')
    except:
        return []


#Setting whether to generate a fresh .pkl of each file
gen_title_basics = False
gen_title_ratings = False

if gen_title_basics == True:
    tb_col_dict={'tconst':np.character, 
                 'titleType':str, 
                 'primaryTitle':str,
                 'originalTitle':str,
                 'genres':np.character}
    title_basics = pd.read_csv('title.basics.tsv',
                                delimiter='\t', 
                                dtype=tb_col_dict).set_index('tconst')
    title_basics['genres'] = title_basics['genres'].apply(trysplit)
    title_basics['genres'].astype(list)
    title_basics.to_pickle('title.basics.pkl')

if gen_title_ratings == True:
    tr_col_dict={'tconst':np.character, 
                 'averageRating':np.float_, 
                 'numVotes':np.int_}
    title_ratings = pd.read_csv('title.ratings.tsv',
                                delimiter='\t', 
                                dtype=tr_col_dict).set_index('tconst')
    title_ratings.dropna(subset=['numVotes'],inplace=True)
    title_ratings.to_pickle('title.ratings.pkl')

tr = pd.read_pickle('title.ratings.pkl')
tb = pd.read_pickle('title.basics.pkl')

#Extract Movies From title.basics
extractor = tb['titleType'] == 'movie'
tbmovies = tb[extractor][['genres']]
overthresh = tr[tr['numVotes'] >= 5000]

#Extract Fantasy Movies
fanextract = []
for item in tbmovies['genres']:
    if 'Fantasy' in item:
        fanextract.append(True)
    else:
        fanextract.append(False)
fanextract = np.array(fanextract)
fantasy = tbmovies[fanextract]
fantasy_ratings = fantasy[['primaryTitle']].join(
        overthresh,
        how='inner')
fantasy_ratings['genre'] = 'Fantasy'

#Extract Comedy Movies
comextract = []
for item in tbmovies['genres']:
    if 'Comedy' in item:
        comextract.append(True)
    else:
        comextract.append(False)
comextract = np.array(comextract)
comedy = tbmovies[comextract]
comedy_ratings = comedy[['primaryTitle']].join(
        overthresh,
        how='inner')
comedy_ratings['genre'] = 'Comedy'

#Extract Sci-Fi Movies
sciextract = []
for item in tbmovies['genres']:
    if 'Sci-Fi' in item:
        sciextract.append(True)
    else:
        sciextract.append(False)
sciextract = np.array(sciextract)
scifi = tbmovies[sciextract]
scifi_ratings = scifi[['primaryTitle']].join(
        overthresh,
        how='inner')
scifi_ratings['genre'] = 'Sci-Fi'

#Extract Documentary Movies
docextract = []
for item in tbmovies['genres']:
    if 'Documentary' in item:
        docextract.append(True)
    else:
        docextract.append(False)
docextract = np.array(docextract)
doc = tbmovies[docextract]
doc_ratings = doc[['primaryTitle']].join(
        overthresh,
        how='inner')
doc_ratings['genre'] = 'Documentary'

#Extract Drama Movies
dramaextract = []
for item in tbmovies['genres']:
    if 'Drama' in item:
        dramaextract.append(True)
    else:
        dramaextract.append(False)
dramaextract = np.array(dramaextract)
drama = tbmovies[dramaextract]
drama_ratings = drama[['primaryTitle']].join(
        overthresh,
        how='inner')
drama_ratings['genre'] = 'Drama'

#Extract Romance Movies
romextract = []
for item in tbmovies['genres']:
    if 'Romance' in item:
        romextract.append(True)
    else:
        romextract.append(False)
romextract = np.array(romextract)
rom = tbmovies[romextract]
rom_ratings = rom[['primaryTitle']].join(
        overthresh,
        how='inner')
rom_ratings['genre'] = 'Romance'

#Extract Horror Movies
horextract = []
for item in tbmovies['genres']:
    if 'Horror' in item:
        horextract.append(True)
    else:
        horextract.append(False)
horextract = np.array(horextract)
horror = tbmovies[horextract]
horror_ratings = horror[['primaryTitle']].join(
        overthresh,
        how='inner')
horror_ratings['genre'] = 'Horror'

#Concatenate Together
together = pd.concat([doc_ratings,
                      drama_ratings,
                      rom_ratings,
                      comedy_ratings,
                      fantasy_ratings,
                      scifi_ratings, 
                      horror_ratings],
                     ignore_index=True)

#Plot
sbs.violinplot(x=together['genre'],y=together['averageRating'])
plt.xticks(rotation=20)
plt.show()
