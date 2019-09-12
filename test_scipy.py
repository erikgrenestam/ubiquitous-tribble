import numpy as np
import scipy.spatial as spatial
import fiona
from shapely.geometry import shape
import time

path = 'C:/Users/Erik/OneDrive/Work/Gis befolkning till Martin/befolkning.shp'

points = fiona.open(path)

ids = [ feat['properties']['id'] for feat in points ]
geoms = [ shape(feat["geometry"]) for feat in points ]

list_arrays = [ np.array((geom.xy[0][0], geom.xy[1][0])) for geom in geoms ]

point_tree = spatial.cKDTree(list_arrays)

for rad in range(3000,16000,1000):
    for i, point in enumerate(list_arrays):
        print("Point no " + str(i))
        t = time.process_time()
        ball = point_tree.query_ball_point(point,float(rad))
        nbrs_id = [ids[j] for j in ball]
        #nbrs_points = [list_arrays[j] for j in ball]
        if i == 0:
            nbrs = np.array([np.repeat(ids[i], len(nbrs_id), axis=0), np.asarray(nbrs_id)],dtype=int).transpose()
        else:
            a = np.array([np.repeat(ids[i], len(nbrs_id), axis=0), np.asarray(nbrs_id)],dtype=int).transpose()
            nbrs = np.append(a,nbrs,axis=0)
            print(time.process_time() - t)

    np.savetxt(f"nbrs_{rad}.csv", nbrs, fmt='%i', delimiter=",")    
    