from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

'''Ashpool - A Comparison Library
'''

import string
import uuid
from builtins import (ascii, bytes, chr, dict, filter, hex, input, int, map,
                      next, oct, open, pow, range, round, str, super, zip)
from itertools import chain, combinations, repeat
from operator import itemgetter
from warnings import warn

import numpy as np
import pandas as pd
from IPython.core.display import display
from past.utils import old_div


# print(string.punctuation, type(unicode(string.punctuation,'utf-8')))
TRAN_TBL = str.maketrans(str(string.punctuation), u' ' * len(string.punctuation))


def make_good_label(x_value):
    """Return something that is a better label.

    Arguments:
        x_value {string} -- or something that can be converted to a string
    """
    # if isinstance(x_value, str):
    #     x_value = x_value.encode('ascii', 'ignore')
    return '_'.join(str(x_value).translate(TRAN_TBL).split()).lower()


def mash(dframe, flds=None, keep_zeros=False):
    """Returns df of non-null and non-zero on flds

    Arguments:
        dframe {pandas.DataFrame} -- Input dataframe

    Keyword Arguments:
        flds {list} -- List of column nmaes (default: {None})
        keep_zeros {bool} -- True will keep zeros. (default: {False})

    Returns:
        pandas.DataFrame -- Dataframe with rows removed if null or zero on column[flds].
    """
    flds = [flds] if isinstance(flds, str) else flds
    df_work = dframe.copy()
    for each in flds:
        assert each in df_work.columns, '"{}" is not in df'.format(each)
        df_work = df_work[df_work[each].notnull()]
        if keep_zeros is False:
            df_work = df_work[df_work[each] != 0]
    return df_work


def flatten_on(dframe, flatten=[], agg_ovr={}):
    """Returns dataframe groupby all non_num fields except those listed in flatten list

    Arguments:
        dframe {pandas.DataFrame} -- input dataframe

    Returns:
        pandas.DataFrame -- same as source dataframe but flattened (i.e., categories removed and data aggregated over other non-numeric columns)
    """
    df_work = dframe.copy()
    df_dtypes = get_dtypes(df_work)
    fltr_non_num = df_dtypes[~df_dtypes['obj_kind'].isin(
        ['f', 'i'])]['fld'].tolist()
    fltr = [x.encode('UTF8') for x in fltr_non_num]
    fltr_num = df_dtypes[~df_dtypes['fld'].isin(fltr_non_num)]['fld'].tolist()
    for each in flatten:
        fltr.remove(each)
    agg_dict = dict(list(zip(fltr_num, repeat(sum))))
    agg_dict.update(agg_ovr)
    df_return = df_work.groupby(fltr).agg(agg_dict).reset_index()
    return df_return


def completeness(srs):
    """Return completeness score for series - i.e., the percentage of non-null values in a series.

    Arguments:
        srs {pandas.Series}

    Returns:
        float
    """
    if srs[srs.notnull()].empty:
        return 0.0

    return float(srs.notnull().sum()) / srs.shape[0]


def uniqueness(srs):
    '''return uniqueness score for series - i.e., percentage of unique values in series (excl. nulls).

    Arguments:
        srs {pandas.Series}

    Returns:
        float
    '''
    if srs[srs.notnull()].empty:
        return 0.0

    u_scr = old_div(float(srs.nunique()), srs.count())
    if u_scr == 1:
        print('{} is perfectly unique and covers {} of rows'.format(srs.name, old_div(float(srs.notnull().sum()), srs.shape[0])))
    return u_scr


def longest_member(srs):
    '''return the max len() of any member in series.

    Arguments:
        srs {pandas.Series}

    Returns:
        float
    '''
    if srs[srs.notnull()].empty:
        return 0.0

    max_len = 0
    for each in srs:
        if len(str(each)) > max_len:
            max_len = len(str(each))
    return max_len


def get_combos(lst):
    """Returns list of combinations of members of list.

    Arguments:
        lst {list} -- List of strings

    Returns:
        list -- List of combinations
    """
    combos = []
    if len(lst) > 10:
        warn('Suggest keep the number of fields below 10, this one is {}'.format(len(lst)))

    for each in range(len(lst)):
        if each > 0:
            combos.extend(combinations(lst, each + 1))
    return list(set(combos))



