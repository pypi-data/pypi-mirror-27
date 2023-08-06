from ..default import *
from .. import group
from .general import * 
from ..graph import put as plot_put
from ..statistics import process
from ..statistics import test

from tqdm import tqdm
from scipy.spatial.distance import cosine

def calc_cosD(data):
    a,b = np.array(data)
    return (2*cosine(a,b))**0.5
        
def condition_shuffled(data, group_labels):
    random.shuffle(group_labels)
    data.index = data.index.set_labels(group_labels,level='cond_group')
    return data

def Topo_CosD(data,container,step='1ms',err_style='ci_band',win='5ms',sample='mean', sig_limit=0):

    def calc(batch_data):

        def sub_task(scene_data):
            scene_data = mean_axis(scene_data,'trial')
            # sampling along time axis
            if step!='1ms':
                scene_data = point_sample(scene_data,step)
            elif win!='1ms':
                scene_data = window_sample(scene_data,win,sample)

            distance = process.row_roll(scene_data, row=['subject','condition','time'], column=['channel'], func=calc_cosD)

            return distance['p'].unstack('time')

        map_result = [(scene_name,sub_task(scene_data)) for scene_name,scene_data in batch_data]

        result = pd.concat([result for name,result in map_result])
        result.sort_index(inplace=True)
        result = result.reindex([name for name,result in map_result],level='condition') # 使condition的顺序和定义时一致

        return result

    # group the data
    container_data = group.extract(data,container,'Topograph')
    # calculate
    diff_data = [(title,calc(batch_data)) for title,batch_data in container_data]
    diff_stat_data = [None for i in diff_data]

    # plot
    note = ['Time(ms)','Distance',[]]
    plot_put.block(diff_data,note,err_style,diff_stat_data,win,sig_limit=0)

    return diff_data, diff_stat_data

def CosineD_dynamics(data,container,step='1ms',win='20ms',sample='mean',shuffle=500):
    def calc_cosD_2(data):
        data_mean = mean_axis(data,'trial')
        return calc_cosD(data_mean)

    def calc(batch_data):
        def sub_task(scene_data):
            # sampling along time axis
            if step!='1ms':
                scene_data = point_sample(scene_data,step)
            elif win!='1ms':
                scene_data = window_sample(scene_data,win,sample)

            result = process.row_roll(scene_data, row=['subject','condition','time'], column=['channel'],
                                        func=test.permutation_on_condition, **{'method':calc_cosD_2,'shuffle_count':shuffle})
            return result['p']

        map_result = [(scene_name,sub_task(scene_data)) for scene_name,scene_data in batch_data]

        result = pd.concat([result for name,result in map_result])
        result.sort_index(inplace=True)
        result = result.reindex([name for name,result in map_result],level='condition') # 使condition的顺序和定义时一致

        return result

    # group the data
    container_data = group.extract(data,container,'Topograph')
    # calculate
    topo_data = [(title,calc(batch_data)) for title,batch_data in container_data]

    return topo_data

