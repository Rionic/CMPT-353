import pandas as pd 
import sys
import difflib as dl
file1 = sys.argv[1]
file2 = sys.argv[2]
file3 = sys.argv[3]


mlist = open(file1).readlines()
ratings =  pd.read_csv(file2)

def matcher(title): 
    a = dl.get_close_matches(title, mlist, cutoff=0.6)
    if len(a)>=1:
        a = a[0]
        return a

ratings['matches'] = pd.DataFrame(ratings['title'].apply(matcher))
ratings['matches'] = ratings['matches'].str.strip('\n')
ratings = ratings.drop(columns=['title'])
ratings = ratings.sort_values(by=['matches'])
ratings = ratings.groupby(['matches']).mean()
ratings = ratings.round(2)
ratings.to_csv(file3)