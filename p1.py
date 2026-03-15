# import the lib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import re
from sklearn.metrics.pairwise import cosine_similarity

# load the data
data = pd.read_csv("movies.csv")
print(data)

# check for null data
print(data.isnull().sum())

# clean title
def clean_title(txt):
	txt = txt.lower()
	txt = re.sub("[^A-Za-z]"," ",txt)	
	return txt
data["clean_title"] = data["title"].apply(clean_title)	
print(data)

# clean genres
def clean_genres(txt):
	txt = txt.lower()
	txt = re.sub("[|]"," ",txt)	
	return txt
data["clean_genres"] = data["genres"].apply(clean_genres)	
print(data)

# text vectorization
tv = TfidfVectorizer()
vector = tv.fit_transform(data["clean_genres"])

# ask for movie name 
t = input("enter movie title: ")
ct = clean_title(t)
print(t)
print(ct)

# suggest the movie
g = data[data.clean_title.str.contains(ct)]
print(g)
print(g.shape)

if g.shape[0] == 0:
	print("movie does not exist")
else:
	print("Movie exist")
	gt = " ".join(g["clean_genres"])
	print(gt)
	vgt = tv.transform([gt])
	print(vgt)

	cs = cosine_similarity(vgt, vector)	# 2d array
	print(cs)

	fcs = cs.flatten()			# 1d array
	print(fcs)

	indices = fcs.argsort()[-100:][::-1]	# top matches
	print(indices)

	res = data.iloc[indices]
	print(res["title"], res["genres"])


















