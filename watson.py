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

## Draw sidebar

col1, col2 = st.sidebar.beta_columns(2)
with col1:
    st.sidebar.image('terminator.png', width = 55)

with col2:
    menu_selection = st.sidebar.radio('Menu:', ('Players', 'Teams'))


playerIds = df.index.values.tolist()
players = df['player'].tolist()
playerDic = dict(zip(playerIds, players))
player_choice = st.sidebar.selectbox('Choose a player:', playerIds, format_func=lambda x: playerDic[x])

st.sidebar.write("Team: " + df.at[player_choice, 'team'])
st.sidebar.write("Position: " + df.at[player_choice, 'position'])
st.sidebar.write("Position rank: ")
st.sidebar.write("FPTs: " + str(int(df.at[player_choice, 'fpts'])))
st.sidebar.write("VAB: " + str(int(df.at[player_choice, 'vab'])))
st.sidebar.write("<b>>> Price target: $" + str(df.at[player_choice, 'price']) + "</b>", unsafe_allow_html=True)
st.sidebar.write("")

drafter = st.sidebar.selectbox("Choose a manager:", managers)
auction_price = st.sidebar.number_input("Enter price:", min_value=1, max_value=200)

if st.sidebar.button("Submit Draft Pick"):
    results_df.loc[len(results_df.index)] = [player_choice, df.at[player_choice, 'player'], df.at[player_choice, 'team'], df.at[player_choice, 'position'], df.at[player_choice, 'fpts'], df.at[player_choice, 'vab'], df.at[player_choice, 'price'], auction_price, drafter]
    results_df.to_csv('draft_results.csv')


with st.sidebar.beta_expander("Adjust settings"):
    st.write("Test")
    if st.sidebar.button("Reset Draft"):
        results_df = results_df[df.round == 0]
        results_df.to_csv('draft_results.csv')

## Draw Main Page

if menu_selection == 'Players':
    positions = df['position'].unique()
    position_choice = st.selectbox("Position to view:", positions)

    df = df[df.position == position_choice]
    df = df.sort_values('fpts', ascending=False)

    st.dataframe(df[['player', 'team', 'position', 'fpts', 'vab', 'price']])

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