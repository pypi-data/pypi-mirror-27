import pandas as pd
import sys
reload(sys)
sys.setdefaultencoding("utf8")
import re
from itertools import combinations
import pandas as pd
import numpy as np
import datetime
import dill
from pyspark import SparkContext
from pyspark import HiveContext
from pyspark.sql import SparkSession
hc = SparkSession.builder.appName("appNAme").enableHiveSupport().getOrCreate()
sc = hc.sparkContext

"""
time test
sample_num   feature_num    time(second,10 rounds average)
  11000         3600                     92.7
  53000         40000                   2004.3
  500000        3600                    1343.5
"""


def group_by_df(data, flag_name, factor_name, bad_name, good_name, na_trigger):
    if len(data) == 0:
        return pd.DataFrame()
    data = data[flag_name].groupby(
        [data[factor_name], data[flag_name]]).count()
    data = data.unstack()
    data = data.reset_index()
    data = data.fillna(0)
    if len(data.columns) == 3:
        data.columns = [factor_name, good_name, bad_name]
        if not na_trigger:
            data[factor_name] = data[factor_name].astype(float)
        data = data.sort_values(by=[factor_name], ascending=True)
        data[factor_name] = data[factor_name].astype(str)
        data = data.reset_index(drop=True)
        return data
    else:
        return pd.DataFrame()


def verify_df_two(date_df, flag_name):
    date_df = date_df.drop(date_df[date_df[flag_name].isnull()].index)
    check = date_df[date_df[flag_name] > 1]
    if len(check) != 0:
        print 'Error: there exits the number bigger than one in the data'
        date_df = pd.DataFrame()
        return date_df
    elif len(date_df) != 0:
        date_df[flag_name] = date_df[flag_name].astype(int)
        return date_df
    else:
        print 'Error: the data is wrong'
        date_df = pd.DataFrame()
        return date_df


def getAllindex(tar_list, item):
    return list(filter(lambda a: tar_list[a] == item, range(0, len(tar_list))))


# the split function part
# since there are the restriction to the position of the best ks ,thus we need to add some transformation to the start
# and end knot in the current function
def best_KS_knot_calculator(data, total_len, good_name, bad_name, start_knot, end_knot, rate):
    # this part may seems to be redundant, you can replace it by passing the total_len in the input part of the function
    # total_len = sum(data[good_name]) + sum(data[bad_name])
    temp_df = data.loc[start_knot:end_knot]
    # the temp len here represents the length of the unique values in the raw data, not only the length of the temp_df
    temp_len = sum(temp_df[good_name]) + sum(temp_df[bad_name])
    # since we'd want to make sure the number of elements in each tiny bin should always greater than 5% of the raw
    # data's length, we need to add some restrictions to the start_knot and the end_knot
    start_add_num = sum(
        np.cumsum(temp_df[good_name] + temp_df[bad_name]) < rate * total_len)
    end_add_num = sum(
        np.cumsum(temp_df[good_name] + temp_df[bad_name]) <= temp_len - rate * total_len)
    processed_start_knot = start_knot + start_add_num
    processed_end_knot = start_knot + end_add_num - 1
    if processed_end_knot >= processed_start_knot:
        if sum(temp_df[bad_name]) != 0 and sum(temp_df[good_name]) != 0:
            default_CDF = np.cumsum(temp_df[bad_name]) / sum(temp_df[bad_name])
            undefault_CDF = np.cumsum(
                temp_df[good_name]) / sum(temp_df[good_name])
            ks_value = max(
                abs(default_CDF - undefault_CDF).loc[processed_start_knot:processed_end_knot])
            # the index find here is not the final result, we should find the data's position in the outer data set
            index = getAllindex(
                list(abs(default_CDF - undefault_CDF)), ks_value)
            return temp_df.index[max(index)]
        else:
            return None
    else:
        return None


