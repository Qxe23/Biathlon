import biathlonresults
print(dir(biathlonresults))

from biathlonresults import *
#all_results(ibu_id="BTFRA22810199801") # All races results of the athlete
#analytic_results(race_id="BT2425SWRLCP01SWSI", type_id="")
#athletes(family_name="Simon", given_name="Julia") # Search athlete
#cisbios(ibu_id="BTFRA22810199801") # Get athlete by id
#competitions(event_id="BT2425SWRLCP01") # list of races in stage
#consts()
#cup_results(cup_id="BT1819SWRLCP__SMTS") # Cup results BT1819SWRLCP__SMTS - Men's WC Total 2018/2019 BT1819SWRLCP__SWTS - Women's WC Total 2018/2019
#cups(season_id="1819") # List of Cups season_id: season identifier (1819 for season 2018/2019, get others in a similar way)
#events(season_id="1819") # Events of cup (schedule)
#print(organizers())
#results(race_id="BT2425SWRLCP01SWSI") # Race results
#seasons()
print(stats(statistic_id="WCPOD_M", stat_id="WCPOD", by_what="ATH", gender_id="W", season_id="", organizer_id="", ibu_id="", nat=""))
#StatisticId=WCPOD_M&StatId=WCPOD&byWhat=ATH&SeasonId=&OrganizerId=&GenderId=M&IBUId=&Nat=

