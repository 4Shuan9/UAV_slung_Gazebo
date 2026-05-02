import matplotlib.pyplot as plt
import numpy as np
import os

# Setup
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
plt.rcParams['mathtext.fontset'] = 'stix'
os.makedirs('output', exist_ok=True)

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.axis('off')

# Parameters
L = 5
theta_x = np.radians(25)
theta_y = np.radians(35)
# 在 FRD 右手系中重新解算坐标 (X: 前, Y: 右, Z: 下)
Z_val = L / np.sqrt(1 + np.tan(theta_x)**2 + np.tan(theta_y)**2)
X = Z_val * np.tan(theta_x)
Y = -Z_val * np.tan(theta_y)  
Z = -Z_val 

# Quadrotor (X型布局)
arm = 2
r_d = arm * np.cos(np.pi/4) # 旋转45度后的投影长度
ax.plot([-r_d, r_d], [-r_d, r_d], [0, 0], 'k-', lw=3)
ax.plot([-r_d, r_d], [r_d, -r_d], [0, 0], 'k-', lw=3)

# Rotors
theta = np.linspace(0, 2*np.pi, 50)
for cx, cy in [(r_d, r_d), (r_d, -r_d), (-r_d, r_d), (-r_d, -r_d)]:
    ax.plot(cx + 0.6*np.cos(theta), cy + 0.6*np.sin(theta), np.zeros_like(theta), 'k-', lw=1.5)
    ax.plot([cx, cx], [cy, cy], [0, 0.025], 'k-', lw=3)

# Body Frame (FRD 右手系)
ax.quiver(0, 0, 0, 3.5, 0, 0, color='k', arrow_length_ratio=0.075, lw=1.5)
ax.quiver(0, 0, 0, 0, -4, 0, color='k', arrow_length_ratio=0.075, lw=1.5) 
ax.quiver(0, 0, 0, 0, 0, -6.5, color='k', arrow_length_ratio=0.05, lw=1.5)
ax.text(3.6, 0, 0, '$X_b$', fontsize=16, fontweight='bold', style='italic')
ax.text(0, -4.2, 0, '$Y_b$', fontsize=16, fontweight='bold', style='italic')
ax.text(0, 0, -7.0, '$Z_b$', fontsize=16, fontweight='bold', style='italic')
ax.text(-0.3, 0.3, 0.3, '$O_b$', fontsize=16, fontweight='bold', style='italic')

# Inertial Frame
offset_x, offset_y, offset_z = -3, 3, 2 
ax.quiver(offset_x, offset_y, offset_z, 2, 0, 0, color='k', arrow_length_ratio=0.1, lw=1.5)
ax.quiver(offset_x, offset_y, offset_z, 0, -2, 0, color='k', arrow_length_ratio=0.1, lw=1.5)
ax.quiver(offset_x, offset_y, offset_z, 0, 0, -2, color='k', arrow_length_ratio=0.1, lw=1.5)
ax.text(offset_x+2.2, offset_y, offset_z, '$X_I$', fontsize=16)
ax.text(offset_x, offset_y-2.4, offset_z, '$Y_I$', fontsize=16)
ax.text(offset_x, offset_y, offset_z-2.5, '$Z_I$', fontsize=16)
ax.text(offset_x-0.3, offset_y+0.3, offset_z+0.3, '$O_I$', fontsize=16)

# Cable & Payload
ax.plot([0, X], [0, Y], [0, Z], color="#727272", lw=3, label='Rigid Cable')
ax.scatter([X], [Y], [Z], color='k', s=200, depthshade=False, zorder=5)
ax.text(X+0.1, Y-0.3, Z, 'm', fontsize=16, style='italic')

# Projections & Lines
ax.plot([X, X], [Y, 0], [Z, Z], 'k--', alpha=0.5, lw=1.2)
ax.plot([X, 0], [Y, Y], [Z, Z], 'k--', alpha=0.5, lw=1.2)
ax.plot([X, 0], [0, 0], [Z, Z], 'k--', alpha=0.5, lw=1.2)
ax.plot([0, 0], [Y, 0], [Z, Z], 'k--', alpha=0.5, lw=1.2)
ax.plot([0, 0], [0, 0], [0, Z], 'k--', alpha=0.5, lw=1.2)
ax.plot([X, 0], [Y, 0], [Z, Z], 'k--', alpha=0.5, lw=1.2)
ax.plot([0, X], [0, 0], [0, Z], '--', color='#d62728', lw=1.75)
ax.plot([0, 0], [0, Y], [0, Z], '--', color='#1f77b4', lw=1.75)

# Angles
t = np.linspace(0, theta_x, 30)
arc_r = 2.1
ax.plot(arc_r*np.sin(t), np.zeros_like(t), -arc_r*np.cos(t), '#d62728', lw=1.5)
ax.text(arc_r*np.sin(theta_x/2) - 0.2, -0.15, -arc_r*np.cos(theta_x/2) -0.3, r'$\theta_x$', color='#d62728', fontsize=16)

t2 = np.linspace(0, theta_y, 30)
arc_r2 = 1.25
ax.plot(np.zeros_like(t2), -arc_r2*np.sin(t2), -arc_r2*np.cos(t2), '#1f77b4', lw=1.5)
ax.text(-0.2, -arc_r2*np.sin(theta_y/2) - 0.2, -arc_r2*np.cos(theta_y/2) - 0.2, r'$\theta_y$', color='#1f77b4', fontsize=16)

# View - 视角修改为 40 (原 -50 逆时针旋转 90 度)
ax.view_init(elev=20, azim=-118)

# Save Configuration
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
plt.savefig('output/Fig1.png', dpi=600, transparent=False, facecolor='white', bbox_inches='tight', pad_inches=0)
plt.savefig('output/Fig1.pdf', transparent=False, facecolor='white', bbox_inches='tight', pad_inches=0)
plt.show()