def get_dtypes(dframe):
    '''return dtypes and kinds by column names (fld)'''
    df_work = pd.DataFrame({'fld': dframe.columns.tolist()}, )
    df_work['obj_type'] = df_work.fld.apply(lambda x: dframe[x].dtype)
    df_work['obj_kind'] = df_work.fld.apply(lambda x: dframe[x].dtype.kind)
    return df_work


def rate_series(dframe):
    """return ratings of fields for completeness and uniqueness

    Arguments:
        dframe {pandas.DataFrame} -- Input dataframe.

    Returns:
        pandas.DataFrame -- Dataframe with statistics regarding the quality of columns as identifiers.
    """
    df_work = pd.DataFrame({'fld': dframe.columns.tolist()}, )
    df_work['obj_type'] = df_work.fld.apply(lambda x: dframe[x].dtype)
    df_work['obj_kind'] = df_work.fld.apply(lambda x: dframe[x].dtype.kind)
    df_work['completeness'] = df_work['fld'].apply(lambda x: completeness(dframe[x]))
    df_work['uniqueness'] = df_work['fld'].apply(lambda x: uniqueness(dframe[x]))
    df_work['longest_member'] = df_work['fld'].apply(lambda x: longest_member(dframe[x]))
    df_work.sort_values(['obj_type', 'completeness', 'uniqueness'], ascending=[False, False, False])
    return df_work


def get_sorted_fields(dframe):
    """return lists of fields sorted by most_complete, most_unique, and non_object

    Arguments:
        dframe {pandas.DataFrame} -- Input dataframe.

    Returns:
        dict -- Dictionary of lists with fields sorted by completeness and uniqueness. Also a list for fields with are non_object, which are not ranked for completeness or uniqueness.
    """
    df_work = rate_series(dframe)
    fltr_om = df_work['obj_kind'].isin(['O', 'M'])
    flds_srt_completeness = df_work[fltr_om].sort_values(
        ['completeness', 'longest_member'], ascending=[False, True])['fld'].tolist()
    flds_srt_uniqueness = df_work[fltr_om].sort_values(
        ['uniqueness', 'completeness', 'longest_member'], ascending=[False, False, True])['fld'].tolist()
    flds_non_object = df_work[~fltr_om]['fld'].tolist()
    return {'most_complete': flds_srt_completeness, 'most_unique': flds_srt_uniqueness, 'non_object': flds_non_object}


def attach_temp_id(dframe, field_list=None, id_label='tempid', append_uuid=False, prefix=''):
    """Attach an column with ID created from field_list and optionally add uuid

    Arguments:
        dframe {pandas.DataFrame} -- Input dataframe.

    Keyword Arguments:
        field_list {list} -- List of columns to use to build tempid. (default: {None})
        append_uuid {bool} -- True appends uuid. (default: {False})

    Returns:
        pandas.DataFrame -- Dataframe with tempid using flds.
    """
    df_work = dframe.copy()
    df_work['_prefix_'] = prefix.strip()
    df_work['_uuid_'] = ''

    if len(field_list) == 0:
        warn('No fields supplied.')
        return pd.DataFrame()

    if len(field_list) > 1:
        df_work[field_list] = df_work[field_list].applymap(str)
        flds_x = [df_work[x].tolist() for x in field_list[1:]]
        df_work['_work_'] = df_work[field_list[0]].str.cat(
            flds_x, sep='_', na_rep='nan')
    else:
        flds_x = field_list
        df_work['_work_'] = df_work[field_list]

    if append_uuid:
        df_work['_uuid_'] = pd.Series(
            ['_' + uuid.uuid4().hex[:3].upper() for x in range(len(df_work))])
        df_work['_work_'] = df_work['_work_'] + df_work['_uuid_']
    if prefix:
        df_work['_work_'] = df_work['_prefix_'] + '_' + df_work['_work_']
    df_work['_work_'] = df_work['_work_'].apply(make_good_label).str.upper()
    df_work = df_work.drop(['_prefix_', '_uuid_'], axis=1)
    df_work = df_work.rename(columns={'_work_': id_label})

    df_result = dframe.copy()
    df_result = pd.merge(
        df_result, df_work[[id_label]], left_index=True, right_index=True)

    return df_result


