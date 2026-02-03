# clean.py
import pandas as pd

seasons = ["1617", "1718", "1819", "1920", "2021", "2122", "2223", "2324"]

# ---------------------- LOAD RAW DATA ----------------------
def load_raw(season):
    df = pd.read_csv(f"data/raw/all_races_{season}.csv")
    return df

# ---------------------- TIME UTILS ----------------------
def time_to_seconds(t):
    """Convert biathlon time format to seconds."""
    if pd.isna(t) or t == "":
        return pd.NA
    
    t = str(t).replace("+", "").strip()

    # Already in seconds
    if ":" not in t:
        return float(t)
    
    parts = t.split(":")

    if len(parts) == 3:  # hh:mm:ss
        h, m, s = parts
        return int(h) * 3600 + int(m) * 60 + float(s)
    
    if len(parts) == 2:  # mm:ss
        m, s = parts
        return int(m) * 60 + float(s)

    return pd.NA

def convert_time_columns(df):
    """Convert all time columns to seconds"""
    time_cols = [
        "TotalTime", "Behind",
        "TotalTime_shooting", "Behind_shooting",
        "TotalTime_range", "Behind_range",
        "TotalTime_ski", "Behind_ski"
    ]

    for col in time_cols:
        df[col + "_seconds"] = df[col].apply(time_to_seconds)

    df = df.drop(columns=time_cols)
    return df


# ---------------------- SHOOTING PARSING ----------------------
def separate_shootings(row):
    prone1 = prone2 = stand1 = stand2 = prone = stand = None
    t = row["Shootings"]
    race_name = row["RaceName"]

    if pd.isna(t) or t == "":
        return prone1, prone2, stand1, stand2, prone, stand
    
    parts = str(t).split("+")

    # Sprint(2 shootings: prone, stand)
    if "Sprint" in race_name:
        prone1 = prone = int(parts[0]) if len(parts) > 0 else None
        stand1 = stand = int(parts[1]) if len(parts) > 1 else None
        return prone1, prone2, stand1, stand2, prone, stand
    
    # Individual (4 shootings: prone, stand, prone, stand)
    if "Individual" in race_name:
        prone1 = int(parts[0]) if len(parts) > 0 else None
        stand1 = int(parts[1]) if len(parts) > 1 else None
        prone2 = int(parts[2]) if len(parts) > 2 else None
        stand2 = int(parts[3]) if len(parts) > 3 else None
        prone = (prone1 or 0) + (prone2 or 0)
        stand = (stand1 or 0) + (stand2 or 0)
        return prone1, prone2, stand1, stand2, prone, stand
    
    # Pursuit / Mass Start (4 shootings: prone, prone, stand, stand)
    if "Pursuit" in race_name or "Mass Start" in race_name:
        prone1 = int(parts[0]) if len(parts) > 0 else None
        prone2 = int(parts[1]) if len(parts) > 1 else None
        stand1 = int(parts[2]) if len(parts) > 2 else None
        stand2 = int(parts[3]) if len(parts) > 3 else None
        prone = (prone1 or 0) + (prone2 or 0)
        stand = (stand1 or 0) + (stand2 or 0)
        return prone1, prone2, stand1, stand2, prone, stand
    
    return prone1, prone2, stand1, stand2, prone, stand


def add_shooting_columns(df):
    cols = [
        "prone_shooting1", "prone_shooting2",
        "standing_shooting1", "standing_shooting2",
        "prone_shooting", "standing_shooting"
    ]

    df[cols] = df.apply(separate_shootings, axis=1).apply(pd.Series)
    return df


# ---------------------- ACCURACY ----------------------
def add_accuracy_features(df):
    for col in ["prone_shooting1", "prone_shooting2", "standing_shooting1", "standing_shooting2"]:
        df["accuracy_" + col] = (5 - df[col]) * 100 / 5

    df["accuracy_prone"] = df[["accuracy_prone_shooting1", "accuracy_prone_shooting2"]].mean(axis=1, skipna=True)
    df["accuracy_standing"] = df[["accuracy_standing_shooting1", "accuracy_standing_shooting2"]].mean(axis=1, skipna=True)
    df["accuracy_total"] = df[["accuracy_prone", "accuracy_standing"]].mean(axis=1, skipna=True)

    return df


# ---------------------- RACE NAME ----------------------
def extract_race_name(t):
    parts = str(t).split()
    return " ".join(parts[2:]).replace(" ", "") if len(parts) >= 3 else None

def add_race_name(df):
    df["race_name"] = df["RaceName"].apply(extract_race_name)
    return df



# ---------------------- COMPETITION NAME ----------------------
def compet_name(race_id):
    if pd.isna(race_id):
        return None
    if "SWRLCP" in str(race_id):
        return "world_cup"
    if "SWRLOG__" in str(race_id):
        return "world_championship"
    return None


def add_competition_name(df):
    df["compet_name"] = df["RaceId"].apply(compet_name)
    return df


# ---------------------- TIME PERFORMANCE VS MEDIAN ----------------------
def time_perf_vs_median(df):
    # Compute median ski time per race
    median_ski = df.groupby("RaceId")["TotalTime_ski_seconds"].transform("median")
    median_range = df.groupby("RaceId")["TotalTime_range_seconds"].transform("median")
    median_shooting = df.groupby("RaceId")["TotalTime_shooting_seconds"].transform("median")

    # Percentage difference vs median
    df["ski_vs_median_pct"] = (df["TotalTime_ski_seconds"] - median_ski) / median_ski * 100
    df["range_vs_median_pct"] = (df["TotalTime_range_seconds"] - median_range) / median_range * 100
    df["shooting_vs_median_pct"] = (df["TotalTime_shooting_seconds"] - median_shooting) / median_shooting * 100
    
    return df


# ---------------------- MAIN CLEAN PIPELINE ----------------------
def clean_dataframe(df):
    """Main cleaning pipeline"""

    # Remove DNF/DNS/etc
    df = df[~df["IRM"].isin(["DNF", "DNS", "DSQ", "LAP"])].copy()

    # Convert time columns
    df = convert_time_columns(df)

    # Shooting parsing
    df = add_shooting_columns(df)

    # Accuracy features
    df = add_accuracy_features(df)

    # Race name 
    df = add_race_name(df)

    # Competition name
    df = add_competition_name(df)

    # Time performance vs median
    df = time_perf_vs_median(df)

    # Drop unused columns
    df = df.drop(columns=["RaceName"], errors="ignore")

    return df


# ---------------------- SAVE PROCESSED DATA  ----------------------
def save_processed(df, season):
    df.to_csv(f"data/processed/all_races_{season}_cleaned.csv", index=False)

# ---------------------- MAIN  ----------------------
def main():
    for season in seasons:
        print(f"Load season {season}")
        df = load_raw(season)
        df = clean_dataframe(df)
        save_processed(df, season)
        print(f"✓ {season} season cleaning complete")


if __name__ == '__main__':
    main()