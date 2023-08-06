from ..default import *
from tqdm import tqdm
from ..statistics import stats_methods

# todo: group single or not, 2*2 or not
def check_availability(data,single_value_level=[],complex_value_level=[]):
    for l in single_value_level:
        if l == 'time_group':
            values = list(data.columns.get_level_values(l).unique())
        else:
            values = list(data.index.get_level_values(l).unique())
        if len(values)>1:
            raise Exception(f'level "{l}" should have only one value, but {values} in there.')
    for l in complex_value_level:
        if l == 'time_group':
            values = list(data.columns.get_level_values(l).unique())
        else:
            values = list(data.index.get_level_values(l).unique())
        if len(values)==1:
            raise Exception(f'level "{l}" should have more than one value, but {values} in there.')

'sampling'
def point_sampling(df, step_size):
    if step_size[-2:] in ['ms','Ms','MS'] and step_size[:-2].isdigit():
        step_size = step_size[:-2]+'N'
    else:
        raise Exception('step_size should be a string formatted as "10ms" or "2ms"')

    new_df = []
    for idx,group_data in df.groupby(axis=1,level='time_group'):
        old_tps = [pd.Timedelta(tp) for tp in group_data.columns.levels[1]]
        tp_indexs = [old_tps.index(tp) for tp in pd.timedelta_range(old_tps[0], old_tps[-1], freq=step_size) if tp in old_tps]
        group_data = group_data.iloc[:,tp_indexs]
        new_df.append(group_data)
    new_df = pd.concat(new_df,axis=1)

    return new_df

def window_sampling(df, win_size, sample='mean'):
    if win_size[-2:] in ['ms','Ms','MS'] and win_size[:-2].isdigit():
        win_size = win_size[:-2]+'N'
    else:
        raise Exception('win_size should be a string formatted as "20ms" or "5ms"')

    new_df = []
    for idx,group_data in df.groupby(axis=1,level='time_group'):
        group_data.columns.set_levels([pd.Timedelta(tp) for tp in group_data.columns.levels[1]], level=1, inplace=True)
        group_data_new = group_data.resample(win_size, axis=1, how='mean', level=1)
        group_data_new.columns = group_data_new.columns + pd.Timedelta(win_size[:-1]+'ns')/2 # loffset of `resample` doesn't work, so I add this line 
        if group_data_new.columns[-1]>group_data[0].columns[-1]:
            del group_data_new[group_data_new.columns[-1]]
        group_data_new.columns = pd.MultiIndex.from_product([[idx], group_data_new.columns.values.tolist()],names=['time_group','time'])
        new_df.append(group_data_new)

    new_df = pd.concat(new_df,axis=1)

    return new_df

def sampling(data,step_size='1ms',win_size='1ms',sample='mean'):
    if step_size!='1ms':
        data = point_sampling(data, step_size)
    elif win_size!='1ms':
        data = window_sampling(data, win_size, sample=sample)
    return data

'map and apply'
def roll_on_levels(df, func, arguments_dict=None, levels='time', between='condition_group', in_group='subject',prograssbar=True):
    disable_prograssbar = (not prograssbar)
    col_level = df.columns.names[1]
    df = df.stack(col_level)
    result = []
    group_ids = []

    for group_id,group_data in df.groupby(level=levels):
        data_subjects = [group_data.mean(level=in_group).mean(axis=1) 
            for group_id,group_data in group_data.groupby(level=between)]
        
        result_one_group = func(data_subjects)
        
        re_add_name = group_data.index.get_level_values(between)[0][2:]
        
        group_ids.append(group_id)
        result.append(result_one_group)

    if type(levels)==str or len(levels)==1:
        index = pd.Index(group_ids, name=levels)
        # print(index)
    else:
        index = pd.MultiIndex.from_tuples(group_ids, names=levels)

    result = pd.DataFrame(result, index=index)
    
    recover_index(result, group_data, between)
   
    return result.unstack(col_level)

def stats_compare(df, comparison, levels='time', between='condition_group', in_group='subject'):
    condition_groups = df.index.get_level_values(between).unique()
    if comparison['sig_limit']>0 and len(condition_groups)==2:
        if comparison['win']!='1ms':
            df = window_sampling(df, comparison['win'], comparison['method'])
        stats_result = roll_on_levels(df, comparison['test'], levels=levels, between=between, in_group=in_group)
        pval_result = stats_result['pvalue']
        if comparison['need_fdr']: pval_result = stats_methods.fdr(pval_result)
        return pval_result
    else:
        return None

def add_index(df, name, value):
    df[name] = value
    df.set_index(name, append=True, inplace=True)

def recover_index(df, old_df, name):
    if '_group' in name:
        values = old_df.index.get_level_values(name).map(lambda x: '0 '+' '.join(x.split(' ')[1:])).unique()
    else:
        values = old_df.index.get_level_values(name).unique()
    if len(values)==1: # make sure if the value in old_df index is unique'
        value = values[0]
    else:
        value = ','.join(values)
        # raise Exception(f'The values in level {name} should be unique')
    add_index(df, name, value)

# def subtract(data,index):
#     # part1 = data.query('%s=="+"' %index)
#     # part1.index = part1.index.droplevel(index)
#     part1 = data.xs('+',level=index) # speed++
#     try:
#         part2 = data.xs('-',level=index)
#         result = part1.subtract(part2,fill_value=0)
#     except:
#         result = part1
#     return result

# # remove certain axis
# def mean_axis(df, axis_to_mean):
#     level = list(np.setdiff1d(df.index.names, axis_to_mean))
#     return df.mean(level=level)

