import pandas as pd
import streamlit as st

path = 'C:/Users/night/OneDrive/Documents/Out of the Park Developments/OOTP Baseball 21/saved_games/'

leagues = {
    "SBC": [145,
            '2038-04-04',
            2038,
            'https://raw.githubusercontent.com/EDuBose74/Competitive-Balance/main/SBC/'],
    "PBC": [146,
            '2030-10-28',
            2030,
            path + 'PBC.lg/import_export/csv/'],
    "NBC": [153,
            '2023-04-11',
            2024,
            path + 'NBC.lg/import_export/csv/'],
    "MVP": [153,
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
                                                      (team_history_financials['league_id'] == leagues['SBC'][
                                                          0])].set_index('team_id')

    temp = pd.merge(team_history, team_history_financials, how='left', left_index=True, right_index=True)

    comp_bal = pd.DataFrame()
    comp_bal['Team'] = temp['name'] + ' ' + temp['nickname']
    comp_bal['Total Revenue'] = temp['gate_revenue'] + \
                                temp['season_ticket_revenue'] + \
                                temp['media_revenue'] + \
                                temp['merchandising_revenue'] + \
                                temp['playoff_revenue']
    comp_bal['Media Revenue'] = temp['media_revenue']
    comp_bal['Media Revenue %'] = round((comp_bal['Media Revenue'] / comp_bal['Total Revenue']) * 100, 1)
    comp_bal['Other Revenue %'] = 100 - comp_bal['Media Revenue %']
    comp_bal['Market Size'] = temp['market']
    comp_bal['Playoffs'] = temp['made_playoffs']

    return comp_bal


sbc_comp_bal = comp_balance('SBC')
sbc_comp_bal = sbc_comp_bal[sbc_comp_bal['Playoffs'] == 0]

revenue = sbc_comp_bal[['Team', 'Total Revenue', 'Market Size']].sort_values('Total Revenue', ascending=True).head(
    10).set_index(
    'Team')
revenue['Revenue Balls'] = [25, 20, 15, 10, 8, 7, 6, 4, 3, 2]

market = sbc_comp_bal[['Team', 'Total Revenue', 'Market Size']].sort_values('Market Size', ascending=True).head(
    10).set_index('Team')
market['Market Balls'] = [25, 20, 15, 10, 8, 7, 6, 4, 3, 2]

# lottery = revenue[['Revenue Balls']].merge(market[['Market Balls']], how='outer', left_index=True,
#                                            right_index=True).fillna(0)

lottery = pd.concat([revenue, market]).fillna(0).groupby(
    by=['Team', 'Total Revenue', 'Market Size']).sum().reset_index().set_index('Team')
lottery['Total Balls'] = lottery['Revenue Balls'] + lottery['Market Balls']
lottery.sort_values('Total Balls', ascending=False, inplace=True)

# st.set_page_config(layout="wide")
st.title("SBC Comp Balance Eligibility")

# col1, col2 = st.beta_columns((1, 1))
#
# with col1:
#     st.header("Revenue Eligible")
#     st.write("Revenue Based Eligibility. Playoff Teams are removed.")
#     st.dataframe(revenue.style.format({'Total Revenue': "{:,}"}))
#
# with col2:
#     st.header("Market Eligible")
#     st.write("Market Based Eligibility. Playoff Teams are removed.")
#     st.dataframe(market)

st.header("Total Balls")
st.write("Total Lottery Balls for each team. If 0 in a category, then a team is not eligible. Click the column to sort.")
st.dataframe(lottery.style.format({'Total Revenue': "{:,}",
                                   'Revenue Balls': "{:,.0f}",
                                   'Market Balls': "{:,.0f}",
                                   'Total Balls': "{:,.0f}"
                                   }), height = 768)
