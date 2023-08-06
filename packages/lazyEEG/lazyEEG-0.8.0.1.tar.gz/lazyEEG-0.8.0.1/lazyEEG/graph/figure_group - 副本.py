from ..default import *
from .. import structure
from . import figure_unit

import matplotlib.gridspec as gridspec

def select_subplot_type(subplot_type, ax, data, annotation, plot_params):
    if subplot_type == 'waveform':
        figure_unit.plot_waveform(ax, data, plot_params)
        if type(annotation) == pd.DataFrame:
            figure_unit.significant(ax, annotation, plot_params['win'], plot_params['sig_limit'])
    elif subplot_type == 'spectrum':
        figure_unit.plot_spectrum(ax, data, plot_params)
        if type(annotation) == pd.DataFrame:
            figure_unit.significant(ax, annotation, plot_params['win'], plot_params['sig_limit'])
    elif subplot_type == 'topograph':
        figure_unit.plot_topograph(ax, data, plot_params)
    elif subplot_type == 'heatmap':
        figure_unit.plot_heatmap(ax, data, None, plot_params)
    else:
        raise Exception(f'Unsupported subplot_type "{subplot_type}"')

def plot(self, plot_params=dict(), save=False):
    'setting'
    for k in self.default_plot_params:
        if k not in plot_params:
            plot_params[k] = self.default_plot_params[k]

    if 'color' in plot_params:
        color = sns.color_palette(plot_params['color'])
    if 'style' in plot_params:
        sns.set_style(plot_params['style']) # "ticks" "white" "dark" 'darkgrid'(default) 'whitegrid'

    if len(self.data) > 1:
        col,row = 2, math.ceil(len(self.data)/2)
    else:
        col,row = 1,1

    if 'x_len' in plot_params:
        fig_x = plot_params['x_len']
    else:
        fig_x = 8

    'preparing the canvas'
    fig_collection = plt.figure(figsize=(fig_x*col,5*row))
    outer = gridspec.GridSpec(row, col, wspace=0.2, hspace=0.2)
    
    for idx in range(len(self.data)):
        if plot_params['plot_type'][0] == 'direct':
            ax = plt.Subplot(fig_collection, outer[idx])
            select_subplot_type(plot_params['plot_type'][1], ax, self.data[idx], self.annotation[idx], plot_params)
            # cbar_axis = fig.add_axes([axpos.x0, axpos.y0-0.1, axpos.width, 0.05])
            fig_collection.add_subplot(ax)
        elif plot_params['plot_type'][0] == 'matrix':
            matrix_plot(fig_collection, outer[idx], 
                self.data[idx], self.annotation[idx], 
                plot_params['x_axis'],plot_params['y_axis'],plot_params)
        elif plot_params['plot_type'][0] == 'float':
            float_plot(fig_collection, outer[idx], 
                self.data[idx], self.annotation[idx], 
                plot_params['xy_locs'], plot_params)
        else:
            raise Exception(f'Unsupported plot_type {plot_params["plot_type"][0]}')  

    'reset'
    sns.despine()
    sns.set()
    
    'save'
    if save:
        title = f'{title}.png'
        if type(save) == str:
            title = save
        fig_collection.savefig(title, transparent=True)
    
    # fig_collection.show()
    return fig_collection

structure.Analyzed_data.plot = plot

