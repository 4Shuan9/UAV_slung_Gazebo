import matplotlib.pyplot as plt
import numpy as np
import os

# Set font to Times New Roman globally, and use STIX for math text (looks like Times)
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
plt.rcParams['mathtext.fontset'] = 'stix'

# Create output directory
os.makedirs('output', exist_ok=True)

fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

# Remove axes for clean diagram look
ax.axis('off')

# Base parameters
L = 5
theta_x = np.radians(25)
theta_y = np.radians(35)

# Calculate coordinates based on projection definition
Z = L / np.sqrt(1 + np.tan(theta_x)**2 + np.tan(theta_y)**2)
X = Z * np.tan(theta_x)
Y = Z * np.tan(theta_y)
Z = -Z # pointing downwards

# Draw Quadrotor body
arm = 2
ax.plot([-arm, arm], [0, 0], [0, 0], 'k-', lw=3)
ax.plot([0, 0], [-arm, arm], [0, 0], 'k-', lw=3)

# Draw Rotors
theta = np.linspace(0, 2*np.pi, 50)
for cx, cy in [(arm, 0), (-arm, 0), (0, arm), (0, -arm)]:
    ax.plot(cx + 0.6*np.cos(theta), cy + 0.6*np.sin(theta), np.zeros_like(theta), 'k-', lw=1.5)
    ax.plot([cx, cx], [cy, cy], [0, 0.2], 'k-', lw=2)

# Coordinate system (Body frame Ob-XbYbZb)
ax.quiver(0, 0, 0, 4, 0, 0, color='k', arrow_length_ratio=0.075, lw=1.5)
ax.quiver(0, 0, 0, 0, 4, 0, color='k', arrow_length_ratio=0.075, lw=1.5)
ax.quiver(0, 0, 0, 0, 0, -6.5, color='k', arrow_length_ratio=0.05, lw=1.5)
ax.text(4.4, 0, 0, '$X_b$', fontsize=16, fontweight='bold', style='italic')
ax.text(0, 4.4, 0, '$Y_b$', fontsize=16, fontweight='bold', style='italic')
ax.text(0, 0, -7.0, '$Z_b$', fontsize=16, fontweight='bold', style='italic')
ax.text(-0.5, 0, 0.5, '$O_b$', fontsize=16, fontweight='bold', style='italic')

# Draw Inertial Frame (OI-XIYIZI) in the background
offset_x, offset_y, offset_z = -3, -3, 2
ax.quiver(offset_x, offset_y, offset_z, 2, 0, 0, color='k', arrow_length_ratio=0.1, lw=1)
ax.quiver(offset_x, offset_y, offset_z, 0, 2, 0, color='k', arrow_length_ratio=0.1, lw=1)
ax.quiver(offset_x, offset_y, offset_z, 0, 0, -2, color='k', arrow_length_ratio=0.1, lw=1)
ax.text(offset_x+2.2, offset_y, offset_z, '$X_I$', fontsize=16)
ax.text(offset_x, offset_y+2.2, offset_z, '$Y_I$', fontsize=16)
ax.text(offset_x, offset_y, offset_z-2.5, '$Z_I$', fontsize=16)
ax.text(offset_x-0.5, offset_y, offset_z+0.3, '$O_I$', fontsize=16)

# Draw Cable
ax.plot([0, X], [0, Y], [0, Z], color="#727272", lw=3, label='Rigid Cable')

# Draw Payload
ax.scatter([X], [Y], [Z], color='k', s=200, depthshade=False, zorder=5)
ax.text(X+0.3, Y+0.3, Z, 'm', fontsize=16, style='italic')

# Draw projections and planes
# 1. 载荷到 X-Z 平面的投影连线
ax.plot([X, X], [Y, 0], [Z, Z], 'k--', alpha=0.5, lw=1.2)
# 2. 载荷到 Y-Z 平面的投影连线
ax.plot([X, 0], [Y, Y], [Z, Z], 'k--', alpha=0.5, lw=1.2)
# 3. X-Z 平面投影点 到 Z 轴的连线
ax.plot([X, 0], [0, 0], [Z, Z], 'k--', alpha=0.5, lw=1.2)
# 4. Y-Z 平面投影点 到 Z 轴的连线
ax.plot([0, 0], [Y, 0], [Z, Z], 'k--', alpha=0.5, lw=1.2)
# 5. 补全中心 Z 轴的辅助线，延伸到载荷的 Z 轴高度
ax.plot([0, 0], [0, 0], [0, Z], 'k--', alpha=0.5, lw=1.2)
# 6. 新增：载荷 m 直接到 Z 轴的连线（底面对角线）
ax.plot([X, 0], [Y, 0], [Z, Z], 'k--', alpha=0.5, lw=1.2)

# Projection to X-Z plane (theta_x)
ax.plot([0, X], [0, 0], [0, Z], '--', color='#d62728', lw=1.75)
# Projection to Y-Z plane (theta_y)
ax.plot([0, 0], [0, Y], [0, Z], '--', color='#1f77b4', lw=1.75)

# Draw angles
t = np.linspace(0, theta_x, 30)
arc_r = 1.25
ax.plot(arc_r*np.sin(t), np.zeros_like(t), -arc_r*np.cos(t), '#d62728', lw=1.5)
ax.text(arc_r*np.sin(theta_x/2) + 0.0, -0.2, -arc_r*np.cos(theta_x/2) -0.4, r'$\theta_x$', color='#d62728', fontsize=16)

t2 = np.linspace(0, theta_y, 30)
arc_r2 = 2.5
ax.plot(np.zeros_like(t2), arc_r2*np.sin(t2), -arc_r2*np.cos(t2), '#1f77b4', lw=1.5)
ax.text(0, arc_r2*np.sin(theta_y/2) + 0.0, -arc_r2*np.cos(theta_y/2) - 0.4, r'$\theta_y$', color='#1f77b4', fontsize=16)

# Set view angle
ax.view_init(elev=20, azim=-50)

# Save
plt.tight_layout()
plt.savefig('output/Fig1.png', dpi=600, transparent=False, facecolor='white')
plt.savefig('output/Fig1.pdf', transparent=False, facecolor='white')
plt.show()