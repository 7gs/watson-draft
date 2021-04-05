import pandas as pd

from settings import *

def getBaseline(df, position):

    df = df[df.position == position]
    df = df.sort_values('fpts', ascending=False)
    df = df.reset_index()   

    baseline = df.at[baseline_dict[position], 'fpts']

    return baseline

# Import raw data as a Pandas dataframe and set NAs to 0
df = pd.read_csv('rawdata.csv', index_col='playerId')
df = df.fillna(0)

# Remove positions we don't care about
positions_to_dump = ['DL', 'K', 'DB', 'LB']
for position in positions_to_dump:
    df = df[df.position != position]

# Calculate FPTs as new column
################# NOT CALCULATING QB FPTS CORRECTLY!!! #####################################
df['fpts'] = (df['dstBlk'] * score_block) + (df['dstFumlRec'] * score_fr) + (df['dstInt'] * score_int) + (df['dstRetTd'] * score_dst_td) + (df['dstSack'] * score_sack) + (df['dstSafety'] * score_sf) + (df['dstTd'] * score_dst_td) + (df['fumbles'] * score_fumble) + (df['passInt'] * score_int) + (df['passTds'] * score_td_pass) + (df['passYds'] * score_py) + (df['rec'] * score_rec) + (df['recTds'] * score_td_rec) + (df['recYds'] * score_rey) + (df['rushTds'] * score_td_run) + (df['rushYds'] * score_ry) + (df['twoPts'] * score_2pt)

# Calculate VAB as new column
baseline_fpts_dict = {
    "QB": getBaseline(df, "QB"),
    "RB": getBaseline(df, "RB"),
    "WR": getBaseline(df, "WR"),
    "TE": getBaseline(df, "TE"),
    "DST": getBaseline(df, "DST")
}

# Create VAB column set it to fpts initially
df['vab'] = df['fpts']

# Calculate VAB for all players
for index, row in df.iterrows():
    
    if row['position'] == 'QB':
        df.at[index, 'vab'] -= baseline_fpts_dict['QB']
    elif row['position'] == 'RB':
        df.at[index, 'vab'] -= baseline_fpts_dict['RB']
    elif row['position'] == 'WR':
        df.at[index, 'vab'] -= baseline_fpts_dict['WR']
    elif row['position'] == 'TE':
        df.at[index, 'vab'] -= baseline_fpts_dict['TE']
    elif row['position'] == 'DST':
        df.at[index, 'vab'] -= baseline_fpts_dict['DST']

# Set VABs to 0 if they are less than 0
for index, row in df.iterrows():
    if row['vab'] < 0:
        df.at[index, 'vab'] = 0

# Create price column
df['price'] = 0

# Calculate VAB multiplier
total_vab = df['vab'].sum()
vab_multiplier = spend_above_baseline / total_vab

# Calculate price targets for each player
for index, row in df.iterrows():
    df.at[index, 'price'] = int(row['vab'] * vab_multiplier)

# Create status column
df['status'] = "Undrafted"

df.to_csv('data_modified.csv')