def get_unique_fields(dframe, candidate_flds, threshold=1.0, max_member_length=30, show_all=False):
    """Return list of fields that combine to create an ID that has uniqueness >= threshold.

    Arguments:
        dframe {pandas.DataFrame} -- Input dataframe.
        candidate_flds {list} -- List of column names.

    Keyword Arguments:
        threshold {float} -- Uniqueness threshold where 1 is perfectly unique (default: {1})
        max_member_length {int} -- Used to filter out columns which have members that are too lengthy. (default: {30})
        show_all {bool} -- Show all results even if uniqueness does not meet threshold. (default: {False})

    Returns:
        list -- List of column names that combine to create a unique ID.
    """
    summary = []
    flds_work = [x for x in candidate_flds if longest_member(dframe[x]) <= max_member_length]
    for each in get_combos(flds_work):
        df_temp = attach_temp_id(dframe[list(each)], field_list=list(each))  # .copy()
        df_temp['tempid_makeup'] = str(each)
        u_scr = uniqueness(df_temp['tempid'])
        summary.append((str(each), u_scr))
        if u_scr >= threshold:
            print('Uniqueness: {}'.format(u_scr))
            display(df_temp.head())
            if not show_all:
                return list(each)

    summary.sort(key=itemgetter(1), reverse=True)

    if show_all:
        return summary

    assert summary[0][1] >= threshold, 'Does not meet threshold of {}, best found was {}'.format(threshold, summary[0][1])
    return


def attach_unique_id(dframe, threshold=0.5):
    """Return a new dataframe based on input dframe with unique fields attached.

    Arguments:
        dframe {pandas.DataFrame} -- Source dataframe
        threshold {float} -- Specify how unique 0.0 to 1.0 (most unique)

    Returns:
        pandas.DataFrame -- datatframe with most unique fields attached.
    """
    flds = get_sorted_fields(dframe)
    u_flds = get_unique_fields(dframe, candidate_flds=flds['most_unique'], threshold=threshold)
    print('!!!u_flds:', u_flds)
    assert u_flds, 'Did not get valid unique fields'
    df_work = attach_temp_id(dframe, field_list=u_flds, id_label='u_id')
    return df_work[['u_id'] + flds['most_unique'] + sorted(flds['non_object'])]


def coveredness(srs_l, srs_r):
    """Returns percentage of srs_l members that can be found in srs_r

    Arguments:
        srs_l {pandas.Series} -- Source series.
        srs_r {pandas.Series} -- Target series.

    Returns:
        float -- Percentage of srs_l members that can be found in srs_r
    """
    if srs_l.empty or srs_r.empty:
        warn('One of the series used is empty.')
        return 0.0
    return old_div(float(srs_l.isin(srs_r).sum()), srs_l.shape[0])


def jaccard_similarity(srs_l, srs_r):
    """Returns the jaccard similarity between two lists"""
    intersection_card = len(set.intersection(*[set(srs_l), set(srs_r)]))
    union_card = len(set.union(*[set(srs_l), set(srs_r)]))
    return old_div(intersection_card, float(union_card))


def oneness(srs_l, srs_r):
    '''TODO'''
    map_len_l = len(dict(list(zip(srs_l.tolist(), srs_r.tolist()))))
    map_len_r = len(dict(list(zip(srs_r.tolist(), srs_l.tolist()))))
    return old_div(min(map_len_l, map_len_r), max(map_len_l, map_len_r))


def has_name_match(srs_l, dframe_r):
    """Returns True if srs_l name found in dframe_r

    Arguments:
        srs_l {pandas.Series} -- Source series.
        dframe_r {pandas.DataFrame} -- Dataframe to search.

    Returns:
        bool -- True if srs_l.name is found in dframe_r.columns.
    """
    if srs_l.name in dframe_r.columns:
        return True
    return False


def get_most_coveredness(srs_l, dframe_r, top_limit=3):
    """Returns columns that most cover source series

    Arguments:
        srs_l {pandas.Series} -- Input series.
        dframe_r {pandas.DataFrame} -- Target dataframe to search.

    Keyword Arguments:
        top_limit {int} -- Maximum number of column names (default: {3})

    Returns:
        list -- List of columns from dframe_r that most cover srs_l.
    """
    res = []
    for each in dframe_r:
        if srs_l.dtype == dframe_r[each].dtype:
            cvd = coveredness(srs_l, dframe_r[each])
            if cvd > 0:
                res.append((each, cvd))
    res.sort(key=itemgetter(1), reverse=True)
    return res[:top_limit]


