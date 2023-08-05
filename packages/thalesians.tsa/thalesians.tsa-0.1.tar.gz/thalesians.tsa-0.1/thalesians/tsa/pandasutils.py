import collections as col
import datetime as dt

import numpy as np
import pandas as pd

import thalesians.tsa.checks as checks
import thalesians.tsa.conversions as conv
import thalesians.tsa.times as tsatimes
import thalesians.tsa.utils as utils

eq = lambda column, value, fun=None: \
    (lambda df: (df[column] if fun is None else df[column].apply(fun)) == value)
    
lt = lambda column, value, fun=None: \
    (lambda df: (df[column] if fun is None else df[column].apply(fun)) < value)
    
gt = lambda column, value, fun=None: \
    (lambda df: (df[column] if fun is None else df[column].apply(fun)) > value)
    
leq = lambda column, value, fun=None: \
    (lambda df: (df[column] if fun is None else df[column].apply(fun)) <= value)
    
geq = lambda column, value, fun=None: \
    (lambda df: (df[column] if fun is None else df[column].apply(fun)) >= value)
    
isin = lambda column, values, fun=None: \
    (lambda df: (df[column] if fun is None else df[column].apply(fun)).isin(values))

def apply_predicates(df, predicates):
    for p in predicates:
        if p is not None: df = df[p(df)]
    return df

def apply_funs(df, funs):
    for f in funs:
        if f is not None: df = f(df)
    return df

def load_df_from_zipped_csv(path, predicates=[], pre_funs=[], post_funs=[], **kwargs):
    if 'iterator' not in kwargs: kwargs['iterator'] = True
    if 'chunksize' not in kwargs: kwargs['chunksize'] = 10000
    if 'compression' not in kwargs: kwargs['compression'] = 'zip'
    if 'header' not in kwargs: kwargs['header'] = 0
    if 'dtype' not in kwargs: kwargs['dtype'] = str
    if 'keep_default_na' not in kwargs: kwargs['keep_default_na'] = False
    it = pd.read_csv(path, **kwargs)
    df = pd.concat([apply_funs(apply_predicates(apply_funs(chunk, pre_funs), predicates), post_funs) for chunk in it])
    # Since we are reading the data chunk by chunk and then concatenating the resulting data frames, the indices may not
    # be unique. We correct this by replacing them:
    df.index = range(len(df))
    return df

def detect_df_column_types(df, none_values=conv.default_none_values, min_success_rate=conv.default_min_success_rate,
                           convert=False, in_place=False, return_df=False):
    if convert and (not in_place): return_df = True
    if not in_place: df = df.copy()
    types = {}
    for c in df.columns:
        if df[c].dtype != object:
            types[c] = df[c].dtype
            continue
        
        if len(df) == 0 or not checks.is_string(df[c].values[0]):
            types[c] = object
            continue
        
        float_results, float_success_count, _ = conv.strs_to_float(df[c].values, none_values=none_values,
                none_result=float('nan'), raise_value_error=False, return_extra_info=True,
                min_success_rate=min_success_rate)
        if float_results is not None and float_success_count > 0:
            int_results, int_success_count, _ = conv.strs_to_int(df[c].values, none_values=none_values,
                    none_result=None, min_success_rate=min_success_rate,
                    raise_value_error=False, return_extra_info=True)
            if float_success_count > int_success_count:
                types[c] = float
                if convert: df[c] = float_results
            else:
                types[c] = int
                if convert: df[c] = int_results
            continue        
        
        datetime_results = conv.strs_to_datetime(df[c].values, none_values=none_values, none_result=None,
                                                 raise_value_error=False, return_extra_info=False,
                                                 min_success_rate=min_success_rate)
        if datetime_results is not None:
            types[c] = dt.datetime
            if convert: df[c] = datetime_results
            continue
        
        date_results = conv.strs_to_date(df[c].values, none_values=none_values, none_result=None,
                                         raise_value_error=False, return_extra_info=False,
                                         min_success_rate=min_success_rate)
        if date_results is not None:
            types[c] = dt.date
            if convert: df[c] = date_results
            continue
        
        time_results = conv.strs_to_time(df[c].values, none_values=none_values, none_result=None,
                                         raise_value_error=False, return_extra_info=False,
                                         min_success_rate=min_success_rate)
        if time_results is not None:
            types[c] = dt.time
            if convert: df[c] = time_results
            continue
        
        types[c] = type(df[c].values[0]) if len(df) > 0 else None        
    
    return (types, df) if return_df else types

def convert_df_columns(df, conversions, in_place=False):
    if not in_place: df = df.copy()
    conversion_columns = set(conversions.keys())
    unfamiliar_columns = conversion_columns.difference(df.columns)
    assert len(unfamiliar_columns) == 0, 'Unfamiliar columns: %s' % str(unfamiliar_columns)
    for column, conversion in conversions.items():
        df[column] = df[column].apply(conversion)
    return df

