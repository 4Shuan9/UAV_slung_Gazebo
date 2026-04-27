import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

# ==========================================
# 配置区：在此修改文件名和路径
# ==========================================
CSV_FILE_PATH = 'data_analysis/csv/20260427_transform_Data.csv'
START_TIME_OFFSET = 0

# ==========================================
# 数据处理逻辑
# ==========================================
def process_drone_data(file_path):
    if not os.path.exists(file_path):
        print(f"Error: 文件 {file_path} 不存在。")
        return

    print(f"正在读取文件: {file_path} ...")
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

    interp_truth_for_cv_x = np.interp(cv_data['t'], truth_data['t'], truth_data[col_truth_x])
    interp_truth_for_cv_y = np.interp(cv_data['t'], truth_data['t'], truth_data[col_truth_y])
    interp_truth_for_cv_comp_x = np.interp(cv_comp_data['t'], truth_data['t'], truth_data[col_truth_x])
    interp_truth_for_cv_comp_y = np.interp(cv_comp_data['t'], truth_data['t'], truth_data[col_truth_y])

    error_cv_x = cv_data[col_cv_x].values - interp_truth_for_cv_x
    error_cv_y = cv_data[col_cv_y].values - interp_truth_for_cv_y
    error_cv_comp_x = cv_comp_data[col_cv_comp_x].values - interp_truth_for_cv_comp_x
    error_cv_comp_y = cv_comp_data[col_cv_comp_y].values - interp_truth_for_cv_comp_y

    error_cv_total = np.sqrt(error_cv_x**2 + error_cv_y**2)
    error_cv_comp_total = np.sqrt(error_cv_comp_x**2 + error_cv_comp_y**2)

    rmse_cv_x = np.sqrt(np.mean(error_cv_x**2))
    rmse_cv_y = np.sqrt(np.mean(error_cv_y**2))
    rmse_cv_total = np.sqrt(np.mean(error_cv_total**2))
    
    rmse_cv_comp_x = np.sqrt(np.mean(error_cv_comp_x**2))
    rmse_cv_comp_y = np.sqrt(np.mean(error_cv_comp_y**2))
    rmse_cv_comp_total = np.sqrt(np.mean(error_cv_comp_total**2))

    print(f"--- 稳态跟踪误差 ---")
    print(f"CV:      RMSE X = {rmse_cv_x:.4f}, RMSE Y = {rmse_cv_y:.4f}, RMSE Total = {rmse_cv_total:.4f}")
    print(f"CV_Comp: RMSE X = {rmse_cv_comp_x:.4f}, RMSE Y = {rmse_cv_comp_y:.4f}, RMSE Total = {rmse_cv_comp_total:.4f}")

    # ==========================================
    # 可视化绘图 (Plotly)
    # ==========================================
    title_str = (f"UAV Swing Angle Comparison<br>"
                 f"CV: RMSE_Tot={rmse_cv_total:.4f} | "
                 f"CV_Comp: RMSE_Tot={rmse_cv_comp_total:.4f}")

    fig = make_subplots(
        rows=3, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.06,
        subplot_titles=(
            "X-Axis Estimation vs Truth", 
            "Y-Axis Estimation vs Truth",
            "Total Estimation Error"
        )
    )

    fig.add_trace(go.Scatter(x=truth_data['t'], y=truth_data[col_truth_x], name="Truth X", line=dict(color='black', width=2)), row=1, col=1)
    fig.add_trace(go.Scatter(x=cv_data['t'], y=cv_data[col_cv_x], name="CV X", line=dict(color='blue', width=1, dash='dash')), row=1, col=1)
    fig.add_trace(go.Scatter(x=cv_comp_data['t'], y=cv_comp_data[col_cv_comp_x], name="CV Comp X", line=dict(color='red', width=1.5, dash='dashdot')), row=1, col=1)

    fig.add_trace(go.Scatter(x=truth_data['t'], y=truth_data[col_truth_y], name="Truth Y", line=dict(color='black', width=2)), row=2, col=1)
    fig.add_trace(go.Scatter(x=cv_data['t'], y=cv_data[col_cv_y], name="CV Y", line=dict(color='blue', width=1, dash='dash')), row=2, col=1)
    fig.add_trace(go.Scatter(x=cv_comp_data['t'], y=cv_comp_data[col_cv_comp_y], name="CV Comp Y", line=dict(color='red', width=1.5, dash='dashdot')), row=2, col=1)

    fig.add_trace(go.Scatter(x=cv_data['t'], y=error_cv_total, name="Total Error CV", line=dict(color='blue', width=1)), row=3, col=1)
    fig.add_trace(go.Scatter(x=cv_comp_data['t'], y=error_cv_comp_total, name="Total Error CV Comp", line=dict(color='red', width=1.5)), row=3, col=1)

    fig.update_layout(
        height=1000, 
        title_text=title_str,
        showlegend=True,
        template="plotly_white",
        hovermode="x unified"
    )

    fig.update_xaxes(title_text="Time (s)", row=3, col=1)
    fig.update_yaxes(title_text="Angle X", row=1, col=1)
    fig.update_yaxes(title_text="Angle Y", row=2, col=1)
    fig.update_yaxes(title_text="Total Error", row=3, col=1)

    fig.show()

if __name__ == "__main__":
    process_drone_data(CSV_FILE_PATH)