def check_coveredness(dframe_l, dframe_r):
    """Returns ratings of coveredness for columns in dframe_l

    Arguments:
        dframe_l {pandas.DataFrame} -- Source dataframe.
        dframe_r {pandas.DataFrame} -- Target dataframe.

    Returns:
        pandas.DataFrame -- Dataframe showing statistics regard each columns coveredness.
    """
    df_work = pd.DataFrame({'fld': dframe_l.columns.tolist()}, )
    df_work['obj_type'] = df_work.fld.apply(lambda x: dframe_l[x].dtype)
    df_work['obj_kind'] = df_work.fld.apply(lambda x: dframe_l[x].dtype.kind)
    df_work['has_name_match'] = df_work.fld.apply(lambda x: has_name_match(dframe_l[x], dframe_r))
    df_work['coveredness'] = df_work['fld'].apply(lambda x: get_most_coveredness(dframe_l[x], dframe_r))

    df_work['completeness'] = df_work['fld'].apply(lambda x: completeness(dframe_l[x]))
    df_work['uniqueness'] = df_work['fld'].apply(lambda x: uniqueness(dframe_l[x]))
    df_work['longest_member'] = df_work['fld'].apply(lambda x: longest_member(dframe_l[x]))
    return df_work


def suggest_id_pairs(dframe_l, dframe_r, threshold=0.5, incl_all_dtypes=False, incl_all_pairs=False):
    """Suggest matching series from two dfs.

    Arguments:
        dframe_l {pandas.DataFrame} -- Left dataframe.
        dframe_r {pandas.DataFrame} -- Right dataframe.

    Keyword Arguments:
        threshold {float} -- Value between 0 and 1 that represents minimum coveredness. (default: {0.5})
        incl_all_dtypes {bool} -- Try to use all dtypes (not just object) if True. (default: {False})
        incl_all_pairs {bool} -- Show all pairs regardless of threshold. (default: {False})

    Returns:
        pandas.DataFrame -- Statistics regarding which pairs of columns to use as IDs and their score (id_scr).
    """
    flds_l = dframe_l.columns.tolist()
    flds_r = dframe_r.columns.tolist()
    pairs = []
    for fld in flds_l:
        dtype_l = dframe_l[fld].dtype.kind
        if incl_all_dtypes or dtype_l == 'O':
            for each in flds_r:
                cvd = coveredness(dframe_l[fld], dframe_r[each])
                if cvd >= threshold:
                    cvd_reversed = coveredness(dframe_r[each], dframe_l[fld])
                    complete_l = completeness(dframe_l[fld])
                    complete_r = completeness(dframe_l[fld])
                    uniq_l = uniqueness(dframe_l[fld])
                    uniq_r = uniqueness(dframe_l[fld])
                    pairs.append((fld, each, cvd, cvd_reversed, complete_l, complete_r, uniq_l, uniq_r))
    df_result = pd.DataFrame(pairs, columns=['fld_l', 'fld_r', 'cover_l', 'cover_r', 'complete_l', 'complete_r', 'uniq_l', 'uniq_r'])
    df_result['id_scr'] = df_result.product(axis=1, numeric_only=True)
    df_result.sort_values(['id_scr'], ascending=False, inplace=True)
    df_result.reset_index(drop=True, inplace=True)
    if incl_all_pairs:
        return df_result
    df_result = df_result.groupby(['fld_l']).first().sort_values(['id_scr'], ascending=False).reset_index()
    return df_result


def cum_uniq(dframe, flds=None):
    """Return list of incremental uniqueness as tempid is created based on flds.

    Arguments:
        dframe {pandas.DataFrame} -- Source dataframe.

    Keyword Arguments:
        flds {list} -- List of columnn names to be used for create tempid. (default: {None})

    Returns:
        list -- List of floats representing incremental addition to uniqueness as more columns are used to create a tempid.
    """
    flds_work = [f for f in flds if f in dframe.columns]
    u_res = []

    for each in range(len(flds_work)):
        df_temp = attach_temp_id(dframe, field_list=flds_work[:each + 1])
        u_res.append(uniqueness(df_temp['tempid']))
    return u_res


