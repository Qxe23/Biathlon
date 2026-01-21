import pandas as pd

df_race = pd.read_csv("all_races_2122.csv")

season = "2122"

def time_to_seconds(t):
    if pd.isna(t) or t == "":
        return None

    t = str(t).replace("+", "").strip()

    # Cas déjà en secondes ("0.0")
    if ":" not in t:
        return float(t)

    parts = t.split(":")

    try:
        # hh:mm:ss
        if len(parts) == 3:
            hours, minutes, seconds = parts
            return int(hours) * 3600 + int(minutes) * 60 + float(seconds)

        # mm:ss
        elif len(parts) == 2:
            minutes, seconds = parts
            return int(minutes) * 60 + float(seconds)

        else:
            return None

    except:
        return None


df_race["TotalTime_seconds"] = df_race["TotalTime"].apply(time_to_seconds)
df_race["Behind_seconds"] = df_race["Behind"].apply(time_to_seconds)
df_race["TotalTime_shooting_seconds"] = df_race["TotalTime_shooting"].apply(time_to_seconds)
df_race["Behind_shooting_seconds"] = df_race["Behind_shooting"].apply(time_to_seconds)
df_race["TotalTime_range_seconds"] = df_race["TotalTime_range"].apply(time_to_seconds)
df_race["Behind_range_seconds"] = df_race["Behind_range"].apply(time_to_seconds)
df_race["TotalTime_ski_seconds"] = df_race["TotalTime_ski"].apply(time_to_seconds)
df_race["Behind_ski_seconds"] = df_race["Behind_ski"].apply(time_to_seconds)

df_race = df_race.drop(columns=[
    "TotalTime", 
    "Behind", 
    "TotalTime_shooting", 
    "Behind_shooting",
    "TotalTime_range", 
    "Behind_range",
    "TotalTime_ski",
    "Behind_ski"
])

df_race.to_csv(f"all_races_{season}.csv", index=False)