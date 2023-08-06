Aim；
Simplifying the analysis
- For beginners: clear logics for the steps (least concepts);
- For data players (who want to check various aspects of data or to try various analysis algorithms): one-line code for each idea;
- For data players (who want to apply DIY analysis methods): plenty of low/high level functions for quickly building your own algorithm.

Advantages:
- Don't need to extract the data in a messy way when you want to do new analysis. You can just use a string or a dictionary to describe the target now.
- Applying EEG analysis method by one-line code. (ERP, topography, specturm, time-frequency, etc.)
- Applying advanced EEG analysis methods (clustering, classification, etc.)
- Beautiful ploting
- Plenty of basic and advanced APIs which can help to build your own analysis algorithm and to visualize the result.


---
# todo

---
# `Load data`
load_raw_eeg()
    mne_preprocessor()
    - show_full_waveform()
    from_mne_epochs()

load_epochs
    - load_dataframe_pickle()
    - load_mne_fif()
    - load_eeglab_mat()
    - load_filetrip_mat()
---

# `Extract the data`
epochs = Epochs(all,average,info)

epochs.save(self, filepath, append=False)

**extracted = epochs.extract(collection_script, average=False)**

extracted.get_batch_names(self, batch_id='all')
extracted.get_dataframe(self, batch_id=0, case_id=0, to_print=False)
extracted.get_array(self, batch_id=0, case_id=0, to_print=False)
extracted.get_index(self, batch_id=0, case_id=0, to_print=False)
extracted.get_info(self, key)
---

# `Analysis`
result = t.ERP(plot=True)
result = t.TANOVA(plot=True)
result = t.clustering(plot=True)
result = t.topography(plot=True)

- stats
    - permutation
    - classification
---

# `Plot`
 - figure_group (collection)
    - 方阵
    axis: shared (title,x,y,colorbar), hidden
    attrs: - shared_axis=True -> topo
           - shared_axis=False -> block
 - figure_unit
    - general
    - advanced
        - line
        - topo
        - heatmap
            - gird
            - smooth

