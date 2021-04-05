import pandas as pd
import streamlit as st
import altair as alt

from settings import *

#################################################################
### To run in streamlit use command "streamlit run watson.py" ###
#################################################################

# Import massaged data
df = pd.read_csv('data_modified.csv', index_col='playerId')
df = df.round(0)

# Create draft results data frame
results_df = pd.read_csv('draft_results.csv', index_col='round')

# Mark drafted players
# for index, row in results_df.iterrows():
#     st.sidebar.write(results_df.at[index, 'playerId'])
#     st.sidebar.write(df)
#     #st.sidebar.write(df['playerIds'])
#     if results_df.at[index, 'playerId'] in df:
#         df.at[index, 'status'] = "Drafted"

## Draw sidebar
col1, col2 = st.sidebar.beta_columns([1, 3])
col1.image('terminator.png', width = 55)
menu_selection = col2.radio('Menu:', ('Players', 'Teams'))


playerIds = df.index.values.tolist()
players = df['player'].tolist()
playerDic = dict(zip(playerIds, players))
player_choice = st.sidebar.selectbox('Choose a player:', playerIds, format_func=lambda x: playerDic[x])

st.sidebar.write(df.at[player_choice, 'team'] + " / " + df.at[player_choice, 'position'])
st.sidebar.write(df.at[player_choice, 'status'])
st.sidebar.text_area("Player notes")
st.sidebar.write("FPTs: " + str(int(df.at[player_choice, 'fpts'])))
st.sidebar.write("VAB: " + str(int(df.at[player_choice, 'vab'])))
st.sidebar.write("<b>>> Price target: $" + str(df.at[player_choice, 'price']) + "</b>", unsafe_allow_html=True)
st.sidebar.write("")

drafter = st.sidebar.selectbox("Choose a manager:", managers)
auction_price = st.sidebar.number_input("Enter price:", min_value=1, max_value=200)

if st.sidebar.button("Submit Draft Pick"):
    results_df.loc[len(results_df.index)] = [player_choice, df.at[player_choice, 'player'], df.at[player_choice, 'team'], df.at[player_choice, 'position'], df.at[player_choice, 'fpts'], df.at[player_choice, 'vab'], df.at[player_choice, 'price'], auction_price, drafter]
    results_df.to_csv('draft_results.csv')


st.sidebar.write("")
st.sidebar.write("")
expander = st.sidebar.beta_expander("Adjust settings")
if expander.button("Reset Draft"):
    results_df = pd.read_csv('blank_draft_results.csv', index_col='round')
    results_df.to_csv('draft_results.csv')

## Draw Main Page
if menu_selection == 'Players':

    undrafted_only = st.checkbox('Undrafted players only', value=True)

    positions = {
        "QB": 0,
        "RB": 1,
        "WR": 2,
        "TE": 3,
        "DST": 4
    }

    position_choice = st.selectbox("Position to view:", list(positions.keys()), index=positions[df.at[player_choice, 'position']])

    df = df[df.position == position_choice]
    df = df.sort_values('fpts', ascending=False)

    st.dataframe(df[['player', 'team', 'position', 'fpts', 'vab', 'price', 'status']])

    newdf = df[df.vab > 0]

    source = pd.DataFrame({
        'x': newdf['position'],
        'y': newdf['vab'],
        'label': newdf['player']
    })

    points = alt.Chart(source).mark_point().encode(
        x='x:N',
        y='y:Q'
    )

    text = points.mark_text(
        align='left',
        baseline='middle',
        dx=7,
        color='white'
    ).encode(
        text = 'label'
    )

    st.altair_chart(points + text, use_container_width=True)
elif menu_selection == 'Teams':
    st.dataframe(results_df)