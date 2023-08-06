from ..default import *

# def t_test(values):
#     values = np.array(values)
#     if len(values)==2:
#         t,pv = scipy.stats.ttest_rel(values[0],values[1])
#         return pv,t
#     else:
#         return None

def t_test(values):
    a,b = values
    result = scipy.stats.ttest_rel(a,b)
    return result

def permutation_test(values,reps=1000):
    values = np.array(values)
    if len(values)==2:
        pv,t = two_sample(values[0],values[1], reps=reps,stat=lambda u,v: mean(u-v),alternative='two-sided')
        return pv,t
    else:
        return None

def permutation_on_condition(data,method,shuffle_count=1000):
    def condition_shuffled(data):
        group_labels = list(data.index.get_level_values(level='cond_group'))
        random.shuffle(group_labels)
        data.index = data.index.set_labels(group_labels,level='cond_group')
        return data
    # keep
    val_raw = method(data)

    # shuffle
    baseline =[]
    for i in range(shuffle_count):
        val_shuffled = method(condition_shuffled(data))
        baseline.append(val_shuffled)

    baseline.append(2) # correction
    baseline.append(val_raw)
    baseline.sort()

    pv = 1-baseline.index(val_raw)/shuffle_count

    return pv,None

def fdr(pvs):
    re_calc = lambda v: statsmodels.sandbox.stats.multicomp.multipletests(v, 0.05, 'fdr_bh')[1]
    if type(pvs) is pd.DataFrame:
        fdr = [re_calc(i) for i in pvs.values]
        pvs_new = pd.DataFrame(fdr, index=pvs.index, columns=pvs.columns)
    elif type(pvs) is pd.Series:
        fdr = re_calc(pvs.values)
        pvs_new = pd.Series(fdr, index=pvs.index, name=pvs.name)
    elif type(pvs) is dict:
        fdr = re_calc(pvs.values())
        pvs_new = dict(zip(pvs.keys(),fdr))
    elif type(pvs) is list:
        pvs_new = re_calc(pvs)
    else:
        raise ValueError('Only support pd.DataFrame, pd.Series,dict, and list')
    return pvs_new

def anova():
    pass

def similarity():
    pass

def classifier():
    pass            