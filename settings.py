
# Manager settings
managers = [
    "Tom",
    "Tommy",
    "Brad",
    "Charlie",
    "Mike",
    "Andy",
    "Doug",
    "Eric",
    "Craig",
    "Dave",
    "Julien",
    "Matt"
]

# Draft settings
draft_budget = 200

# Roser settings
roster_size = 14
roster_qb = 1
roster_rb = 1
roster_wr = 2
roster_te = 1
roster_flex = 2
roster_dst = 1
roster_bench = 6

# Baseline settings
baseline_dict = {
    "QB": 6,
    "RB": 35,
    "WR": 40,
    "TE": 10,
    "DST": 5
}

# Calculated variables
players_drafted = len(managers) * roster_size
total_spend = len(managers) * draft_budget
baseline_players = roster_bench * len(managers)
baseline_spend = baseline_players * 1
roster_size = sum([roster_qb, roster_rb, roster_wr, roster_te, roster_flex, roster_dst, roster_bench])
spend_above_baseline = total_spend - baseline_spend


# League scoring system
# Passing
score_py = 0.04
score_td_pass = 4
score_int = -2
score_2pt_pass = 2

# Rushing
score_ry = 0.1
score_td_run = 6

# Receiving
score_rey = 0.1
score_rec = 1
score_td_rec = 6

# DST
score_dst_td = 6
score_sack = 1.5
score_block = 2
score_int = 3
score_fr = 3
score_sf = 2

# Misc scoring
score_fumble = -3
score_2pt = 2

### ADD POINTS ALLOWED??????????