def best_ks_knots_helper(data, total_len, max_times, good_name, bad_name, rate, start_knot, end_knot, current_time):
    # define the base case
    # here, we should first find out the total length of the raw data. Since the elements in the input data
    # represent the count of unique item in the raw data, thus we need to do some transformation to it to find
    # out the length that we need
    # total_len = sum(data[good_name]) + sum(data[bad_name])
    temp_df = data.loc[start_knot:end_knot]
    temp_len = sum(temp_df[good_name]) + sum(temp_df[bad_name])
    # due to the restriction to the number of elements in the tiny bin
    if temp_len < rate * total_len * 2 or current_time >= max_times:
        return []
    new_knot = best_KS_knot_calculator(
        data, total_len, good_name, bad_name, start_knot, end_knot, rate)
    if new_knot is not None:
        # upper_result = best_ks_knots_helper(data, total_len, max_times, good_name, bad_name, rate, start_knot,
        #                                     new_knot - 1, current_time + 1)
        upper_result = best_ks_knots_helper(data, total_len, max_times, good_name, bad_name, rate, start_knot,
                                            new_knot, current_time + 1)
        lower_result = best_ks_knots_helper(data, total_len, max_times, good_name, bad_name, rate, new_knot + 1,
                                            end_knot, current_time + 1)
    else:
        upper_result = []
        lower_result = []
    return upper_result + [new_knot] + lower_result


def new_ks_auto(data_df, total_rec, piece, rate, good_name, bad_name):
    # call the helper function to finish the following recursion part
    temp_result_list = best_ks_knots_helper(
        data_df, total_rec, piece, good_name, bad_name, rate, 0, len(data_df), 0)
    # since we are gonna to use reconstruct the whole function, thus I choose not to add the two marginal points to the
    # result list
    # temp_result_list = temp_result_list + [0, len(data_df)-1]
    temp_result_list.sort()
    return filter(lambda x: x is not None, temp_result_list)


# the merge function part


# first, we need to define a IV calculator function. The input should be the knots list and the data with unique value's
# black flag count. The result returned by the function will be the IV list of these tiny bins
def IV_calculator(data_df, good_name, bad_name, knots_list):
    # to improve the efficiency of the calculation, I first split the df into a bunch of smaller data frames and put
    # them into a list. Then I Use the map function to do some transformation to calculate the IV value for each small bin
    temp_df_list = []
    for i in range(1, len(knots_list)):
        if i == 1:
            # the data range here we chose to use such format (start, end], since the calculation of CDF is left
            # continuous, thus we need to include the right margin and the left margin should be not included
            # attention: the pd.Series[start:end] is different from pd.DataFrame.loc[start:end]. The previous will not
            # include the end point but the later one will include
            temp_df_list.append(data_df.loc[knots_list[i - 1]:knots_list[i]])
        else:
            temp_df_list.append(
                data_df.loc[knots_list[i - 1] + 1:knots_list[i]])
    total_good = sum(data_df[good_name])
    total_bad = sum(data_df[bad_name])
    good_percent_series = pd.Series(
        list(map(lambda x: float(sum(x[good_name])) / total_good, temp_df_list)))
    bad_percent_series = pd.Series(
        list(map(lambda x: float(sum(x[bad_name])) / total_bad, temp_df_list)))
    # the woe_list here is used for debugging
    woe_list = list(np.log(good_percent_series / bad_percent_series))
    # here, since we want to make sure the woe of the result bins is monotonic, thus we add a justification statement
    # here, if it is not monotonic, then it will be discarded and the return will be None
    if sorted(woe_list) != woe_list and sorted(woe_list, reverse=True) != woe_list:
        return None
    IV_series = (good_percent_series - bad_percent_series) * \
        np.log(good_percent_series / bad_percent_series)
    if np.inf in list(IV_series) or -np.inf in list(IV_series):
        return None
    else:
        return sum(IV_series)


# combination_helper function
def combine_helper(data_df, good_name, bad_name, piece_num, cut_off_list):
    knots_list = list(combinations(cut_off_list, piece_num - 1))
    # here we do some transformation to the knots list, add the start knot and end knot to all the elements in the list
    # knots_list = map(lambda x: sorted(tuple(set(x + (0, len(data_df) - 1)))), knots_list)
    knots_list = map(lambda x: sorted(x + (0, len(data_df) - 1)), knots_list)
    IV_for_bins = map(lambda x: IV_calculator(
        data_df, good_name, bad_name, x), knots_list)
    filtered_IV = list(filter(lambda x: x is not None, IV_for_bins))
    if len(filtered_IV) == 0:
        print('There are no suitable division for the data set with ' +
              str(piece_num) + ' pieces')
        return None
    else:
        if len(getAllindex(IV_for_bins, max(filtered_IV))) > 0:
            target_index = getAllindex(IV_for_bins, max(filtered_IV))[0]
            return knots_list[target_index]
        else:
            return None