def best_id_pair(dframe_l, dframe_r, threshold=0.5):
    """Return df showing which IDs are best for matching two dfs.

    Arguments:
        dframe_l {pandas.DataFrame} -- Left dataframe.
        dframe_r {pandas.DataFrame} -- Right dataframe.

    Keyword Arguments:
        threshold {float} -- Value between 0 and 1 that represents minimum coveredness (default: {0.5})

    Returns:
        pandas.DataFrame -- Dataframe showing best IDs to use to align source dataframes.
    """
    df_work = suggest_id_pairs(dframe_l, dframe_r, threshold=threshold)
    df_work['cum_uniq_l'] = cum_uniq(dframe_l, flds=df_work['fld_l'].tolist())
    df_work['cum_uniq_r'] = cum_uniq(dframe_r, flds=df_work['fld_r'].tolist())
    df_work['cum_uniq_l_increment'] = df_work['cum_uniq_l'] - df_work['cum_uniq_l'].shift()
    df_work['cum_uniq_r_increment'] = df_work['cum_uniq_r'] - df_work['cum_uniq_r'].shift()
    df_result = df_work[~((df_work['cum_uniq_l_increment'] == 0) & (df_work['cum_uniq_r_increment'] == 0))]

    if df_result.empty:
        warn('Could not find a good id to use for aligning dataframes.')
        return pd.DataFrame()
    return df_result


def reconcile(dframe_l, dframe_r, fields_l=None, fields_r=None, gen_diffs=True):
    """Aligns and compares two dataframes

    Arguments:
        dframe_l {pandas.DataFrame} -- left dataframe
        dframe_r {pandas.DataFrame} -- right dataframe

    Keyword Arguments:
        fields_l {list} -- list of columns names to compare from dframe_l (default: {None})
        fields_r {list} -- list of columns names to compare from dframe_r (default: {None})
        gen_diffs {bool} -- whether or not to include a calculation of the difference in results (default: {True})

    Returns:
        dataframe -- shows results of the comparison
    """
    if dframe_l.empty or dframe_r.empty:
        warn('One or both source dataframes are empty.')
        return pd.DataFrame()

    df_best = best_id_pair(dframe_l, dframe_r)

    if df_best.empty:
        warn('Returning empty dataframe.')
        return pd.DataFrame()

    print('Diags:')
    display(df_best)
    df_temp_l = attach_temp_id(dframe_l, field_list=df_best['fld_l'].tolist())
    df_temp_r = attach_temp_id(dframe_r, field_list=df_best['fld_r'].tolist())
    return differ(df_temp_l, df_temp_r, left_on='tempid', right_on='tempid', fields_l=fields_l, fields_r=fields_r, gen_diffs=gen_diffs)


def differ(dframe_l, dframe_r, left_on, right_on, fields_l=None, fields_r=None, gen_diffs=False, return_data=True):
    '''TODO'''
    assert len(fields_l) == len(fields_r), 'Comparison lists not of equal length / None.'

    df_l = dframe_l.rename(columns={left_on: 'compid'}).copy()
    df_r = dframe_r.rename(columns={right_on: 'compid'}).copy()
    fields = list(zip(fields_l, fields_r))

    final_fields = []
    for each in fields:
        if each[0] == each[1]:
            final_fields.append((each[0] + '_l', each[1] + '_r'))
        else:
            final_fields.append(each)

    ordered_fields = list(chain(*final_fields))
    df_out = pd.merge(df_l[['compid'] + fields_l], df_r[['compid'] + fields_r], how='outer', left_on='compid', right_on='compid', suffixes=['_l', '_r'], indicator='found')
    df_out = df_out[['compid', 'found'] + ordered_fields]

    # Do comparison
    vs_fields = []
    for each in final_fields:
        lbl = each[0] + ' vs ' + each[1]
        try:
            df_out[lbl] = np.isclose(
                df_out[each[0]], df_out[each[1]], rtol=0.000000001, atol=0.0001)
            vs_fields.append(lbl)
        except:
            print('Cannot compare:', lbl)
            print(each[0], type(each[0]), each[1], type(each[1]))

    df_out['vs_pct'] = old_div(sum([df_out[each] for each in vs_fields]), len(fields))

    # Calc diffs
    if gen_diffs:
        for each in final_fields:
            lbl = each[0] + ' - ' + each[1]
            lbl2 = each[0] + ' / ' + each[1]
            try:
                df_out[lbl] = df_out[each[0]] - df_out[each[1]]
                df_out[lbl2] = old_div(df_out[each[0]], df_out[each[1]])
            except:
                print('Cannot calc diff:', lbl, lbl2)
                print(each[0], type(each[0]), each[1], type(each[1]))

    # Check if need to return data
    if not return_data:
        df_out = df_out.drop(ordered_fields, axis=1)

    return df_out