# 1. calc the raw cosD
# 2. repeat to make cosD distribution (baselines)
#     2.1 shuffling (in [each subject]/[all subjects])
#     2.2 averaging the all
#     2.3 calc the cosD
# 3. permutation test -- where is the raw cosD rank in the distribution
def TANOVA1(data,container,step='1ms',win='1ms',sample='mean',shuffle=500,shuffleInSubj=True):

    def calc(batch_data):
        def sub_task(scene_data):
            # sampling along time axis
            if step!='1ms':
                scene_data = point_sample(scene_data,step)
            elif win!='1ms':
                scene_data = window_sample(scene_data,win,sample)

            pvs = pd.DataFrame()
            pvs.columns.name='time'
            pvs.index.name='condition'
            for index,index_data in tqdm(scene_data.stack('time').unstack(['channel']).groupby(level=['condition','time']),ncols=0):
                dist_raw = calc_cosD(mean_axis(index_data,['subject','trial'])) # calc the raw cosD
                dist_baseline = []

                if shuffleInSubj:
                    datas_and_labels = [(subj_data, list(subj_data.index.get_level_values(level='cond_group')))
                                     for subj_name,subj_data in index_data.groupby(level='subject')]
                    for i in range(shuffle):
                        shuffled = pd.concat([condition_shuffled(subj_data,group_labels) for subj_data,group_labels in datas_and_labels])
                        t_baseline = mean_axis(shuffled,['subject','trial']) # remove certain axis
                        dist_baseline.append(calc_cosD(t_baseline))
                else:
                    group_labels = list(index_data.index.get_level_values(level='cond_group'))
                    for i in range(shuffle):
                        shuffled = condition_shuffled(index_data,group_labels)
                        t_baseline = mean_axis(shuffled,['subject','trial']) # remove certain axis
                        dist_baseline.append(calc_cosD(t_baseline))

                dist_baseline.append(dist_raw)
                dist_baseline.append(2)
                dist_baseline.sort()
                pvs.set_value(index[0],index[1],1-dist_baseline.index(dist_raw)/shuffle)
            return pvs

        map_result = [(scene_name,sub_task(scene_data)) for scene_name,scene_data in batch_data]

        result = pd.concat([result for name,result in map_result])
        result.sort_index(inplace=True)
        result = result.reindex([name for name,result in map_result]) # 使condition的顺序和定义时一致
        return result

    # group the data
    container_data = group.extract(data,container,'TANOVA')
    # calculate
    topo_data = [(title,calc(batch_data)) for title,batch_data in container_data]

    return {'p':topo_data}

# 1. grand-average, calculate the CosD
# 2. average in each subject
# 3. shuffle 500
#      calculate CosD
# 4. the baseline CosD in 500 shuffling become a baseline distribution, 
#      then run permutation test
def TANOVA3(data,container,step='1ms',win='1ms',sample='mean',shuffle=500):

    def calc(batch_data):
        def sub_task(scene_data):
            # sampling along time axis
            if step!='1ms':
                scene_data = point_sample(scene_data,step)
            elif win!='1ms':
                scene_data = window_sample(scene_data,win,sample)

            pvs = pd.DataFrame()
            pvs.columns.name='time'
            pvs.index.name='condition'
            for index,index_data in tqdm(scene_data.stack('time').unstack(['channel']).groupby(level=['condition','time']),ncols=0):
                dist_raw = calc_cosD(mean_axis(index_data,['subject','trial'])) # calc the raw cosD
                dist_baseline = []

                data_of_subjects = mean_axis(index_data,['trial'])
                # data_of_subjects = mean_axis(data_of_subjects,['chan_group','chan_sign','cond_sign'])
                group_labels = list(data_of_subjects.index.get_level_values(level='cond_group'))

                for i in range(5):
                    shuffled = condition_shuffled(data_of_subjects, group_labels)
                    t_baseline = mean_axis(shuffled,['subject']) # remove certain axis
                    dist_baseline.append(calc_cosD(t_baseline))
                    # print(t_baseline['data'].iloc[:,:3])
                    # print(data['data'].iloc[:,:3])
                
                dist_baseline.append(dist_raw)
                dist_baseline.append(2)
                dist_baseline.sort()
                print(dist_raw)
                print(dist_baseline)
                pvs.set_value(index[0],index[1],1-dist_baseline.index(dist_raw)/shuffle)
            return pvs

        map_result = [(scene_name,sub_task(scene_data)) for scene_name,scene_data in batch_data]

        result = pd.concat([result for name,result in map_result])
        result.sort_index(inplace=True)

        result = result.reindex([name for name,result in map_result]) # 使condition的顺序和定义时一致

        return result
        

    # group the data
    container_data = group.extract(data,container,'TANOVA')
    # calculate
    topo_data = [(title,calc(batch_data)) for title,batch_data in container_data]

    return {'p':topo_data}

