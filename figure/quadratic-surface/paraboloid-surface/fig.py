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
# 创建画布（2个子图）
# ============================================================

fig = plt.figure(figsize=(10, 5))

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
# 公共坐标系设置
# ============================================================

def setup_axis(ax):
    ax.set_axis_off()
    ax.set_xlim(axis_limits[0], axis_limits[1])
    ax.set_ylim(axis_limits[2], axis_limits[3])
    ax.set_zlim(axis_limits[4], axis_limits[5])
    ax.set_box_aspect([1, 1, 0.7])
    ax.view_init(elev=view_elev, azim=view_azim)

    ax.plot_wireframe(
        X_plane, Y_plane, Z_plane,
        color='#b0b0b0', alpha=0.28, linewidth=0.55,
        rstride=1, cstride=1, zorder=1
    )

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

    label_kwargs = {'fontsize': 14, 'color': axis_color, 'ha': 'center', 'va': 'center', 'zorder': 2}
    ax.text(axis_length + 0.5, 0, 0, r'$x$', **label_kwargs)
    ax.text(0, axis_length + 0.5, 0, r'$y$', **label_kwargs)
    ax.text(0, 0, axis_length - 0.5, r'$z$', **label_kwargs)


# ============================================================
# 子图 1：椭圆抛物面 (开口朝上)
# ============================================================

ax1 = fig.add_subplot(1, 2, 1, projection='3d')

a_ep, b_ep = 1.2, 1.8
r_max_ep = 2.0   # 缩小，使最大 z = r_max^2/2 = 2.0
r = np.linspace(0, r_max_ep, 40)
v = np.linspace(0, 2 * np.pi, 60)
R, V = np.meshgrid(r, v)
X1 = a_ep * R * np.cos(V)
Y1 = b_ep * R * np.sin(V)
Z1 = R**2 / 2

setup_axis(ax1)
surf_color1 = '#1f77b4'
ax1.plot_surface(X1, Y1, Z1, alpha=0.6, color=surf_color1, edgecolor='none', antialiased=True, zorder=5)

# 截口线 (xz平面 y=0) : z = x^2/(2*a^2)
x_line_ep = np.linspace(-a_ep * r_max_ep, a_ep * r_max_ep, 200)
z_line_ep = x_line_ep**2 / (2 * a_ep**2)
ax1.plot(x_line_ep, np.zeros_like(x_line_ep), z_line_ep, color='#0a3b6e', linewidth=2.0, zorder=6)

ax1.set_title(r'$\frac{x^2}{a^2}+\frac{y^2}{b^2}=z$', fontsize=14, y=1.02)


# ============================================================
# 子图 2：双曲抛物面 (鞍面) —— 缩小尺寸
# ============================================================

ax2 = fig.add_subplot(1, 2, 2, projection='3d')

a_hp, b_hp = 1.2, 1.8
u_max = 2.0   # 减小，使范围缩小
u = np.linspace(-u_max, u_max, 40)
v = np.linspace(-u_max, u_max, 40)
U, V = np.meshgrid(u, v)
X2 = a_hp * U
Y2 = b_hp * V
Z2 = (U**2 - V**2) / 2

setup_axis(ax2)
surf_color2 = '#d62728'
ax2.plot_surface(X2, Y2, Z2, alpha=0.6, color=surf_color2, edgecolor='none', antialiased=True, zorder=5)

# 截口线1 (xz平面 y=0) : z = x^2/(2*a^2)
x_line_hp = np.linspace(-a_hp * u_max, a_hp * u_max, 200)
z_line_hp_x = x_line_hp**2 / (2 * a_hp**2)
ax2.plot(x_line_hp, np.zeros_like(x_line_hp), z_line_hp_x, color='#8a1a1a', linewidth=2.0, zorder=6)

# 截口线2 (yz平面 x=0) : z = - y^2/(2*b^2)
y_line_hp = np.linspace(-b_hp * u_max, b_hp * u_max, 200)
z_line_hp_y = - y_line_hp**2 / (2 * b_hp**2)
ax2.plot(np.zeros_like(y_line_hp), y_line_hp, z_line_hp_y, color='#8a1a1a', linewidth=2.0, zorder=6, linestyle='--')

ax2.set_title(r'$\frac{x^2}{a^2}-\frac{y^2}{b^2}=z$', fontsize=14, y=1.02)


# ============================================================
# 调整布局
# ============================================================

plt.subplots_adjust(left=0.02, right=0.98, bottom=0.02, top=0.88, wspace=0.1)

# ============================================================
# 输出 PDF
# ============================================================

output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fig.pdf')
fig.savefig(output_path, format='pdf', bbox_inches='tight', pad_inches=0.05)