import numpy as np
import scipy.spatial as spatial
import fiona
from shapely.geometry import shape
import pandas as pd

class NbrList:
    
    def __init__(self):
        self.data = []
        
    def update(self, rows):
        for r in rows:
            self.data.append(r)
    
    def finalize(self):
        #return np.asarray(self.data, dtype=int)
        return pd.DataFrame(self.data, columns=['id_i', 'id']).astype(int)


SHP_PATH = _your_path

points = fiona.open(SHP_PATH)
ids = [ feat['properties']['id'] for feat in points ]
geoms = [ shape(feat["geometry"]) for feat in points ]
list_arrays = [ np.array((geom.xy[0][0], geom.xy[1][0])) for geom in geoms ]
point_tree = spatial.cKDTree(list_arrays)

nbrs = NbrList()

df_pop = pd.read_csv('befolkning_2017_id.csv')

for rad in range(10000,25000,5000):    
    for i, (point, id_i) in enumerate(zip(list_arrays,ids)):
        print("Point no " + str(i))
        
        ball = point_tree.query_ball_point(point,float(rad))
        nbrs_id = [(id_i,ids[j]) for j in ball]
        nbrs.update(nbrs_id)        

    df = nbrs.finalize()
    df = df.merge(df_pop, how='left', on='id', validate='many_to_one')
    
    #collapse on id_i
    df_agg = df[['n','id_i']].groupby(['id_i']).sum()
    df_agg.reset_index(level=0, inplace=True)
    del df
    
    #merge coordinates
    df_agg.rename(columns={"id_i": "id"}, inplace=True)
    df_agg = df_agg.merge(df_pop, how='left', on='id', validate='many_to_one')
    df_agg.rename(columns={"n_x": "n_circle", "n_y": "n"}, inplace=True)
    
    #calc population density in circle    
    km = int(rad/1000)
    area = km*km*3.14159
    df_agg[f'pop_dens_{km}km'] = df_agg['n_circle'] / area
    
    #export to Stata
    df_agg.to_stata(f'nbrs_{rad}.dta')
    
