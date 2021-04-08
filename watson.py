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
for index, row in results_df.iterrows():
    df.at[int(row['playerId']), 'status'] = "Drafted"

## Try to rank positionally
# df = df.sort_values(['fpts'], ascending=False)
# tmp = df.groupby('position').size()
# rank = tmp.map(range)
# rank =[item for sublist in rank for item in sublist]
# df['rank'] = rank
# st.write(df)


## Draw sidebar

# Logo and navigation menu
col1, col2 = st.sidebar.beta_columns([1, 3])
col1.image('terminator.png', width = 55)
menu_selection = col2.radio('Menu:', ('Players', 'Draft Results'))

# Round display
st.sidebar.title("Round " + str((len(results_df) + 1)))

# Do some maneuveering to draw select box showing names but returning IDs
playerIds = df.index.values.tolist()
players = df['player'].tolist()
playerDic = dict(zip(playerIds, players))
player_choice = st.sidebar.selectbox('Choose a player:', playerIds, format_func=lambda x: playerDic[x])

# Create the drafting form if selected player is undrafted
if df.at[player_choice, 'status'] == "Undrafted":
    drafter = st.sidebar.selectbox("Choose a manager:", managers)
    auction_price = st.sidebar.number_input("Enter price:", min_value=1, max_value=200)

    if st.sidebar.button("Submit Draft Pick"):
        results_df.loc[len(results_df.index)] = [player_choice, df.at[player_choice, 'player'], df.at[player_choice, 'team'], df.at[player_choice, 'position'], df.at[player_choice, 'fpts'], df.at[player_choice, 'vab'], df.at[player_choice, 'price'], auction_price, drafter]
        results_df.to_csv('draft_results.csv')

# Show some data about the selected player
st.sidebar.write("<b>" + df.at[player_choice, 'status'] + "</b>", unsafe_allow_html=True)
st.sidebar.write(df.at[player_choice, 'team'] + " / " + df.at[player_choice, 'position'])
st.sidebar.text_area("Player notes")
st.sidebar.write("FPTs: " + str(int(df.at[player_choice, 'fpts'])))
st.sidebar.write("VAB: " + str(int(df.at[player_choice, 'vab'])))
st.sidebar.write("<b>>> Price target: $" + str(df.at[player_choice, 'price']) + "</b>", unsafe_allow_html=True)
st.sidebar.write("")





# Settings expander
expander = st.sidebar.beta_expander("Settings")
expander.write("This will completely erase the draft results. Don't fuck it up!")
if expander.button("Reset Draft"):
    results_df = pd.read_csv('blank_draft_results.csv', index_col='round')
    results_df.to_csv('draft_results.csv')

## Draw Main Page

st.title(df.at[player_choice, 'player'])
st.header("$" + str(df.at[player_choice, 'price']))

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

    if undrafted_only:
        st.dataframe(df[['player', 'team', 'position', 'fpts', 'vab', 'price', 'status']][df.status == 'Undrafted'])
    else:
        st.dataframe(df[['player', 'team', 'position', 'fpts', 'vab', 'price', 'status']])

    # Draw scatter plot of players above baseline
    newdf = df[df.vab > 0]
    # newdf = newdf[df.status == 'Undrafted']

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
elif menu_selection == 'Draft Results':
    results_df.index += 1
    st.dataframe(results_df[['player', 'position', 'fpts', 'vab','drafter', 'auctionPrice']])