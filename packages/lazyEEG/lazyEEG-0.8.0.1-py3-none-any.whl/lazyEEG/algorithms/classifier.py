from ..default import *
from .. import group
from .general import * 
from ..graph import put as plot_put
from ..statistics import process
from ..statistics import test

from tqdm import tqdm

import sklearn
from sklearn import linear_model
from sklearn.svm import SVC
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import roc_auc_score
from sklearn.metrics import accuracy_score

def condition_shuffled(data):
    group_labels = list(data.index.get_level_values(level='cond_group'))
    random.shuffle(group_labels)
    data.index = data.index.set_labels(group_labels,level='cond_group')
    return data

def run_model(X,Y,model,fold,test_size):
    score_train_folds = []
    score_test_folds = []
    coef_folds = []
    for train_index, test_index in StratifiedShuffleSplit(fold, test_size=test_size).split(X, Y):
        model.fit(X[train_index], Y[train_index])
        if getattr(model,'predict_proba', None):
            prob_train = model.predict_proba(X[train_index])[:,1]
            prob_test = model.predict_proba(X[test_index])[:,1]
        else:
            prob_train = model.decision_function(X[train_index])
            prob_test = model.decision_function(X[test_index])

        score_train_folds.append(roc_auc_score(Y[train_index],prob_train))
        score_test_folds.append(roc_auc_score(Y[test_index],prob_test))
        try:
            coef_folds.append(model.coef_[0]) # weights
        except:
            coef_folds.append(0)
    return score_train_folds,score_test_folds,coef_folds

model = linear_model.LogisticRegression(class_weight="balanced")


# 0904 version
from sklearn.decomposition import PCA
def Classifier(data,groups,step='1ms',win='1ms',sample='mean', model=model,permute_baseline=False,pca=False,feature = lambda x:x,fold=30,test_size=0.3):
    # [parameters example]
    # groups: ['TtG&FfG,FtG&FfG @ @ 120ms,160ms','TtG&baseG @ @ 0ms,300ms,1ms']
    # data: todo 
    # return: todo

    # average level=['subject','channel','trial','cond_group']
    def calc(data_in_condition):
        data_in_condition = data_in_condition.groupby(level=['subject','channel','trial','cond_group']).mean()['data']
        if step!='1ms':
            data_in_condition = point_sample(data_in_condition,step)
        elif win!='1ms':
            data_in_condition = window_sample(data_in_condition,win,sample)

        data_in_condition = data_in_condition.unstack('channel')
        
        return data_in_condition
    
    # group the data
    data_groups = group.extract(data,groups,'MVPA')

    pval_groups_data = []
    score_groups_data = []
    info_groups_data = []
    for title,group_data in data_groups:
        pval_group_data = []
        score_group_data = []
        info_group_data = []

        # for compr_name,compr_data in group_data.groupby(level='condition'):
        for compr_name,compr_data in group_data:
            classN = len(compr_data.index.get_level_values('cond_group').unique())
            datasets = calc(compr_data)

            pvs = pd.Series(name=compr_name)
            score_detail = []
            info = {'score':dict(),'std':dict(),'variance':dict(),'coef':dict()}
            for tp,tp_data in tqdm(datasets.stack('time').groupby(level=['time']),ncols=0):
                score_subjects = []
                variance_subjects = [] # training error - test error, high variance means overfitting
                std_subjects = [] # standard deviation of test error
                coef_subjects = []
                baselines = []
                for subject,samples in tp_data.groupby(level=['subject']):
                    X = sklearn.preprocessing.scale(samples)
                    if pca:
                        pca = PCA(svd_solver='randomized', whiten=True).fit(X)
                        X = pca.transform(X)
                    # X = sklearn.preprocessing.minmax_scale(X,axis=1)
                    # X = feature(X)
                    Y = np.array(samples.index.labels[2]) # index of cond_group

                    score_train_folds,score_test_folds,coef_folds = run_model(X,Y,model,fold,test_size)

                    score_subjects.append(np.mean(score_test_folds))
                    variance_subjects.append(np.mean(score_train_folds)-np.mean(score_test_folds))
                    std_subjects.append(np.std(score_test_folds))
                    coef_subjects.append(np.mean(coef_folds,axis=0))

                    if permute_baseline:
                        baseline = np.mean([run_model(X,np.random.permutation(Y),model,fold,test_size)[1] for i in range(3)])
                        baselines.append(baseline)
                    else:
                        baselines.append(1/classN)

                # pval
                pv = two_sample(score_subjects,baselines, reps=1000,stat=lambda u,v: np.mean(u-v),alternative='greater')[0]
                pvs.set_value(tp,pv)
                # score
                score_detail.append(pd.Series(score_subjects,name=tp))
                # other
                tp_name = (tp/np.timedelta64(1, 'ms')).astype(int)
                info['score'][tp_name] = float("%.4f" %np.mean(score_subjects))
                info['variance'][tp_name] = float("%.4f" %np.mean(variance_subjects))
                info['std'][tp_name] = float("%.4f" %np.mean(std_subjects))
                info['coef'][tp_name] = np.around(np.mean(coef_subjects,axis=0), decimals=3)

            pval_group_data.append(pvs)
            score_group_data.append((compr_name,pd.DataFrame(score_detail).T))
            info_group_data.append((compr_name,pd.DataFrame(info)))

        pval_groups_data.append((title,pd.DataFrame(pval_group_data)))
        score_groups_data.append((title,score_group_data))
        info_groups_data.append((title,info_group_data))

    return {'p':pval_groups_data,'score':score_groups_data,'other':info_groups_data}