def float_plot(fig, outer_grid, data, annotation, positions, plot_params):
    sns.set_style("white")

    data_cells = dict((k[2:],v) for k,v in data.groupby(level='channel_group'))

    if type(annotation) == pd.DataFrame:
        annotation_cells = dict((k[2:],v) for k,v in annotation.groupby(level='channel_group'))
    for idx,(data_name,data) in enumerate(data_cells.items()):
        data.name = data_name
        sys.stdout.write(' ' * 30 + '\r')
        sys.stdout.flush()
        sys.stdout.write('%d/%d\r' %(idx+1,len(data_cells)))
        sys.stdout.flush()

        ax = plt.Subplot(fig, outer_grid)
        if type(annotation) == pd.DataFrame:
            select_subplot_type(plot_params['plot_type'][1], ax, data, annotation_cells[data_name], plot_params)
        else:
            select_subplot_type(plot_params['plot_type'][1], ax, data, None, plot_params)
        ax.set_position([positions[data_name][0], positions[data_name][1] ,0.3,0.3])
        ax.axis('off')
        fig.add_subplot(ax)

        ax.legend(bbox_to_anchor=(1.01, 1))

    sns.set() # switch to seaborn defaults

def matrix_plot(fig, outer_grid, data, annotation, x_axis, y_axis, plot_params):
    sns.set_style("white")

    data = data.stack('time')

    for level_name in data.index.names:
        if '_group' in level_name:
            old_values_in_level = data.index.levels[data.index.names.index(level_name)]
            data.index = data.index.set_levels([' '.join(i.split(' ')[1:]) for i in old_values_in_level],level=level_name)
    'add "ms" to time axis'
    old_values_in_level = data.index.levels[data.index.names.index('time')]
    data.index = data.index.set_levels([f'{i}ms' for i in old_values_in_level],level='time')

    x_axis_values = list(OrderedDict.fromkeys(data.index.get_level_values(x_axis))) # remove duplicates from a list in whilst preserving order
    y_axis_values = list(OrderedDict.fromkeys(data.index.get_level_values(y_axis))) # remove duplicates from a list in whilst preserving order

    col_N,row_N = len(x_axis_values), len(y_axis_values)
    fig.set_figwidth(15)

    W,H = 1,1

    wspace = 0.1
    hspace = 0.1
    has_title = False
    has_colorbar = False

    height_ratios = [0,0.3,row_N,1]
    width_ratios = [0.7,col_N,0.7]
    fig.set_figwidth(sum(width_ratios)*1.7)
    fig.set_figheight(sum(height_ratios)*1.7)

    if has_title:
        height_ratios[0] = 0.5

    inner_grids = gridspec.GridSpecFromSubplotSpec(4, 3, outer_grid, wspace=wspace, hspace=hspace, height_ratios=height_ratios, width_ratios=width_ratios)
    
    'title'
    ax = plt.Subplot(fig, inner_grids[1])
    ax.text(0.5, 0.5, plot_params['title'], va="center", ha="center")
    ax.axis('off')
    fig.add_subplot(ax)

    'x_axis'
    inner_grids_for_x_axis = gridspec.GridSpecFromSubplotSpec(1, col_N, inner_grids[4], wspace=wspace, hspace=hspace)
    for i in range(col_N):
        ax = plt.Subplot(fig, inner_grids_for_x_axis[i])
        ax.text(0.5, 0.5, x_axis_values[i], va="center", ha="center")
        ax.axis('off')
        fig.add_subplot(ax)

    'y_axis'
    inner_grids_for_y_axis = gridspec.GridSpecFromSubplotSpec(row_N, 1, inner_grids[6], wspace=wspace, hspace=hspace)
    for i in range(row_N):
        ax = plt.Subplot(fig, inner_grids_for_y_axis[i])
        ax.text(0.5, 0.5, y_axis_values[i], va="center", ha="center")
        ax.axis('off')
        fig.add_subplot(ax)

    'data'
    inner_grids_for_data = gridspec.GridSpecFromSubplotSpec(row_N, col_N, inner_grids[7])
    data_cells = dict((k,v) for k,v in data.groupby(level=[y_axis,x_axis]))
    for idx,data_name in enumerate(itertools.product(y_axis_values,x_axis_values)):
        ax = plt.Subplot(fig, inner_grids_for_data[idx])
        select_subplot_type(plot_params['plot_type'][1], ax, data_cells[data_name], annotation, plot_params)
        fig.add_subplot(ax)

    sns.set() # switch to seaborn defaults


