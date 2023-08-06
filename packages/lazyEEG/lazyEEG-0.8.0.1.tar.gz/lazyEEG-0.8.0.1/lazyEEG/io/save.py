from ..default import *

def save_epochs(epochs, filepath, append=False):
    if append:
        mode = 'a'
    else:
        mode = 'w'
    if not filepath.endswith('.h5'):
        print('Your file have been added ".h5" as the extension name.')
        filepath += '.h5'

    '''for a unknown bug of pd.HDFStore. del it here and in load.py--load_dataframe_hdf5() if fixed'''
    t = epochs.info['trials']
    del epochs.info['trials']
    ''''''

    with pd.HDFStore(filepath, mode) as store:
        for subj_id,subj_data in epochs.all.groupby(level=['subject']):
            subj_id = str(subj_id)
            print('saving',subj_id,'...')
            store[subj_id] = subj_data
            store.get_storer(subj_id).attrs['info'] = epochs.info

    '''for a unknown bug of pd.HDFStore. del it here and in load.py--load_dataframe_hdf5() if fixed'''
    epochs.info['trials'] = t
    ''''''

    print('Done.')