# def TANOVA1(data,container,step='1ms',win='1ms',sample='mean',shuffle=500,shuffleInSubj=True):
#     def calc_cosD(data):
#         a,b = np.array(data)
#         return (2*cosine(a,b))**0.5

#     def condition_shuffled(data):
#         group_labels = list(data.index.get_level_values(level='cond_group'))
#         random.shuffle(group_labels)
#         data.index = data.index.set_labels(group_labels,level='cond_group')
#         return data

#     def calc(batch_data):
#         # sampling along time axis
#         if step!='1ms':
#             batch_data = point_sample(batch_data,step)
#         elif win!='1ms':
#             batch_data = window_sample(batch_data,win,sample)

#         pvs = pd.DataFrame()
#         pvs.columns.name='time'
#         pvs.index.name='condition'
#         for index,index_data in tqdm(batch_data.stack('time').unstack(['channel']).groupby(level=['condition','time']),ncols=0):
#             dist_raw = calc_cosD(mean_axis(index_data,['subject','trial'])) # calc the raw cosD
#             dist_baseline = []
#             for i in range(shuffle):
#                 if shuffleInSubj:
#                     shuffled = pd.concat([condition_shuffled(subj_data) for subj_name,subj_data in index_data.groupby(level='subject')])
#                 else:
#                     shuffled = condition_shuffled(index_data)
#                 t_baseline = mean_axis(shuffled,['subject','trial']) # remove certain axis
#                 dist_baseline.append(calc_cosD(t_baseline))

#             dist_baseline.append(dist_raw)
#             dist_baseline.append(2)
#             dist_baseline.sort()
#             pvs.set_value(index[0],index[1],1-dist_baseline.index(dist_raw)/shuffle)
#         return pvs

#     # group the data
#     container_data = group.extract(data,container,'Topograph')
#     # calculate
#     topo_data = [(title,calc(batch_data)) for title,batch_data in container_data]

#     return {'p':topo_data}

# In each subject:
#     1. calc the raw cosD
#     if AvergThenCosD:
#        2. shuffling to make baselines' distribution
#        3. averaging the baselines, then calc cosD
#     if CosDThenAverg:
#        2. shuffling to make cosD distribution (baselines)
#        3. averaging the cosD distribution
# t-test -- compare the raw cosDs and shuffled cosDs

def TANOVA2(data,container,step='1ms',win='1ms',sample='mean',shuffle=500,AvergThenCosD=True):
    def calc_cosD(data):
        a,b = np.array(data)
        return (2*cosine(a,b))**0.5

    def condition_shuffled(data):
        group_labels = list(data.index.get_level_values(level='cond_group'))
        random.shuffle(group_labels)
        data.index = data.index.set_labels(group_labels,level='cond_group')
        return data

    def calc(batch_data):
        # sampling along time axis
        if step!='1ms':
            batch_data = point_sample(batch_data,step)
        elif win!='1ms':
            batch_data = window_sample(batch_data,win,sample)

        pvs = pd.DataFrame()
        pvs.columns.name='time'
        pvs.index.name='condition'
        for index,index_data in tqdm(batch_data.stack('time').unstack(['channel']).groupby(level=['condition','time']),ncols=0):
            # print(index, end=".")
            dist_raw = []
            dist_baseline = []
            for subject_index,subject_data in index_data.groupby(level='subject'):
                # keep
                dist_raw.append(calc_cosD(mean_axis(subject_data,'trial')))
                # shuffle
                if AvergThenCosD:
                    shuffled_baselines = []
                    for i in range(shuffle):
                        t_baseline = mean_axis(condition_shuffled(subject_data),'trial')
                        shuffled_baselines.append(np.array(t_baseline))
                    shuffled_baseline = np.mean(shuffled_baselines,0)

                    dist_baseline.append(calc_cosD(shuffled_baseline))
                else:
                    shuffled_baselines = [calc_cosD(mean_axis(condition_shuffled(subject_data),'trial')) 
                            for i in range(shuffle)]
                    dist_baseline.append(np.mean(shuffled_baselines))

            pvs.set_value(index[0],index[1],test.t_test([dist_raw,dist_baseline])[0])

        # index = pd.MultiIndex.from_tuples(list(pvs.keys()), names=['condition','time'])
        return pvs

    # group the data
    container_data = group.extract(data,container,'Topograph')
    # calculate
    topo_data = [(title,calc(batch_data)) for title,batch_data in container_data]

    return {'p':topo_data}





