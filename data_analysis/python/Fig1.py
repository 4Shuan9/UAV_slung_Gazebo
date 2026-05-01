import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# 隐藏默认坐标轴
ax.set_axis_off()

# 定义无人机机体中心
O_b = np.array([0, 0, 0])

# 绘制机体系 O_b - X_b Y_b Z_b
ax.quiver(*O_b, 2, 0, 0, color='b', arrow_length_ratio=0.1)
ax.text(2.2, 0, 0, '$X_b$', fontsize=14)
ax.quiver(*O_b, 0, 2, 0, color='b', arrow_length_ratio=0.1)
ax.text(0, 2.2, 0, '$Y_b$', fontsize=14)
ax.quiver(*O_b, 0, 0, -3, color='b', arrow_length_ratio=0.05)
ax.text(0, 0, -3.2, '$Z_b$', fontsize=14)
ax.text(0.1, 0.1, 0.1, '$O_b$', fontsize=14)

# 绘制惯性系 O_I - X_I Y_I Z_I
O_I = np.array([-3, 2, 2])
ax.quiver(*O_I, 1.5, 0, 0, color='k', arrow_length_ratio=0.1)
ax.text(-1.3, 2, 2, '$X_I$', fontsize=12)
ax.quiver(*O_I, 0, 1.5, 0, color='k', arrow_length_ratio=0.1)
ax.text(-3, 3.7, 2, '$Y_I$', fontsize=12)
ax.quiver(*O_I, 0, 0, -1.5, color='k', arrow_length_ratio=0.1)
ax.text(-3, 2, 0.3, '$Z_I$', fontsize=12)
ax.text(-3.2, 2.2, 2.2, '$O_I$', fontsize=12)

# 绘制机臂与旋翼升力
arms = [[1.5,0,0], [0,1.5,0], [-1.5,0,0], [0,-1.5,0]]
for i, arm in enumerate(arms):
    ax.plot([0, arm[0]], [0, arm[1]], [0, arm[2]], 'k-', linewidth=3)
    # 升力箭头
    ax.quiver(arm[0], arm[1], arm[2], 0, 0, 1, color='r', arrow_length_ratio=0.2)
    ax.text(arm[0], arm[1], arm[2]+1.2, f'$F_{i+1}$', fontsize=12)

# 吊挂载荷位置
Load = np.array([1.2, 0.8, -2.5])
# 绘制刚性绳索 (由于假设为不伸长恒定绳长)
ax.plot([0, Load[0]], [0, Load[1]], [0, Load[2]], 'k-', linewidth=2)
ax.text(Load[0]/2 + 0.2, Load[1]/2, Load[2]/2, '$L$', fontsize=14)

# 绘制载荷质点 (忽略体积假设[cite: 1])
ax.scatter(*Load, color='k', s=200)

# 绘制投影线 (辅助虚线)
ax.plot([Load[0], Load[0]], [Load[1], 0], [Load[2], Load[2]], 'k--', alpha=0.5)
ax.plot([Load[0], 0], [Load[1], Load[1]], [Load[2], Load[2]], 'k--', alpha=0.5)
ax.plot([Load[0], 0], [Load[1], 0], [Load[2], Load[2]], 'k--', alpha=0.5)
ax.plot([Load[0], Load[0]], [0, 0], [Load[2], 0], 'k--', alpha=0.5)
ax.plot([0, 0], [Load[1], Load[1]], [Load[2], 0], 'k--', alpha=0.5)

# 标注摆角 theta_x (X-Z平面) 和 theta_y (Y-Z平面)[cite: 1]
ax.text(0.6, 0, -1.0, r'$\theta_x$', color='g', fontsize=14)
ax.text(0, 0.4, -1.0, r'$\theta_y$', color='orange', fontsize=14)

# 调整视角
ax.view_init(elev=25, azim=-55)

# 导出高质量矢量图
plt.savefig('fig1_slung_load_schematic.pdf', format='pdf', bbox_inches='tight')
plt.show()