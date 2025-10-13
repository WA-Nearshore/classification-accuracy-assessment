# Compute fuzzy error matrix

# load libraries
import arcpy
import pandas as pd

# import data to pd dataframe
sample_points = r"..\KAMaccuracy.gdb\TAC_2022_SamplePoints_Method2_Fuzzy"

sample_df = pd.DataFrame(arcpy.da.FeatureClassToNumPyArray(sample_points))

sample_df.head()
