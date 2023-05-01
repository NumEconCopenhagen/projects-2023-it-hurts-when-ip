import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from IPython.display import display
import re
import random
import colorsys


def clean_ets(ets):

    # a. rename columns
    ets.rename(columns={'ETS information':'category', 'main activity sector name':'sector'}, inplace=True)
   

    # b. establish list of rows to drop and handler function
    rows_to_drop = {}
    def add_rows_to_drop(colname, *rowvalues):
        if not colname in rows_to_drop: rows_to_drop[colname] = []
        rows_to_drop[colname].extend(rowvalues)

    
    # c. remove unwanted data
    add_rows_to_drop('country', 'NER 300 auctions')
    add_rows_to_drop('sector', '21-99 All industrial installations (excl. combustion)', '20-99 All stationary installations')
    add_rows_to_drop('year', 'Total 1st trading period (05-07)', 'Total 2nd trading period (08-12)', 'Total 3rd trading period (13-20)', 'Total 4th trading period (21-30)')
    del ets['unit']


    # d. special case: categories 
    # -> want to remove all super-categories
    categories = ets['category'].unique()
    supers = []
    num_stop_start = '^[0-9\.]+'
    num_maybe_stop_end = '\.?[0-9]\.?$'

    for category in categories:
        num_id = re.search(num_stop_start, category).group() # get identifying numbers at start of string
        super_category = num_id[:re.search(num_maybe_stop_end, num_id).start()] # remove last number and stops   1.1.2. -> 1.1
        if super_category and super_category not in supers: supers.append(super_category)

    supers = [s+'.' if len(s)==1 else s for s in supers] # handle inconsistent point formatting
    filter = pd.Series(categories).str.startswith(tuple([s+' ' for s in supers]))     
    add_rows_to_drop('category', *categories[filter])
    
    
    # e. perform row drop and reset index
    for colname, values in rows_to_drop.items(): ets.drop(ets.loc[ets[colname].isin(values)].index, inplace=True)
    ets = ets.reset_index(drop=True)


    # f. other cleaning
    # fix inconsistent naming of sectors
    def remove_double_spaces(s): return s.replace('  ', ' ')
    ets['sector'] = ets['sector'].apply(remove_double_spaces)
    # format year type
    ets['year'] = ets['year'].astype('int')
    
    
    return ets


def sort_legend(ax, key=lambda label: label, reverse=False, **kw):
    handles, labels = ax.get_legend_handles_labels()
    handle_label = zip(handles, labels)
    handles, labels = zip(*sorted(handle_label, key=lambda h_l: key(h_l[1]), reverse=reverse))
    ax.legend(handles, labels, **kw)


def stretch_series(series, pow=1, span=1, lb=0):
    series = series.copy()
    series **= pow
    series *= span / (max(series)-min(series))
    series += lb - min(series)
    return series 


def random_colour():
    hsv_colour = (random.uniform(0,1), 0.75, 0.75)
    rgb_colour = colorsys.hsv_to_rgb(*hsv_colour)
    return rgb_colour