# the cut_off_list here should not contain the start knot 0 and end knot len(data_df)-1, since these knots will be added
# in the later process in function's map part
def combine_tiny_bins(data_df, good_name, bad_name, max_piece_num, cut_off_list):
    return_piece_num = min(max_piece_num, len(cut_off_list) + 1)
    if return_piece_num == 1:
        return cut_off_list
    for current_piece_num in sorted(range(2, return_piece_num + 1), reverse=True):
        result_knots_list = combine_helper(
            data_df, good_name, bad_name, current_piece_num, cut_off_list)
        # here we obey the rule that, the function will return the maximum number of bins with maximum IV value, thus if
        # there is no suitable cut_off_list for the current piece, the number of bins will be minus one
        if result_knots_list is not None:
            return result_knots_list
    print("sry, there isn't any suitable division for this data set with the column that you give :(")
    return [0, len(data_df) - 1]


# this function is used for return the import statistical indicators for the binning result
def important_indicator_calculator(data_df, good_name, bad_name, factor_name, knots_list, na_df):
    if len(na_df) != 0:
        total_good = sum(data_df[good_name]) + sum(na_df[good_name])
        total_bad = sum(data_df[bad_name]) + sum(na_df[bad_name])
        na_good_percent = sum(na_df[good_name]) / float(total_good)
        na_bad_percent = sum(na_df[bad_name]) / float(total_bad)
        na_indicator = pd.DataFrame({'Bin': ['NA'], 'KS': [None], 'WOE': [np.log(na_good_percent / na_bad_percent)],
                                     'IV': [
                                         (na_good_percent - na_bad_percent) * np.log(na_good_percent / na_bad_percent)],
                                     'total_count': [sum(na_df[good_name]) + sum(na_df[bad_name])],
                                     'bad_rate': [
                                         float(sum(na_df[bad_name])) / (sum(na_df[good_name]) + sum(na_df[bad_name]))]})
    else:
        total_good = sum(data_df[good_name])
        total_bad = sum(data_df[bad_name])
        na_indicator = pd.DataFrame()
    default_CDF = np.cumsum(data_df[bad_name]) / total_bad
    undefault_CDF = np.cumsum(data_df[good_name]) / total_good
    ks_list = list(
        abs(default_CDF - undefault_CDF).loc[knots_list[:len(knots_list) - 1]])
    temp_df_list = []
    bin_list = []
    for i in range(1, len(knots_list)):
        if i == 1:
            temp_df_list.append(data_df.loc[knots_list[i - 1]:knots_list[i]])
            bin_list.append(
                '(-inf, ' + data_df[factor_name][knots_list[i]] + ']')
        else:
            temp_df_list.append(
                data_df.loc[knots_list[i - 1] + 1:knots_list[i]])
            if i == len(knots_list) - 1:
                bin_list.append(
                    '(' + data_df[factor_name][knots_list[i - 1]] + ', inf)')
            else:
                bin_list.append(
                    '(' + data_df[factor_name][knots_list[i - 1]] + ', ' + str(
                        data_df[factor_name][knots_list[i]]) + ']')
    good_percent_series = pd.Series(
        list(map(lambda x: float(sum(x[good_name])) / total_good, temp_df_list)))
    bad_percent_series = pd.Series(
        list(map(lambda x: float(sum(x[bad_name])) / total_bad, temp_df_list)))
    woe_list = list(np.log(good_percent_series / bad_percent_series))
    IV_list = list((good_percent_series - bad_percent_series) *
                   np.log(good_percent_series / bad_percent_series))
    total_list = list(
        map(lambda x: sum(x[good_name]) + sum(x[bad_name]), temp_df_list))
    bad_rate_list = list(map(lambda x: float(
        sum(x[bad_name])) / (sum(x[good_name]) + sum(x[bad_name])), temp_df_list))
    non_na_indicator = pd.DataFrame({'Bin': bin_list, 'KS': ks_list, 'WOE': woe_list, 'IV': IV_list,
                                     'total_count': total_list, 'bad_rate': bad_rate_list})
    result_indicator = pd.concat(
        [non_na_indicator, na_indicator], axis=0).reset_index(drop=True)
    return result_indicator


# the most significant difference between the two function is the all_information part
# let's redefine this function
def all_information(data_df, na_df, total_rec, piece, rate, factor_name, bad_name, good_name):
    # to get the final result of the binning part, we need two process: split and merge
    split_knots = new_ks_auto(
        data_df, total_rec, piece, rate, good_name, bad_name)
    best_knots = combine_tiny_bins(
        data_df, good_name, bad_name, piece, split_knots)
    return important_indicator_calculator(data_df, good_name, bad_name, factor_name, best_knots, na_df)


