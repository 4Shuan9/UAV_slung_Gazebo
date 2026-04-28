import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import os

mpl.rcParams['font.family'] = 'serif'
mpl.rcParams['font.serif'] = ['Times New Roman']
mpl.rcParams['mathtext.fontset'] = 'stix'
mpl.rcParams['axes.facecolor'] = 'white'
mpl.rcParams['figure.facecolor'] = 'white'
mpl.rcParams['font.size'] = 10
mpl.rcParams['axes.labelsize'] = 11
mpl.rcParams['axes.titlesize'] = 11
mpl.rcParams['legend.fontsize'] = 10
mpl.rcParams['xtick.labelsize'] = 9
mpl.rcParams['ytick.labelsize'] = 9
mpl.rcParams['axes.linewidth'] = 0.8

CSV_FILE_PATH = 'data_analysis/csv/20260427_antiswing_Data.csv'
OUTPUT_DIR = 'output'
OUTPUT_FILENAME = '20260427_antiswing_error'
TIME_RANGE = (0.0, 60.0)
Y_LIM_ERR = (-0.2, 0.4)

def process_error_plot(file_path):
    if not os.path.exists(file_path):
        return

    df = pd.read_csv(file_path)
    col_time = '__time'
    col_truth_x = '/uav/truth/swing_angle/world_frame/cartesian/vector/x'
    col_truth_y = '/uav/truth/swing_angle/world_frame/cartesian/vector/y'
    col_cv_x = '/uav/cv/swing_angle/world_frame/cartesian/vector/x'
    col_cv_y = '/uav/cv/swing_angle/world_frame/cartesian/vector/y'
    col_cv_comp_x = '/uav/cv_comp/swing_angle/world_frame/cartesian/vector/x'
    col_cv_comp_y = '/uav/cv_comp/swing_angle/world_frame/cartesian/vector/y'

    truth_data = df[[col_time, col_truth_x, col_truth_y]].dropna().copy()
    cv_data = df[[col_time, col_cv_x, col_cv_y]].dropna().copy()
    cv_comp_data = df[[col_time, col_cv_comp_x, col_cv_comp_y]].dropna().copy()

    t0 = min(truth_data[col_time].min(), cv_data[col_time].min(), cv_comp_data[col_time].min())
    truth_data['t'] = truth_data[col_time] - t0
    cv_data['t'] = cv_data[col_time] - t0
    cv_comp_data['t'] = cv_comp_data[col_time] - t0

    truth_data = truth_data[(truth_data['t'] >= TIME_RANGE[0]) & (truth_data['t'] <= TIME_RANGE[1])]
    cv_data = cv_data[(cv_data['t'] >= TIME_RANGE[0]) & (cv_data['t'] <= TIME_RANGE[1])]
    cv_comp_data = cv_comp_data[(cv_comp_data['t'] >= TIME_RANGE[0]) & (cv_comp_data['t'] <= TIME_RANGE[1])]

    error_cv_x = cv_data[col_cv_x].values - np.interp(cv_data['t'], truth_data['t'], truth_data[col_truth_x])
    error_cv_y = cv_data[col_cv_y].values - np.interp(cv_data['t'], truth_data['t'], truth_data[col_truth_y])
    error_cv_comp_x = cv_comp_data[col_cv_comp_x].values - np.interp(cv_comp_data['t'], truth_data['t'], truth_data[col_truth_x])
    error_cv_comp_y = cv_comp_data[col_cv_comp_y].values - np.interp(cv_comp_data['t'], truth_data['t'], truth_data[col_truth_y])

    fig, axs = plt.subplots(2, 1, figsize=(7.16, 7.16))
    fig.subplots_adjust(hspace=0.3, left=0.12, right=0.95, top=0.95, bottom=0.08)

    def plot_sub_err(ax, cv_t, err_cv, comp_t, err_comp, axis_name, title):
        ax.plot(cv_t, err_cv, color='#1f77b4', linestyle='--', linewidth=1.2, label='Raw Error')
        ax.plot(comp_t, err_comp, color='#d62728', linestyle='-.', linewidth=1.5, label='Comp Error')
        
        max_err = max(np.max(err_cv), np.max(err_comp))
        min_err = min(np.min(err_cv), np.min(err_comp))
        
        ax.axhline(max_err, color='black', linestyle='--', linewidth=0.8, alpha=0.6)
        ax.axhline(min_err, color='black', linestyle='--', linewidth=0.8, alpha=0.6)
        ax.text(TIME_RANGE[0] + 0.05, max_err, f'{max_err:.2f}', color='black', va='bottom', ha='left')
        ax.text(TIME_RANGE[0] + 0.05, min_err, f'{min_err:.2f}', color='black', va='top', ha='left')

        ax.set_ylabel(f'Error ${axis_name}$ (deg)')
        ax.set_xlabel('Time (s)')
        ax.set_title(title, pad=10)
        ax.set_ylim(Y_LIM_ERR)
        ax.set_xlim(TIME_RANGE)
        ax.grid(True, linestyle='--', color='#e0e0e0', alpha=0.7)
        ax.legend(loc='upper right', frameon=True, facecolor='white', edgecolor='black', fancybox=False, framealpha=1.0)

    plot_sub_err(axs[0], cv_data['t'], error_cv_x, cv_comp_data['t'], error_cv_comp_x, 'X', title='(a) Estimation Error (X-Axis)')
    plot_sub_err(axs[1], cv_data['t'], error_cv_y, cv_comp_data['t'], error_cv_comp_y, 'Y', title='(b) Estimation Error (Y-Axis)')

    fig.align_ylabels(axs)
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    plt.savefig(os.path.join(OUTPUT_DIR, f'{OUTPUT_FILENAME}.pdf'), format='pdf', dpi=600, bbox_inches='tight')
    plt.savefig(os.path.join(OUTPUT_DIR, f'{OUTPUT_FILENAME}.png'), format='png', dpi=600, bbox_inches='tight')
    plt.show()

if __name__ == "__main__":
    process_error_plot(CSV_FILE_PATH)