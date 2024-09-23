# $ git init <path/to/dir>

import pandas as pd
import math

def create_square_df(lst, n=None):
    # If n is None, calculate n as the smallest integer for a square (n^2 >= len(lst))
    if n is None:
        n = math.ceil(math.sqrt(len(lst)))
    
    # Calculate how many rows we need, given n columns
    num_rows = math.ceil(len(lst) / n)
    
    # Pad the list if necessary to make it fit into a full rectangular shape
    padded_list = lst + [''] * (num_rows * n - len(lst))
    
    # Reshape the 1D list into a 2D list (num_rows x n)
    reshaped_matrix = [padded_list[i:i + n] for i in range(0, len(padded_list), n)]
    
    # Create the DataFrame
    df = pd.DataFrame(reshaped_matrix)
    
    return df

def get_diff(diff_index):
# 	chs = {"ACDMRT"}
	modes = "ACDMRT"
	chs = {f'{x}_{y}':[] for y in "ab" for x in "ACDMRT"}
	
	for ch in modes:
		for diff_item in diff_index.iter_change_type(ch):
			cha = diff_item.a_blob.data_stream.read().decode('utf-8')
			chb = diff_item.b_blob.data_stream.read().decode('utf-8')
			chs[f'{ch}_a'].append(cha)
			chs[f'{ch}_b'].append(chb)
	
	return chs

csd = create_square_df