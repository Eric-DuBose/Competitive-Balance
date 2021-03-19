import pandas as pd
import streamlit as st


path = 'C:/Users/night/OneDrive/Documents/Out of the Park Developments/OOTP Baseball 21/saved_games/'

leagues = {
    "SBC":[145, 
           '2038-04-04', 
           2038,
           'https://raw.githubusercontent.com/EDuBose74/Competitive-Balance/main/SBC/'],
    "PBC":[146, 
           '2030-10-28',
           2030,
           path + 'PBC.lg/import_export/csv/'],
    "NBC":[153, 
           '2023-04-11',
           2024,
           path + 'NBC.lg/import_export/csv/'],
    "MVP":[153, 
           '2024-03-28', 
           2024,
           path + 'MVP.lg/import_export/csv/']
}

def comp_balance(league):
    team_history = pd.read_csv(leagues[league][3] + 'team_history.csv')
    team_history_financials = pd.read_csv(leagues[league][3] + 'team_history_financials.csv')
    team_history = team_history[(team_history['year'] == (leagues[league][2] - 1)) & 
                            (team_history['league_id'] == leagues[league][0])].set_index('team_id')

    team_history = team_history[['name', 'nickname', 'made_playoffs']]

    team_history_financials = team_history_financials[(team_history_financials['year'] == (leagues['SBC'][2] - 1)) & 
                            (team_history_financials['league_id'] == leagues['SBC'][0])].set_index('team_id')

    temp = pd.merge(team_history, team_history_financials, how = 'left', left_index = True, right_index = True)
    
    comp_bal = pd.DataFrame()
    comp_bal['Team'] = temp['name'] + ' ' + temp['nickname']
    comp_bal['Total Revenue'] = temp['gate_revenue'] + \
                                temp['season_ticket_revenue'] + \
                                temp['media_revenue'] + \
                                temp['merchandising_revenue'] + \
                                temp['playoff_revenue']
    comp_bal['Media Revenue'] = temp['media_revenue']
    comp_bal['Media Revenue %'] = round((comp_bal['Media Revenue']/comp_bal['Total Revenue'])*100,1)
    comp_bal['Other Revenue %'] = 100 - comp_bal['Media Revenue %']
    comp_bal['Market Size'] = temp['market']
    comp_bal['Playoffs'] = temp['made_playoffs']
    
    return comp_bal
  
sbc_comp_bal = comp_balance('SBC')
st.table(sbc_comp_bal)
