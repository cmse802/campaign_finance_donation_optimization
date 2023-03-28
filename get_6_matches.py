import pandas as pd
import numpy as np


def get_scores(user_position, df):
    # Inputs:
    # User Positions - iterable length 5 of user's positions
    # positions - pandas dataframe containing columns 
    #           "gun_control", "healthcare","abortion", 'climate_change', 'immigration_daca'
    #
    # return: np array of how close each candidate is to user's position
    
    # Convert to numpy
    position_array = df[["gun_control", "healthcare","abortion", 'climate_change', 'immigration_daca']].to_numpy()
    # sets NA to 0, positions to 1 or -1
    position_array[position_array == 0] = -2
    position_array[position_array == -1] = 0
    position_array[position_array == -2] = -1
    
    # make array with same shape as position array, with user's positions
    p = np.array(user_position)
    p = np.expand_dims(p,0)
    tile = np.tile(p, (len(position_array),1))
    scores = abs((tile - position_array))
    sums = 10-np.sum(scores, 1)
    filter_vals = np.unique(np.sort(sums)[0:6])
    
    return sums

def get_top_6(user_preferences):
    
    finance_data = "538_FEC_Won_Opponent_Combined_Dataset.csv"
    position_data = "files/top100_top5.csv"
    save_as = "filter_results.csv"
    
    df = pd.read_csv(finance_data)
    positions = pd.read_csv(position_data)
    df.index = list(df["Unnamed: 0"])
    # Setting the "Universal Index"
    positions.index = ["-".join([positions["district"].iloc[i], positions["party"].iloc[i]]) for i in range(len(positions))]
    positions.head()
    positions = positions.join(df, rsuffix="_")
    sums = get_scores(user_preferences, positions)
    positions["score"] = sums

    top_6 = positions.sort_values(by = ["score", "tipping"], ascending = False)[["name_", "score", "tipping", "district", "party"]].iloc[0:6].reset_index(drop = True)
    top_6.to_csv(save_as)
    
get_top_6([0,1,1,-1,1])