#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pd
from sklearn.cluster import KMeans, Birch, SpectralBiclustering, DBSCAN
from sklearn.metrics import davies_bouldin_score, silhouette_score

def cluster_validation_sil(df): 
    """
    Conduct multiple Silhouette scores calculations with different algorithms. 
    Argument: a standardized dataframe
    Return: a dataframe with three columns of scores
    """
    
    dbs=[]
    #calculate scores of three algorithms
    for i in range(3,11):
        c1 = KMeans(n_clusters=i, random_state=1, algorithm='auto').fit(df) 
        label1 = c1.labels_
        c2 = Birch(n_clusters=i).fit(df)
        label2 = c2.labels_
        c3 = SpectralBiclustering(n_clusters=i, random_state=1).fit(df)
        label3 = c3.row_labels_

        dbs.append([silhouette_score(df, label1),
                    silhouette_score(df, label2),
                    silhouette_score(df, label3)])
    #change column name
    result = pd.DataFrame(dbs).rename(columns={0:'K-Means',
                                                  1:'Birch',
                                                  2:'Spectral Biclustering'})
    return result


def cluster_validation_dav(df): 
    """
    Conduct multiple Davies-Bouldin scores calculations with different algorithms. 
    Argument: a standardized dataframe
    Return: a dataframe with three columns of scores
    """
        
    dbs=[]
    #calculate scores of three algorithms
    for i in range(3,11):
        c1 = KMeans(n_clusters=i, random_state=1, algorithm='auto').fit(df) 
        label1 = c1.labels_
        c2 = Birch(n_clusters=i).fit(df)
        label2 = c2.labels_
        c3 = SpectralBiclustering(n_clusters=i, random_state=1).fit(df)
        label3 = c3.row_labels_

        dbs.append([davies_bouldin_score(df, label1),
                    davies_bouldin_score(df, label2),
                    davies_bouldin_score(df, label3)])
    #change column name
    result = pd.DataFrame(dbs).rename(columns={0:'K-Means',
                                                  1:'Birch',
                                                  2:'Spectral Biclustering'})
    return result
