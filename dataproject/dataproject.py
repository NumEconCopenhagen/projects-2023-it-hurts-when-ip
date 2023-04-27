import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display
import re



def clean(ets):
    """ cleaning of the original datset ets""" 
    
    ets.rename(columns={'ETS information':'category', 'main activity sector name':'sector'}, inplace=True)
   
    # establish list of rows to drop and handler function
    rows_to_drop = {}
    def add_rows_to_drop(colname, *rowvalues):
        if not colname in rows_to_drop: rows_to_drop[colname] = []
        rows_to_drop[colname].extend(rowvalues)

    # remove unwanted auction data
    add_rows_to_drop('country', 'NER 300 auctions')
    
    # over-engineer a function to identify super categories
    def gather_super_categories(categories):
        found = []
        num_stop_start = '^[0-9\.]+'
        num_maybe_stop_end = '\.?[0-9]\.?$'

        for category in categories:
            num_id = re.search(num_stop_start, category).group() # get identifying numbers at start of string
            super_category = num_id[:re.search(num_maybe_stop_end, num_id).start()] # keep all but last number (and stops if present)   1.1.2. -> 1.1
            if super_category and super_category not in found: found.append(super_category)

        found = [f+'.' if len(f)==1 else f for f in found] # handle inconsistent point formatting
        filter = pd.Series(categories).str.startswith(tuple([f+' ' for f in found])) 
        return categories[filter]
    
    categories = ets['category'].unique()
    add_rows_to_drop('category', *gather_super_categories(categories))
    add_rows_to_drop('sector', '21-99 All industrial installations (excl. combustion)', '20-99 All stationary installations')
    # fix inconsistent naming
    def remove_double_spaces(s): return s.replace('  ', ' ')
    ets['sector'] = ets['sector'].apply(remove_double_spaces)
    del ets['unit']
    add_rows_to_drop('year', 'Total 1st trading period (05-07)', 'Total 2nd trading period (08-12)', 'Total 3rd trading period (13-20)', 'Total 4th trading period (21-30)')

    # perform row drop and reset index
    for colname, values in rows_to_drop.items(): ets.drop(ets.loc[ets[colname].isin(values)].index, inplace=True)
    ets = ets.reset_index(drop=True)
    # format year type
    ets['year'] = ets['year'].astype('int')
    return ets

