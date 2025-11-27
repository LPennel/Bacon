import pandas as pd
from ast import literal_eval

# Load the mock data into DataFrames
df_titles = pd.read_csv("Titles.csv", sep=",")
df_actors = pd.read_csv("actors.csv", sep=",")
print("Ran")

## Filters titles based on if they were movies
df_movies = df_titles[df_titles["titleType"] == "movie"].copy()

## Filter people based on if they had the actor or actress role
df_actors_only = df_actors[
    df_actors["primaryProfession"].str.contains("actor|actress", na=False)
].copy()
print("Ran2")

## Spliting the know for titles based on the ,
df_actors_only["knownForTitles"] = df_actors_only["knownForTitles"].str.split(",")

## Seperating titles into different columns for each actor for easier merging
df_exploded_actors = df_actors_only.explode("knownForTitles").rename(
    columns={"knownForTitles": "tconst"}
)
print("Ran3")
df_exploded_actors = df_exploded_actors.reset_index(drop=True)

## Merging actor and movie dataframes
df_final_result = pd.merge(
    df_exploded_actors,
    df_movies[["tconst", "primaryTitle"]],
    on="tconst",
    how="inner",  # Only keep matches where the title ID exists in both filtered sets
)
print("Ran4")

## Recombining an actors multiple rows into one row
df_final = df_final_result.groupby("primaryName")["primaryTitle"].agg(
    list
)  ## If old output need remove line

df_final = df_final.to_frame().reset_index()
print("Ran5")

df_final["primaryTitle"] = df_final["primaryTitle"].apply(
    lambda x: literal_eval(x) if isinstance(x, str) else x
)
df_tempp = df_final["primaryTitle"].dtype
print("Ran6")

# Make dataframe into CSV
df_final.to_csv("Filtered_Actor-Movie.csv", index=False)