def detect_df_categorical_columns(df):
    categorical_columns = []
    for c in df.columns:
        distinct_element_count = len(set(df[c]))
        if distinct_element_count <= 100 and distinct_element_count <= 0.1 * len(df):
            categorical_columns.append(c)
    return categorical_columns

def get_column_types(df):
    column_types = col.OrderedDict()
    if len(df) > 0:
        for c in df.columns:
            if df[c].dtype == object:
                non_none_values = [x for x in df[c].values if x is not None]
                column_types[c] = type(df[c].values[0]) if len(non_none_values) > 0 else object
            else:
                if isinstance(df[c].values[0], np.datetime64):
                    column_types[c] = np.datetime64
                else:
                    column_types[c] = df[c].dtype
    return column_types

def get_df_columns_of_type(df, types):
    columns = []
    if len(df) > 0:
        for c in df.columns:
            non_none_values = [x for x in df[c].values if x is not None]
            if len(non_none_values) > 0 and isinstance(df[c].values[0], types):
                columns.append(c)
    return columns

def get_df_int_columns(df):
    return get_df_columns_of_type(df, (int, np.int64))

def get_df_float_columns(df):
    return get_df_columns_of_type(df, (float, np.float64))

def get_df_time_columns(df):
    return get_df_columns_of_type(df, dt.time)

def get_df_date_columns(df):
    return get_df_columns_of_type(df, dt.date)

def get_df_datetime_columns(df):
    return get_df_columns_of_type(df, (dt.datetime, np.datetime64))

def combine_date_time(df, date_column, time_column):
    return df[[date_column, time_column]].apply(lambda x: dt.datetime.combine(x[0], x[1]), axis=1)

def first(x):
    if isinstance(x, pd.DataFrame): return x.apply(first)
    else: return x[0] if checks.is_iterable(x) else x

def last(x):
    if isinstance(x, pd.DataFrame): return x.apply(first)
    else: return x[-1] if checks.is_iterable(x) else x

def mean_or_first(x):
    if isinstance(x, pd.DataFrame): return x.apply(mean_or_first)
    else:
        try: return np.mean(x)
        except: return x[0] if checks.is_iterable(x) else x

def mean_or_last(x):
    if isinstance(x, pd.DataFrame): return x.apply(mean_or_last)
    else:
        try: return np.mean(x)
        except: return x[-1] if checks.is_iterable(x) else x

