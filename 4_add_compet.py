import pandas as pd

season = "2122"

df = pd.read_csv("all_races_2122.csv")

def compet_name(t):
    if pd.isna(t) or t == "":
        return None
    if "SWRLCP" in str(t):
        return "world_cup"
    elif "SWRLOG__" in str(t):
        return "world_championship"
    else:
        return None
    
df["compet_name"] = df["RaceId"].apply(compet_name)

df.to_csv(f"all_races_{season}.csv", index=False)
