# Local poulation density in Sweden

Administrative spatial data in Sweden is often based on a national grid system, dividing Sweden into 250 by 250 meter grid square. Here, I was working with data on the population residing in each grid. 

`nbrs_radius.py` calculates the population density in a circle with a given radius (in meters) from each grid square centroid. I do this by first establishing which squares are in each others circles using scipy. Results are exported to Stata for further analysis.