def intraday_to_daily(df, aggregator=mean_or_last,
                      date=None, time=None, datetime=None,
                      new_date_column=None,
                      fix_kind='last', fix_time=None, fix_points=10,
                      min_fix_point_count=None, max_fix_point_count=None,
                      min_min_fix_point_time=None, max_min_fix_point_time=None,
                      min_max_fix_point_time=None, max_max_fix_point_time=None,
                      already_sorted=False,
                      aggregators_apply_to_df=False,
                      return_extra_info=False):
    checks.check(datetime is not None or checks.are_all_not_none(date, time),
            'Either datetime or both date and time must be specified')
    
    columns_to_exclude = set()
    
    if datetime is not None:
        checks.check_all_none(date, time)
        if isinstance(datetime, str):
            columns_to_exclude.add(datetime)
            if new_date_column is None: new_date_column = datetime
            datetime = df[datetime].values
        date = [x.date() for x in datetime]
        time = [x.time() for x in datetime]
    else:
        checks.are_all_not_none(date, time)
        if isinstance(date, str):
            columns_to_exclude.add(date)
            if new_date_column is None: new_date_column = date
            date = df[date].values
        if isinstance(time, str): time = df[time].values
        
    if new_date_column is None: new_date_column = 'date'
    
    if fix_kind in ('first', 'after'): comparison_direction = 'geq'
    elif fix_kind == 'after_exclusive': comparison_direction = 'gt'
    elif fix_kind in ('last', 'before'): comparison_direction = 'leq'
    elif fix_kind == 'before_exclusive': comparison_direction = 'lt'
    else: raise ValueError('Unfamiliar fix_kind: "%s"' % str(fix_kind))
    
    if fix_kind in ('first', 'last'): checks.check_none(fix_time)
    else: checks.check_not_none(fix_time)
    
    numeric_fix_points = checks.is_some_number(fix_points)
    if not numeric_fix_points: fix_points = conv.to_python_timedelta(fix_points)
    
    grouping_df = pd.DataFrame({'date': date, 'time': time}, columns=('date', 'time'))
    
    grouped_df = grouping_df.groupby(date)
    
    columns = [new_date_column]
    data = {new_date_column: []}
    aggs = {}
    
    if checks.is_some_dict(aggregator): column_agg_pairs = aggregator.items()
    elif checks.is_iterable(aggregator): column_agg_pairs = aggregator
    else: column_agg_pairs = zip(df.columns, utils.xconst(aggregator))
    for column, agg in column_agg_pairs:
        columns.append(column)
        data[column] = []
        aggs[column] = agg
        
    dates_with_no_points = []
    dates_with_fix_point_limits_breached = col.OrderedDict()
    fix_point_counts = col.OrderedDict()
    
    for next_date, group_df in grouped_df:
        if len(group_df) == 0: dates_with_no_points.append(next_date)
        if not already_sorted:
            group_df = group_df.copy()
            group_df.sort_values('time', inplace=True)
        if fix_kind == 'first': fix_time = group_df['time'].values[0]
        elif fix_kind == 'last': fix_time = group_df['time'].values[-1]
        
        if numeric_fix_points:
            if comparison_direction == 'geq':
                fix_point_indices = group_df.index[group_df['time'] >= fix_time][0:fix_points]
            elif comparison_direction == 'gt':
                fix_point_indices = group_df.index[group_df['time'] > fix_time][0:fix_points]
            elif comparison_direction == 'leq':
                fix_point_indices = group_df.index[group_df['time'] <= fix_time][-fix_points:]
            else: # comparison_direction == 'le'
                fix_point_indices = group_df.index[group_df['time'] < fix_time][-fix_points:]
        else:
            if comparison_direction == 'geq':
                fix_point_indices = group_df.index[(group_df['time'] >= fix_time) & (group_df['time'] <= tsatimes.plus_timedelta(fix_time, fix_points))]
            elif comparison_direction == 'gt':
                fix_point_indices = group_df.index[(group_df['time'] > fix_time) & (group_df['time'] <= tsatimes.plus_timedelta(fix_time, fix_points))]
            elif comparison_direction == 'leq':
                fix_point_indices = group_df.index[(group_df['time'] <= fix_time) & (group_df['time'] >= tsatimes.plus_timedelta(fix_time, -fix_points))]
            else: # comparison_direction == 'le':
                fix_point_indices = group_df.index[(group_df['time'] < fix_time) & (group_df['time'] >= tsatimes.plus_timedelta(fix_time, -fix_points))]
                
        fix_point_limits_breached = set()

        if min_fix_point_count is not None and len(fix_point_indices) < min_fix_point_count:
            fix_point_limits_breached.add('min_fix_point_count')
        if max_fix_point_count is not None and len(fix_point_indices) > max_fix_point_count:
            fix_point_limits_breached.add('max_fix_point_count')
        if min_min_fix_point_time is not None:
            if checks.is_some_timedelta(min_min_fix_point_time):
                the_min_min_fix_point_time = fix_time + min_min_fix_point_time if comparison_direction in ('geq', 'gt') else fix_time - min_min_fix_point_time
            else: the_min_min_fix_point_time = min_min_fix_point_time
            if min(grouping_df['time'].values[fix_point_indices]) < the_min_min_fix_point_time:
                fix_point_limits_breached.add('min_min_fix_point_time')
        if max_min_fix_point_time is not None:
            if checks.is_some_timedelta(max_min_fix_point_time):
                the_max_min_fix_point_time = fix_time + max_min_fix_point_time if comparison_direction in ('geq', 'gt') else fix_time - max_min_fix_point_time
            else: the_max_min_fix_point_time = max_min_fix_point_time
            if min(grouping_df['time'].values[fix_point_indices]) > the_max_min_fix_point_time:
                fix_point_limits_breached.add('max_min_fix_point_time')
        if min_max_fix_point_time is not None:
            if checks.is_some_timedelta(min_max_fix_point_time):
                the_min_max_fix_point_time = fix_time + min_max_fix_point_time if comparison_direction in ('geq', 'gt') else fix_time - min_max_fix_point_time
            else: the_min_max_fix_point_time = min_max_fix_point_time
            if max(grouping_df['time'].values[fix_point_indices]) < the_min_max_fix_point_time:
                fix_point_limits_breached.add('min_max_fix_point_time')
        if max_max_fix_point_time is not None:
            if checks.is_some_timedelta(max_max_fix_point_time):
                the_max_max_fix_point_time = fix_time + max_max_fix_point_time if comparison_direction in ('geq', 'gt') else fix_time - max_max_fix_point_time
            else: the_max_max_fix_point_time = max_max_fix_point_time
            if max(grouping_df['time'].values[fix_point_indices]) > the_max_max_fix_point_time:
                fix_point_limits_breached.add('max_max_fix_point_time')
                
        if len(fix_point_limits_breached) > 0:
            dates_with_fix_point_limits_breached[next_date] = fix_point_limits_breached
        else:
            data[new_date_column].append(next_date)
            for column in columns[1:]:
                if column not in columns_to_exclude:
                    arg = df.iloc[fix_point_indices] if aggregators_apply_to_df else df.iloc[fix_point_indices][column].values
                    data[column].append(aggs[column](arg))
            fix_point_counts[next_date] = len(fix_point_indices)
    
    df = pd.DataFrame(data, columns=columns)
            
    if return_extra_info:
        return {
                'df': df,
                'dates_with_no_points': dates_with_no_points,
                'dates_with_fix_point_limits_breached': dates_with_fix_point_limits_breached,
                'fix_point_counts': fix_point_counts
            }
    else: return df
    