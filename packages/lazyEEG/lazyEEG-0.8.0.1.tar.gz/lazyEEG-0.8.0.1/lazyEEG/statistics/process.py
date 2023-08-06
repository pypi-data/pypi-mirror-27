from ..default import *
from tqdm import tqdm

# df is pandas.DataFrame:
# - rows: [subject,condition,channel]
# - columns: time 

# def roll_on_time(df, sub_group, func, **arguments):
#     result = []
#     timebin_ids = []
#     for timebin_id,timebin in tqdm(df.groupby(level='time',axis=1),ncols=0):
#         data = [cond_data.get_values().flatten() for cond_id,cond_data in timebin.groupby(level=sub_group)]
#         result_one_time = func(data)
#         timebin_ids.append(timebin_id)
#         result.append(result_one_time)
#     return pd.DataFrame(result, index=timebin_ids)

# def row_roll(df,row,column,func,**arguments):
#     pvs = dict()
#     others = dict()

#     for index,data in tqdm(df.stack('time').unstack(column).groupby(level=row),ncols=0):
#         result = func(data,**arguments)
#         if type(result) not in [list,tuple]:
#             pvs[index] = result
#             others[index] = None
#         else:
#             pv,*other = result
#             pvs[index] = pv
#             others[index] = other
        
#     if len(row)>1:
#         index = pd.MultiIndex.from_tuples(list(pvs.keys()), names=row)
#         return {'p':pd.Series(pvs,index=index),'other':pd.Series(others,index=index)}
#     else:
#         return {'p':pd.Series(pvs),'other':pd.Series(others)}

def parallel():
    pass
