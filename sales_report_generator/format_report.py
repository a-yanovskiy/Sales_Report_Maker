import numpy as np
import pandas as pd
import re


def read_xlsx(file_):
    """ read excel to dataframe and replace all empty values to NaN """
    dataframe = pd.read_excel(io=file_, engine='openpyxl', dtype=str)
    dataframe = dataframe.replace(r'^\s*$', np.nan, regex=True)
    dataframe = dataframe.set_index(dataframe.columns[0])  # 1st column --> index
    return dataframe


def sort_and_filter_dict_by_items(dictionary, filter_by='positive'):
    """ sort dict by float values """
    dict_ = {}
    for i, k in dictionary.items():
        if not pd.isnull(k):
            k = int(k) if k.count('.') == 0 else float(k)
            if filter_by == 'positive':
                if k < 0:
                    continue
            elif filter_by == 'negative':
                if k >= 0:
                    continue
                else:
                    k = abs(k)
            dict_[i] = k

    series = pd.Series(dict_)
    series.sort_values(
        axis=0,
        ascending=False,
        inplace=True,
        kind='quicksort',
        na_position='last',
        ignore_index=False,
        key=None,
    )

    result = series.to_dict()
    return result


def format_dict(input_dict, word_to_be_deleted) -> str:
    result = ''
    for market, value in input_dict.items():
        market = market.replace(word_to_be_deleted, "").strip()
        if value == value:
            meter = 'кг'
            if re.match(r'^-?\d+(?:\.\d+)$', str(value)) is None:
                meter = 'шт'
                value = int(value)
            else:
                value = round(float(value), 2)
        else:
            continue
        result += market + ': ' + str(value) + ' ' + meter + '; '
    return result


def df_to_dict(df_series, result=None) -> dict:
    if result is None:
        result = {}
    df_series = df_series[df_series.index.notnull()]
    item = df_series.iloc[0:1]
    rest_items = df_series.iloc[1:]
    if item.empty:
        return result
    else:
        index = item.index[0]
        value = item.values[0][0]
        result[index] = value
        return df_to_dict(rest_items, result)