def block(data,note,err_style='ci_band',stat_result=None, window='1ms', sig_limit=0.05, sub_plot_type='line', color="Set1", style='darkgrid',grid=True,export=None,x_len=None):
    # [parameters example]
    # note: ['Time(ms)', 'Amplitude(uV)', []]
    # stat_result: [{'p': series1-a, 'other': series1-b},{'p': series2-a, 'other': series2-b}]
    # data: [('title1',dataframe1), ('title2',dataframe2), ...]
    #   dataframe row: names=['subject,'condition','channel']
    #   dataframe columns: names=[None,'time'], levels=[['data'],[tp1,tp2,...]]

    if len(data) == 1:
        column,row = 1,1
        fig_size = [8,5]
    else:
        column, row = 2, math.ceil(len(data)/2)
        fig_size = [15, 4.5*row]

    if x_len:
       fig_size[0] = x_len

    try:
        color = sns.color_palette(color)
    except:
        pass

    sns.set_style(style) # "ticks" "white" "dark" 'darkgrid'(default) 'whitegrid'

    fig = plt.figure(figsize=fig_size)
    for ind,(title,batch_data) in enumerate(data):
        ax = fig.add_subplot(row,column,ind+1)
        if sub_plot_type == 'line':
            draw.line(ax, title, batch_data,note,err_style=err_style,color=color)
            if stat_result and stat_result[ind]!=None:
                draw.significant(ax, stat_result[ind]['p'], window, sig_limit)
        if sub_plot_type == 'heatmap':
            draw.heatmap(ax, title, batch_data, note, "OrRd", grid=grid)
        
    if export: fig.savefig("%s_%d.%s" %(title,ind,export), transparent=True)

    sns.despine()
    sns.set()
    
    plt.show()


def pval_stack(stat_groups_data,note=['Time(ms)','','',['P > 0.1','','P < 0.1','','P < 0.05','','P < 0.01']],export=None,x_len=None):
    # [parameters example]
    # note: ['Time(ms)', '', []]
    row = len(stat_groups_data)

    for ind,(title,data) in enumerate(stat_groups_data):
        # data = pd.DataFrame({name:compr_data for name,compr_data in group}).T
        data = 1-data
        data[data>0.99] = 4
        data[(data<=0.99) & (data>0.95)] = 3
        data[(data<=0.95) & (data>0.9)] = 2
        data[data<=0.9] = 1
        
        for row in range(data.shape[0]):
            for col in range(data.shape[1]-1):
                if data.ix[row,col-1]==1 and data.ix[row,col+1]==1:
                    data.set_value(row,col,1.0,takeable=True)
        
        if not x_len:
            x_len = data.shape[1]/15 # 6

        fig = plt.figure(figsize=(x_len,data.shape[0]/5))
        ax = fig.add_subplot(111)
        cbar_ax = fig.add_axes([0.95,0.1,0.01,0.8])

        draw.heatmap(ax, title, data, note, "OrRd", cbar_ax)

        if export: fig.savefig("%s_%d.%s" %(title,ind,export), transparent=True)
    plt.show()

def class_stack(stat_groups_data,note,export=None,x_len=None):
    # [parameters example]
    # note: ['Time(ms)','','cluster',list(range(1,8))]
    row = len(stat_groups_data)

    for ind,(title,data) in enumerate(stat_groups_data):
        if not x_len:
            x_len = data.shape[1]/40
        fig = plt.figure(figsize=(x_len, data.shape[0]/4))
        ax = fig.add_subplot(111)
        cbar_ax = fig.add_axes([0.95,0.1,0.01,0.8])
        draw.heatmap(ax, title, data, note, sns.cubehelix_palette(light=0.95,as_cmap=True), cbar_ax)

        if export: fig.savefig("%s_%d.%s" %(title,ind,export), transparent=True)
    plt.show()

