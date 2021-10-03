
from datetime import datetime
import pandas as pd
import altair as alt
import re

dateparse = lambda x: datetime.fromisoformat(x).strftime('%Y-%m-%d') # Custom date parser
df=pd.read_csv("raw_data/project_a.csv",
 parse_dates=["dateOfInvestment"],
  date_parser=dateparse)
df.founded=df.founded.apply(lambda x: x[-4:] if len(x)>4 else x) # Cleaning the founded column
for x in ["management", "location"]:
  df[x]=df[x].apply(lambda x: x.replace("\n", " ")) # Cleaning some text
df["countries"]=df["location"].apply(lambda x: ", "\
    .join(set([s.replace(")", "") for s in re.findall(r"\w+ ?\w+\)", x)])) if "(" in x else x) # Getting the countries from locations
df["Active"]=df["status"].apply(lambda x:1 if x=="Active" else 0) # Counting Active in portfolio
df["Exited"]=df["status"].apply(lambda x:0 if x=="Active" else 1) # Counting Exited in portfolio
df["YearOfInvestment"]=df["dateOfInvestment"].apply(lambda x: x.strftime('%Y')) # Converting funded date in year

for x in df.columns:
  if x not in ["Description","headline","management","website","id", "exit","subheadline", "venture"]:
    print(df[x].value_counts(), "\n") # Print the more interesting relationships
df_cumsum=df.groupby(["YearOfInvestment",'countries']).agg({"Active":"sum", "Exited":"sum"})\
    .groupby(level=1).cumsum().reset_index().copy() # Creating cumulative sum data for graph
df_cumsum["total"]=df_cumsum["Active"]+df_cumsum["Exited"] # Creating a column of total cumsum companies in portfolio
df_cumsum["Exited_neg"]=-df_cumsum["Exited"] # For ploting purposes but not being used
# Altair Stream Graph with legend interaction
source = df_cumsum
selection = alt.selection_multi(fields=['countries'], bind='legend')
alt.Chart(source).mark_area().encode(
    alt.X('YearOfInvestment',
        axis=alt.Axis( domain=False, tickSize=0)
    ),
    alt.Y('Active', stack='zero', axis=None), # Can be changed to total or Exited
    alt.Color("countries",
        scale=alt.Scale(scheme='accent')),
    opacity=alt.condition(selection, alt.value(1), alt.value(0.2))
).add_selection(
    selection).properties(
    width=1000,
    height=400
)