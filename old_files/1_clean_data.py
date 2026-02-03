import pandas as pd

season = "2425"

df = pd.read_csv(f"all_races_{season}.csv")

df = df[df["IRM"] != "DNF"]
df = df[df["IRM"] != "DNS"]
df = df[df["IRM"] != "DSQ"]
df = df[df["IRM"] != "LAP"]

print(df["TotalTime"].isna().sum())

def time_to_seconds(t):
    if pd.isna(t) or t == "":
        return None

    t = str(t).replace("+", "").strip()

    # Cas déjà en secondes ("0.0")
    if ":" not in t:
        return float(t)

    parts = t.split(":")

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


df["TotalTime_seconds"] = df["TotalTime"].apply(time_to_seconds)
df["Behind_seconds"] = df["Behind"].apply(time_to_seconds)
df["TotalTime_shooting_seconds"] = df["TotalTime_shooting"].apply(time_to_seconds)
df["Behind_shooting_seconds"] = df["Behind_shooting"].apply(time_to_seconds)
df["TotalTime_range_seconds"] = df["TotalTime_range"].apply(time_to_seconds)
df["Behind_range_seconds"] = df["Behind_range"].apply(time_to_seconds)
df["TotalTime_ski_seconds"] = df["TotalTime_ski"].apply(time_to_seconds)
df["Behind_ski_seconds"] = df["Behind_ski"].apply(time_to_seconds)

df = df.drop(columns=[
    "TotalTime", 
    "Behind", 
    "TotalTime_shooting", 
    "Behind_shooting",
    "TotalTime_range", 
    "Behind_range",
    "TotalTime_ski",
    "Behind_ski"
])

def separate_shootings(row):
    prone1, prone2, stand1, stand2, prone, stand = None, None, None, None, None, None  
    
    t = row["Shootings"]
    race_name = row["RaceName"]
    
    if pd.isna(t) or t == "":
        return prone1, prone2, stand1, stand2, prone, stand
    
    if "Sprint" in race_name:
        parts = str(t).split("+")
        if len(parts) >= 1:
            prone1 = prone = int(parts[0])
        if len(parts) >= 2:
            stand1 = stand = int(parts[1])
        return prone1, prone2, stand1, stand2
    
    if "Individual" in race_name:
        parts = str(t).split("+")
        if len(parts) >= 1:
            prone1 = prone = int(parts[0])
        if len(parts) >= 2:
            stand1 = stand = int(parts[1])
        if len(parts) >= 3:
            prone2 = int(parts[2])
            prone += prone2
        if len(parts) >= 4:
            stand2 = int(parts[3])
            stand += stand2
        return prone1, prone2, stand1, stand2, prone, stand
    
    if "Pursuit" in race_name or "Mass Start" in race_name:
        parts = str(t).split("+")
        if len(parts) >= 1:
            prone1 = prone = int(parts[0])
        if len(parts) >= 2:
            prone2 = int(parts[1])
            prone += prone2
        if len(parts) >= 3:
            stand1 = stand = int(parts[2])
        if len(parts) >= 4:
            stand2 = int(parts[3])
            stand += stand2
        return prone1, prone2, stand1, stand2, prone, stand


df[[
    "prone_shooting1",
    "prone_shooting2",
    "standing_shooting1",
    "standing_shooting2",
    "prone_shooting",
    "standing_shooting"
]] = df.apply(separate_shootings, axis=1).apply(pd.Series)


df["accuracy_prone1"] = (5 - df["prone_shooting1"]) * 100 / 5
df["accuracy_prone2"] = (5 - df["prone_shooting2"]) * 100 / 5
df["accuracy_standing1"] = (5 - df["standing_shooting1"]) * 100 / 5
df["accuracy_standing2"] = (5 - df["standing_shooting2"]) * 100 / 5

df["accuracy_prone"] = df[["accuracy_prone1", "accuracy_prone2"]].mean(axis=1)
df["accuracy_standing"] = df[["accuracy_standing1", "accuracy_standing2"]].mean(axis=1)
df["accuracy_total"] = df[["accuracy_prone", "accuracy_standing"]].mean(axis=1)


def race_name(t):
    parts = str(t).split()

    if len(parts) < 3:
        return None

    race_name = " ".join(parts[2:]).replace(" ", "")

    return race_name

df["race_name"] = df["RaceName"].apply(race_name)


df = df.drop(columns=[
    "RaceName", 
])

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