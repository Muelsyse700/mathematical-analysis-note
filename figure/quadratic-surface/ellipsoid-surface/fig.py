import os
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# 全局字体设置
# ============================================================

plt.rcParams.update({
    'font.family': 'STIXGeneral',
    'mathtext.fontset': 'stix',
    'pdf.fonttype': 42,
    'ps.fonttype': 42,
    'axes.unicode_minus': False,
})

# ============================================================
# 创建画布
# ============================================================

fig = plt.figure(figsize=(15, 5))

# ============================================================
# 公共参数
# ============================================================

z_range = np.linspace(-3, 3, 40)

X_plane = np.linspace(-4, 4, 17)
Y_plane = np.linspace(-4, 4, 17)
X_plane, Y_plane = np.meshgrid(X_plane, Y_plane)
Z_plane = np.zeros_like(X_plane)

view_elev = 25
view_azim = -60
axis_limits = [-4, 4, -4, 4, -3, 3]
axis_length = 4.5

# ============================================================
# 公共坐标系设置（坐标轴和网格在底层，zorder=1）
# ============================================================

def setup_axis(ax):
    ax.set_axis_off()
    ax.set_xlim(axis_limits[0], axis_limits[1])
    ax.set_ylim(axis_limits[2], axis_limits[3])
    ax.set_zlim(axis_limits[4], axis_limits[5])
    ax.set_box_aspect([1, 1, 0.7])
    ax.view_init(elev=view_elev, azim=view_azim)

    # 参考平面网格（最底层）
    ax.plot_wireframe(
        X_plane, Y_plane, Z_plane,
        color='#b0b0b0', alpha=0.28, linewidth=0.55,
        rstride=1, cstride=1, zorder=1
    )

    # 坐标轴线（底层）
    axis_color = '#222222'
    axis_width = 1.3
    ax.plot([0, axis_length], [0, 0], [0, 0], color=axis_color, linewidth=axis_width,
            solid_capstyle='round', zorder=1)
    ax.quiver(0, 0, 0, axis_length, 0, 0, color=axis_color, linewidth=axis_width,
              arrow_length_ratio=0.055, pivot='tail', zorder=1)

    ax.plot([0, 0], [0, axis_length], [0, 0], color=axis_color, linewidth=axis_width,
            solid_capstyle='round', zorder=1)
    ax.quiver(0, 0, 0, 0, axis_length, 0, color=axis_color, linewidth=axis_width,
              arrow_length_ratio=0.055, pivot='tail', zorder=1)

    ax.plot([0, 0], [0, 0], [0, axis_length - 1], color=axis_color, linewidth=axis_width,
            solid_capstyle='round', zorder=1)
    ax.quiver(0, 0, 0, 0, 0, axis_length - 1, color=axis_color, linewidth=axis_width,
              arrow_length_ratio=0.075, pivot='tail', zorder=1)

    # 坐标轴标签（稍高一层）
    label_kwargs = {'fontsize': 14, 'color': axis_color, 'ha': 'center', 'va': 'center', 'zorder': 2}
    ax.text(axis_length + 0.5, 0, 0, r'$x$', **label_kwargs)
    ax.text(0, axis_length + 0.5, 0, r'$y$', **label_kwargs)
    ax.text(0, 0, axis_length - 0.5, r'$z$', **label_kwargs)


# ============================================================
# 辅助函数：绘制截口线（只保留 z=0 和 x=0 平面）
# ============================================================

def draw_intersections(ax, a, b, c, color, alpha=0.6, linewidth=1.0):
    t = np.linspace(0, 2 * np.pi, 120)

    # z=0 平面
    x = a * np.cos(t)
    y = b * np.sin(t)
    z = np.zeros_like(t)
    ax.plot(x, y, z, color=color, alpha=alpha, linewidth=linewidth, zorder=6)

    # x=0 平面
    y = b * np.cos(t)
    z = c * np.sin(t)
    x = np.zeros_like(t)
    ax.plot(x, y, z, color=color, alpha=alpha, linewidth=linewidth, zorder=6)


# ============================================================
# 子图 1：一般椭球面
# ============================================================

ax1 = fig.add_subplot(1, 3, 1, projection='3d')

a, b, c = 2.0, 1.5, 1.0
theta = np.linspace(0, np.pi, 40)
phi = np.linspace(0, 2 * np.pi, 60)
Theta, Phi = np.meshgrid(theta, phi)
X = a * np.sin(Theta) * np.cos(Phi)
Y = b * np.sin(Theta) * np.sin(Phi)
Z = c * np.cos(Theta)

# 先画坐标轴和网格（底层）
setup_axis(ax1)

# 曲面（中层）
surf_color1 = '#1f77b4'
ax1.plot_surface(X, Y, Z, alpha=0.5, color=surf_color1, edgecolor='none', antialiased=True, zorder=5)

# 截口线（中层偏上）
draw_intersections(ax1, a, b, c, color='#105090', alpha=0.6, linewidth=1.0)

ax1.set_title(r'$\frac{x^2}{a^2}+\frac{y^2}{b^2}+\frac{z^2}{c^2}=1$', fontsize=14, y=1.02)


# ============================================================
# 子图 2：旋转椭球面
# ============================================================

ax2 = fig.add_subplot(1, 3, 2, projection='3d')

a_rot, c_rot = 2.0, 1.5
theta = np.linspace(0, np.pi, 40)
phi = np.linspace(0, 2 * np.pi, 60)
Theta, Phi = np.meshgrid(theta, phi)
X = a_rot * np.sin(Theta) * np.cos(Phi)
Y = a_rot * np.sin(Theta) * np.sin(Phi)
Z = c_rot * np.cos(Theta)

setup_axis(ax2)

surf_color2 = '#d62728'
ax2.plot_surface(X, Y, Z, alpha=0.5, color=surf_color2, edgecolor='none', antialiased=True, zorder=5)
draw_intersections(ax2, a_rot, a_rot, c_rot, color='#a01020', alpha=0.6, linewidth=1.0)

ax2.set_title(r'$\frac{x^2+y^2}{a^2}+\frac{z^2}{c^2}=1$', fontsize=14, y=1.02)


# ============================================================
# 子图 3：球面
# ============================================================

ax3 = fig.add_subplot(1, 3, 3, projection='3d')

R = 2.0
theta = np.linspace(0, np.pi, 40)
phi = np.linspace(0, 2 * np.pi, 60)
Theta, Phi = np.meshgrid(theta, phi)
X = R * np.sin(Theta) * np.cos(Phi)
Y = R * np.sin(Theta) * np.sin(Phi)
Z = R * np.cos(Theta)

setup_axis(ax3)

surf_color3 = '#2ca02c'
ax3.plot_surface(X, Y, Z, alpha=0.5, color=surf_color3, edgecolor='none', antialiased=True, zorder=5)
draw_intersections(ax3, R, R, R, color='#1a701a', alpha=0.6, linewidth=1.0)

ax3.set_title(r'$x^2+y^2+z^2=R^2$', fontsize=14, y=1.02)


# ============================================================
# 调整布局
# ============================================================

plt.subplots_adjust(left=0.01, right=0.99, bottom=0.02, top=0.88, wspace=-0.1)

# ============================================================
# 输出 PDF
# ============================================================

output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fig.pdf')
fig.savefig(output_path, format='pdf', bbox_inches='tight', pad_inches=0.05)