# here is the final_outer function
def Best_KS_Bin(flag_name, factor_name, data=pd.DataFrame(), bad_name='bad', good_name='good', piece=5, rate=0.05, min_bin_size=50, not_in_list=[]):
    # print(time.localtime(time.time()))
    # in order to avoid revising the raw data, we choose to copy the current data and contain only the factor and flag
    # columns
    if len(data) == 0:
        print 'Error: there is no data'
        return pd.DataFrame()
    work_data = data.loc[data.index, [factor_name, flag_name]]
    # since the data without flag is meaningless thus, we can use the helper function to help us filer these data
    work_data = verify_df_two(work_data, flag_name)
    if len(work_data) == 0:
        return pd.DataFrame
    # after that, we want to separate the current df into two parts, NA and non-NA
    # the very first thing here should be transforming the type of value in factor_name column into str type
    work_data[factor_name] = work_data[factor_name].astype(str)
    # since there will be the None and nan be transformed into the str type, thus we need to add some default value into
    # the not_in_list, the set here may be redundant
    not_in_list = not_in_list + ['None', 'nan']
    na_df = work_data.loc[work_data[factor_name].apply(
        lambda x: x in not_in_list)]
    non_na_df = work_data.loc[work_data[factor_name].apply(
        lambda x: x not in not_in_list)]
    # generate the grouped_by format which is used for the later process
    na_df = group_by_df(na_df, flag_name, factor_name,
                        bad_name, good_name, True)
    non_na_df = group_by_df(non_na_df, flag_name,
                            factor_name, bad_name, good_name, False)
    print factor_name
    if len(non_na_df) == 0:
        print('sry, there are no data available for separate process :(')
        return pd.DataFrame()
    # total_good = sum(non_na_df[good_name]) + sum(na_df[good_name])
    # total_bad = sum(non_na_df[bad_name]) + sum(na_df[bad_name])
    # total_rec = total_good + total_bad
    total_rec = len(work_data)
    min_bin_size_rate = min_bin_size / float(total_rec)
    min_bin_size_r = max(rate, min_bin_size_rate)
    result = all_information(non_na_df, na_df, total_rec,
                             piece, min_bin_size_r, factor_name, bad_name, good_name)
    # print(time.localtime(time.time()))
    return result


def trans_rdd(data, black_flag):
    """method's help string.
    --------------------------------------------------------------
    trans_rdd:将指标计算代码产出的dataframe转换为可用rdd，为筛选指标做准备

    Parameter Description

    data:指标计算代码产出的dataframe
    black_flag:标签列列名
    --------------------------------------------------------------
    Return:转换后的rdd
    --------------------------------------------------------------
    """.encode("utf8")
    def todict1(x):
        x["i_cnt_relate_"].update(x["m_cnt_relate_"])
        x["i_cnt_relate_"].update({black_flag: x[black_flag]})
        return x["i_cnt_relate_"]

    def todict2(x):
        x["id_value_stats"].update(x["mobile_value_stats"])
        x["id_value_stats"].update({black_flag: x[black_flag]})
        return x["id_value_stats"]

    def fillna(x):
        for _key in x.keys():
            if x[_key]:
                pass
            else:
                x[_key] = "-999"
        return x

    if "i_cnt_relate_" in data.columns:
        data_rdd = data.rdd.map(lambda x: todict1())
    else:
        data_rdd = data.rdd.map(lambda x: todict2())

    data_rdd = data_rdd.map(lambda x: fillna(x))
    data_df = data_rdd.toDF()

    columns = data_df.columns
    rdd_columns = sc.parallelize([tuple(columns)])
    rdd_tuple = rdd_columns + data_df.rdd.map(tuple)

    rdd_add_index = rdd_tuple.zipWithIndex().flatMap(
        lambda x: [(x[1], k[0], k[1]) for k in enumerate(x[0])])
    rdd_groupby_index = rdd_add_index.map(lambda x: (
        x[1], (x[0], x[2]))).groupByKey().sortByKey()
    rdd_combine = rdd_groupby_index.map(lambda x: sorted(
        list(x[1]), cmp=lambda k1, k2: cmp(k1[0], k2[0])))
    rdd_transed = rdd_combine.map(lambda x: map(lambda y: y[1], x))
    rdd_final = rdd_transed.map(lambda x: (x[0], x[1:]))
    return rdd_final


