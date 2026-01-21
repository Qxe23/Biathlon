import pandas as pd

df_race = pd.read_csv("all_races_2122.csv")

season = "2122"

def race_name(t):
    parts = str(t).split()

    if len(parts) < 3:
        return None

    race_name = " ".join(parts[2:]).replace(" ", "")

    return race_name

df_race["race_name"] = df_race["RaceName"].apply(race_name)


df_race = df_race.drop(columns=[
    "RaceName", 
])

df_race.to_csv(f"all_races_{season}.csv", index=False)