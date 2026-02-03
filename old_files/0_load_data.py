import biathlonresults
from biathlonresults import analytic_results, events, results, consts
import pandas as pd
from tqdm import tqdm



seasons = ["1617", "1718", "1819", "1920", "2021", "2122", "2223", "2324", "2425"]

for season in tqdm(seasons, desc="Season"):

    all_results = []
    events = biathlonresults.events(season, level=biathlonresults.consts.LevelType.BMW_IBU_WC)

    for event in tqdm(events, desc="Events"):
        event_id = event["EventId"]

        races = biathlonresults.competitions(event_id)

        for race in tqdm(races, desc=f"Races ({event['ShortDescription']})", leave=False):
            if "Relay" in race["ShortDescription"]:
                continue 

            race_id = race["RaceId"]

            try:
                race_data = results(race_id=race_id)

                df_race = pd.DataFrame(race_data["Results"])

                shooting_analytics = analytic_results(race_id, type_id=consts.AnalysisType.TOTAL_SHOOTING_TIME)
                range_analytics = analytic_results(race_id, type_id=consts.AnalysisType.TOTAL_RANGE_TIME)
                ski_analytics = analytic_results(race_id, type_id=consts.AnalysisType.TOTAL_COURSE_TIME)

                df_shooting = pd.DataFrame(shooting_analytics["Results"])
                df_range = pd.DataFrame(range_analytics["Results"])
                df_ski = pd.DataFrame(ski_analytics["Results"])

                df_shooting = df_shooting[["IBUId", "ResultOrder", "TotalTime", "Behind"]].rename(columns={"ResultOrder": "ResultOrder_shooting", "TotalTime": "TotalTime_shooting", "Behind": "Behind_shooting"})
                df_range = df_range[["IBUId", "ResultOrder", "TotalTime", "Behind"]].rename(columns={"ResultOrder": "ResultOrder_range", "TotalTime": "TotalTime_range", "Behind": "Behind_range"})
                df_ski = df_ski[["IBUId", "ResultOrder", "TotalTime", "Behind"]].rename(columns={"ResultOrder": "ResultOrder_ski", "TotalTime": "TotalTime_ski", "Behind": "Behind_ski"})

                df_race = df_race.merge(df_shooting, on="IBUId", how="left")
                df_race = df_race.merge(df_range, on="IBUId", how="left")
                df_race = df_race.merge(df_ski, on="IBUId", how="left")

                df_race["RaceId"] = race_id
                df_race["EventId"] = event_id
                df_race["EventName"] = event["ShortDescription"]
                df_race["RaceName"] = race["ShortDescription"]
                df_race["RaceDate"] = race["StartTime"][:10]
                df_race["Season"] = season
                df_race["Genre"] = df_race["RaceId"].str[-4:-2].map({
                    "SW": "Female",
                    "SM": "Male"
                })

                cols_to_keep = ["Rank", "IRM", "IBUId", "Name", 'Nat', "Shootings", "ShootingTotal",
                                "TotalTime", 'WC', 'NC', "BibColor", "Behind", "PursuitStartDistance", 
                                'ResultOrder_shooting', 'TotalTime_shooting', 'Behind_shooting',
                                'ResultOrder_range', 'TotalTime_range', 'Behind_range', 'ResultOrder_ski', 
                                'TotalTime_ski', 'Behind_ski', 'RaceId', 'EventId', 'EventName', 'RaceName', 
                                'RaceDate', 'Season', "Genre"]
                
                df_race = df_race[cols_to_keep]
                all_results.append(df_race)

            except Exception as e:
                print(f"Erreur pour la course {race_id} :", e)

    df_all = pd.concat(all_results, ignore_index=True)

    print(df_all.shape)
    df_all.to_csv(f"all_races_{season}.csv", index=False)
