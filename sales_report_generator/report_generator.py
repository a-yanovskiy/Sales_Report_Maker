import re
import format


def generate_report(dataframe,
                    result='',
                    dish_add_text='',
                    leaders_add_text='',
                    grows_add_text='',
                    falls_add_text='',
                    dish_del_text=''):

    df_first_column = dataframe.iloc[:, 0:1]
    df_second_column = dataframe.iloc[:, 1:2]
    
    if df_first_column.empty:
        return result
    else:
        dish = re.split('[0-9]', df_first_column.columns[0])[0].strip()
        
        result += '\n' + dish_add_text + '*_' + dish + '_*'

        if not df_second_column.empty:
            if re.match(r'^Unnamed', df_second_column.columns[0]):
                df_rest_columns = dataframe.iloc[:, 2:]
                comparing = format.df_to_dict(df_second_column)

                grows_sales = format.sort_and_filter_dict_by_items(comparing,
                                                                   'positive')
                result += ('\n' + grows_add_text +
                           format.format_dict(grows_sales, dish_del_text))

                falls_sales = format.sort_and_filter_dict_by_items(
                    comparing, 'negative')
                result += ('\n' + falls_add_text +
                           format.format_dict(falls_sales, dish_del_text))

            else:
                df_rest_columns = dataframe.iloc[:, 1:]
        else:
            df_rest_columns = dataframe.iloc[:, 1:]
        
        f = format.df_to_dict(df_first_column)
        sorted_ = format.sort_and_filter_dict_by_items(f)
        sales_leaders = format.format_dict(sorted_, dish_del_text)
        
        result += '\n' + leaders_add_text + ' ' + sales_leaders + '\n'

        return generate_report(df_rest_columns,
                               result,
                               dish_add_text,
                               leaders_add_text,
                               grows_add_text,
                               falls_add_text,
                               dish_del_text)

