import pandas as pd
from torchctr.layers import EmbeddingLayer
from torchctr.datasets import (FeatureDict, get_movielens, make_datasets, read_data, defaults, fillna)

# step 1: download dataset
root = get_movielens('datasets', 'ml-1m')

# step 2: read data
users = read_data(root / 'users.dat', sep='::', names=['UserID', 'Gender', 'Age', 'Occupation', 'Zip-code'])
movies = read_data(root / 'movies.dat', sep='::', names=['MovieID', 'Title', 'Genres'])
ratings = read_data(root / 'ratings.dat', sep='::', names=['UserID', 'MovieID', 'Rating', 'Timestamp'])

# step 3: make dataset
dataset = pd.merge(ratings, users, on='UserID')
dataset = pd.merge(dataset, movies, on='MovieID')

# make features
sparse_features = ['UserID', 'Gender', 'Age', 'Occupation', 'Zip-code', 'MovieID']
sequence_features = ['Genres']
dataset = fillna(dataset, dataset.columns, fill_v='unk')
features = FeatureDict(sparse_features, None, sequence_features)
input, _ = make_datasets(dataset, features, sep='|')

# build model
model = EmbeddingLayer(input).to(defaults.device)
print(model)
out = model(input)
print(out.shape, out, sep='\n')