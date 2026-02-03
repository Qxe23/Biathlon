import biathlonresults
from biathlonresults import analytic_results, events, results, consts
import pandas as pd
import argparse
from tqdm import tqdm

season = "1617"
level=biathlonresults.consts.LevelType.BMW_IBU_WC

# ------------------ ARGUMENTS ------------------
def parse_args():
    parser = argparse.ArgumentParser(
        description='Build season stats from regular season data'
    )
    parser.add_argument('--season', type=str, default=season)
    parser.add_argument('--out', type=str, default=f'data/raw/all_races_{season}.csv')
    return parser.parse_args()



# ------------------ EVENTS ------------------
def get_events(season, level):
    """
    Docstring for get_event_id_of_season
    
    :param season: id of the season ex:2425
    :param level: World Cup/Ibu Cup...
    """
    print(f"Getting events for season {season}")
    return biathlonresults.events(season, level=level)


# ------------------ RACES ------------------
def get_races(events):
    print(f"Getting races id for season {season}")
    all_races = []
    for event in events:
        event_id = event["EventId"]
        for race in biathlonresults.competitions(event_id):
            if "Relay" in race["ShortDescription"]:
                continue
            all_races.append((event, race))
    return all_races

# ------------------ FETCH RACE DATA ------------------
def fetch_race_data(event, race, season):
    race_id = race["RaceId"]
    event_id = event["EventId"]

    race_data = results(race_id=race_id)
    df_race = pd.DataFrame(race_data["Results"])

    # Analytics
    def get_analytics(type_id, suffix):
        data = analytic_results(race_id, type_id=type_id)
        df = pd.DataFrame(data["Results"])

        return df[["IBUId", "ResultOrder", "TotalTime", "Behind"]].rename(
            columns={
                "ResultOrder": f"ResultOrder_{suffix}",
                "TotalTime": f"TotalTime_{suffix}",
                "Behind": f"Behind_{suffix}"
            }
        )
    
    df_race = df_race.merge(get_analytics(consts.AnalysisType.TOTAL_SHOOTING_TIME, "shooting"), on="IBUId", how="left")
    df_race = df_race.merge(get_analytics(consts.AnalysisType.TOTAL_RANGE_TIME, "range"), on="IBUId", how="left")
    df_race = df_race.merge(get_analytics(consts.AnalysisType.TOTAL_COURSE_TIME, "ski"), on="IBUId", how="left")

    # Metadata
    df_race["RaceId"] = race_id
    df_race["EventId"] = event_id
    df_race["EventName"] = event["ShortDescription"]
    df_race["RaceName"] = race["ShortDescription"]
    df_race["RaceDate"] = race["StartTime"][:10]
    df_race["Season"] = season
    df_race["Genre"] = df_race["RaceId"].str[-4:-2].map({"SW": "Female", "SM": "Male"})

    return df_race


# ------------------ CLEAN COLUMNS ------------------
def clean_columns(df):
    cols = ["Rank", "IRM", "IBUId", "Name", "Nat", "Shootings", "ShootingTotal",
            "TotalTime", "WC", "NC", "BibColor", "Behind", "PursuitStartDistance",
            "ResultOrder_shooting", "TotalTime_shooting", "Behind_shooting",
            "ResultOrder_range", "TotalTime_range", "Behind_range",
            "ResultOrder_ski", "TotalTime_ski", "Behind_ski",
            "RaceId", "EventId", "EventName", "RaceName", "RaceDate", "Season", "Genre"]
    
    return df[cols]


# ------------------ MAIN ------------------
def main():
    args = parse_args()
    season = args.season
    level = biathlonresults.consts.LevelType.BMW_IBU_WC

    events = get_events(season, level)
    races = get_races(events)

    all_results = []
    for event, race in tqdm(races, desc="Races"):
        try:
            df = fetch_race_data(event, race, season)
            all_results.append(df)
        except Exception as e:
            print(f"\nError race {race['RaceId']}:", e)

    df_all = pd.concat(all_results, ignore_index=True)
    df_all = clean_columns(df_all)

    df_all.to_csv(args.out, index=False)
    print(f"Saved {df_all.shape} to {args.out}")


if __name__ == '__main__':
    main()