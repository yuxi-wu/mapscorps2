import pandas as pd
import numpy as np

prod = pd.read_excel("ProductivityData.xlsx", sheetname="FC Productivity")
geoprod = pd.read_excel("ProductivityData.xlsx", sheetname="GeoArea Productivity")
placesprod = pd.read_excel("ProductivityData.xlsx", sheetname="Places Productivity Report")

placesprod.rename({"PlaceId": "Place_Id"})

targs15 = pd.read_excel("clean chicago.xlsx", sheetname="Target 1-5")
targs67 = pd.read_excel("clean chicago.xlsx", sheetname="Target 6-7")

ind15 = pd.read_excel("clean chicago.xlsx", sheetname="Ind 1-5")
ind67 = pd.read_excel("clean chicago.xlsx", sheetname="Ind 6-7")

prod15 = ind15.merge(targs15, on="Team Name")