'''
[old method]:
1. calculate similarity of everyone, average them as real similarity
2. shuffle 1000
     calculate similarity of everyone, average them as baseline similarity
3. the baseline similarities in 1000 shuffling become a baseline distribution, 
     then run permutation test



[now method]:
In each subject:
    1. calculate similarity of everyone, average them as real similarity
    2. shuffle 1000
         calculate baseline similarity of everyone 
       they will be distribution, then run permutation test 

[new method todo]:
In each subject:
    1. calculate similarity of everyone, average them as real similarity
    2. shuffle 1000
         calculate similarity of everyone, average them as baseline similarity
t-test the real similarity and baseline similarity

# TANOVA1
In each subject:
    1. calc the raw cosD
    2. shuffling to make cosD distribution (baselines)
    3. averaging the cosD distribution
3. t-test -- compare the raw cosDs and shuffled cosDs
'''


# def topo_similarity(data,groups,span,win):
#     groups = GroupsDefinition(groups)
#     mix_conds = [i[0] for i in groups[0][0].values()]
#     data_in_condA = [[trial['data_in_wins'] for name,trial in sub.groupby('trial')] 
#                      for name,sub in data[data.cond.isin(mix_conds[0])].groupby('sub')]
#     data_in_condB = [[trial['data_in_wins'] for name,trial in sub.groupby('trial')] 
#                      for name,sub in data[data.cond.isin(mix_conds[1])].groupby('sub')]
    
#     def cosD(A,B):
#          return (2*cosine(A,B))**0.5
        
#     Pv_result = []
#     for tp in range(span[0],span[1],win):
#         index = tp//win
#         data_in_span_condA = [[[d[index] for d in trial] for trial in sub] for sub in data_in_condA]
#         data_in_span_condB = [[[d[index] for d in trial] for trial in sub] for sub in data_in_condB]    
#         erp_count = [[len(sub_A),len(sub_B)] for sub_A,sub_B in zip(data_in_condA,data_in_condB)] 
        
#         erp_in_conds = [[np.array(sub_A).mean(0),np.array(sub_B).mean(0)] for sub_A,sub_B in zip(data_in_span_condA,data_in_span_condB)] 
#         t = np.array(erp_in_conds).mean(0)
#         real = cosD(t[0,:],t[1,:])
        
#         data_for_permutation = [np.array(sub_in_condA + sub_in_condB) for sub_in_condA,sub_in_condB in zip(data_in_span_condA,data_in_span_condB)]
        
#         shuffle_count = 1000
#         cosineD_shuffled =[]
#         for i in range(shuffle_count):
#             cond1_in_sub =[]
#             cond2_in_sub =[]
#             for sub,[A_count,B_count] in zip(data_for_permutation,erp_count):
#                 samples = np.arange(A_count+B_count)
#                 numpy.random.shuffle(samples)
#                 samplesA = samples[:A_count]
#                 samplesB = samples[A_count:]
#                 erp1 = sub[samplesA,:].mean(0)
#                 erp2 = sub[samplesB,:].mean(0)
#                 cond1_in_sub.append(erp1)
#                 cond2_in_sub.append(erp2)
#             cosineD_shuffled.append(cosD(np.array(cond1_in_sub).mean(0),np.array(cond2_in_sub).mean(0)))

#         cosineD_shuffled.append(2) # correction
#         cosineD_shuffled.append(real)
#         cosineD_shuffled.sort()
#         Pv_result.append(1-cosineD_shuffled.index(real)/shuffle_count)

#     return Pv_result