def feature_select(*args, **kwargs):
    """method's help string.
    ------------------------------------------------------------------
    feature_select:通过单一阈值和iv筛选指标，其中iv为best_ks分bin后计算的iv

    Parameter Description

    data:指标计算代码产出的dataframe
    black_flag:y标签列名称,默认"label"
    piece:每个特征分bin个数
    rate:每bin最小样本数占比
    min_bin_size:每bin最小样本数
    not_in_list:空值列表,在列表中的值会被认为空值
    ------------------------------------------------------------------
    Return:一个pandas dataframe 包括了每个特征的变量名,单一阈值和iv
    ------------------------------------------------------------------
    """.encode("utf8")

    def select(x):
        if x[0] != kwargs.get('black_flag', "label"):
            t = pd.DataFrame(x[1])
            sample = pd.concat([y, t], axis=1)
            sample.columns = [kwargs.get('black_flag', "label"), x[0]]
            result = {}
            result['var'] = x[0]
            percent = sample[x[0]].value_counts(normalize=True, dropna=False)
            result['single_threshold'] = percent.max()
            var_stat = Best_KS_Bin(kwargs.get('black_flag', "label"), x[0],
                                   sample, 'bad', 'good', kwargs.get(
                                       'piece', 5),
                                   kwargs.get('rate', 0.05), kwargs.get(
                                       'min_bin_size', 50),
                                   kwargs.get('not_in_list', ['None', 'NaN', 'NA', 'nan', None, "-999", u"-999"]))
            if type(var_stat) == type:
                result['iv'] = 'nan'
            else:
                if len(var_stat) > 0:
                    if len(var_stat['WOE']) != len(set(var_stat['WOE'])):
                        var_stat.ix[var_stat['Bin'] == 'NA',
                                    'WOE'] = var_stat.ix[var_stat['Bin'] == 'NA', 'WOE'] + 0.0000001
                    var_stat['var'] = x[0]
                    result['iv'] = sum(var_stat['IV'])
                else:
                    result['iv'] = 'nan'
            return result
    y = args[0][[kwargs.get('black_flag', "label")]].toPandas()
    rdd_final = trans_rdd(args[0], kwargs.get('black_flag', "label"))
    result = rdd_final.map(lambda x: select(x)).collect()
    result = filter(lambda x: x != None, result)
    sort_result = sorted(result, cmp=lambda k1, k2: cmp(
        k1['iv'], k2['iv']), reverse=True)
    index_iv = pd.DataFrame(sort_result)
    return index_iv


def get_csv(data, path, select_col, update_col=None, overwrite=False):
    """method's help string.
    ------------------------------------------------------------------
    get_csv:在单一阈值和iv筛选后，需要保留的特征

    Parameter Description

    data:指标计算代码产出的dataframe
    select_col:被选中的指标，可接受series或list
    update_col:在data中，除了指标外其他需要获取的列，默认为None，获取除指标外所有列
    path:hdfs路径
    overwrite:是否覆盖写入，默认False
    ------------------------------------------------------------------
    Return:一个pandas dataframe 包括了每个特征的变量名,单一阈值和iv
    ------------------------------------------------------------------
    """.encode("utf8")

    def todict(x, column1, column2):
        x[column1].update(x[column2])
        if update_col:
            x[column1].update({_: x[_] for _ in update_col})
        else:
            pass
        return x[column1]

    def fillna(x):
        for _key in x.keys():
            if x[_key]:
                pass
            else:
                x[_key] = "-999"
        return x

    if update_col:
        pass
    else:
        update_col = data.columns
        if "i_cnt_relate_" in data.columns:
            update_col.pop(update_col.index("i_cnt_relate_"))
            update_col.pop(update_col.index("m_cnt_relate_"))
        else:
            update_col.pop(update_col.index("id_value_stats"))
            update_col.pop(update_col.index("mobile_value_stats"))

    if "i_cnt_relate_" in data.columns:
        data_rdd = data.rdd.map(lambda x: todict(
            x, "i_cnt_relate_", "m_cnt_relate_"))
    else:
        data_rdd = data.rdd.map(lambda x: todict(
            x, "id_value_stats", "mobile_value_stats"))

    data_rdd = data_rdd.map(lambda x: fillna(x))
    data_df = data_rdd.toDF()

    data_df_select = data_df.select(update_col + list(select_col))
    if overwrite:
        data_df_select.write.parquet(path, "overwrite")
    else:
        data_df_select.write.parquet(path)

    print u"数据已经写入%s" % (path)
