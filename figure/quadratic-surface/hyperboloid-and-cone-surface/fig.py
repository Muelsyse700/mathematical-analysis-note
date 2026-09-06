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
# 创建画布（3个子图）
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
# 子图 1：单叶双曲面 (绕 z 轴)
# ============================================================

ax1 = fig.add_subplot(1, 3, 1, projection='3d')

a1, b1, c1 = 1.5, 1.8, 1.2
u_max1 = 1.5

u = np.linspace(-u_max1, u_max1, 40)
v = np.linspace(0, 2 * np.pi, 60)
U, V = np.meshgrid(u, v)
X1 = a1 * np.cosh(U) * np.cos(V)
Y1 = b1 * np.cosh(U) * np.sin(V)
Z1 = c1 * np.sinh(U)

setup_axis(ax1)
surf_color1 = '#1f77b4'
ax1.plot_surface(X1, Y1, Z1, alpha=0.6, color=surf_color1, edgecolor='none', antialiased=True, zorder=5)

# 截口线 (y=0) : x^2/a^2 - z^2/c^2 = 1
t = np.linspace(-u_max1, u_max1, 200)
x_pos = a1 * np.cosh(t)
z_pos = c1 * np.sinh(t)
x_neg = -a1 * np.cosh(t)
ax1.plot(x_pos, np.zeros_like(t), z_pos, color='#0a3b6e', linewidth=2.0, zorder=6)
ax1.plot(x_neg, np.zeros_like(t), z_pos, color='#0a3b6e', linewidth=2.0, zorder=6)

ax1.set_title(r'$\frac{x^2}{a^2}+\frac{y^2}{b^2}-\frac{z^2}{c^2}=1$', fontsize=14, y=1.02)


# ============================================================
# 子图 2：双叶双曲面 (绕 z 轴，正确的参数化)
# ============================================================

ax2 = fig.add_subplot(1, 3, 2, projection='3d')

a2, b2, c2 = 1.5, 1.8, 1.2
u_max2 = 1.7   # 使叶片清晰且不超过坐标轴

# 上叶 (z>0)
u_pos = np.linspace(0.01, u_max2, 30)
v = np.linspace(0, 2 * np.pi, 40)
U_pos, V = np.meshgrid(u_pos, v)
X2_pos = a2 * np.sinh(U_pos) * np.cos(V)
Y2_pos = b2 * np.sinh(U_pos) * np.sin(V)
Z2_pos = c2 * np.cosh(U_pos)

# 下叶 (z<0)
Z2_neg = -c2 * np.cosh(U_pos)
X2_neg = a2 * np.sinh(U_pos) * np.cos(V)
Y2_neg = b2 * np.sinh(U_pos) * np.sin(V)

setup_axis(ax2)
surf_color2 = '#d62728'
ax2.plot_surface(X2_pos, Y2_pos, Z2_pos, alpha=0.6, color=surf_color2, edgecolor='none', antialiased=True, zorder=5)
ax2.plot_surface(X2_neg, Y2_neg, Z2_neg, alpha=0.6, color=surf_color2, edgecolor='none', antialiased=True, zorder=5)

# 截口线 (y=0) : z^2/c^2 - x^2/a^2 = 1  => z = ± c * sqrt(1 + x^2/a^2)
# 参数化：x = a * sinh(t), z = c * cosh(t)  (上叶)
t_line = np.linspace(-u_max2, u_max2, 200)
x_line = a2 * np.sinh(t_line)
z_line_pos = c2 * np.cosh(t_line)
z_line_neg = -c2 * np.cosh(t_line)
ax2.plot(x_line, np.zeros_like(t_line), z_line_pos, color='#8a1a1a', linewidth=2.0, zorder=6)
ax2.plot(x_line, np.zeros_like(t_line), z_line_neg, color='#8a1a1a', linewidth=2.0, zorder=6)

ax2.set_title(r'$-\frac{x^2}{a^2}-\frac{y^2}{b^2}+\frac{z^2}{c^2}=1$', fontsize=14, y=1.02)


# ============================================================
# 子图 3：圆锥面 (绕 z 轴)
# ============================================================

ax3 = fig.add_subplot(1, 3, 3, projection='3d')

a3, b3, c3 = 1.5, 1.8, 1.2
r_max = 2.6   # 使 z 最大约 c/a * r_max ≈ 1.2/1.5*2.6 ≈ 2.08

r = np.linspace(0, r_max, 40)
v = np.linspace(0, 2 * np.pi, 60)
R, V = np.meshgrid(r, v)
X3 = a3 * R * np.cos(V)
Y3 = b3 * R * np.sin(V)
Z3_pos = c3 * R
Z3_neg = -c3 * R

setup_axis(ax3)
surf_color3 = '#2ca02c'
ax3.plot_surface(X3, Y3, Z3_pos, alpha=0.6, color=surf_color3, edgecolor='none', antialiased=True, zorder=5)
ax3.plot_surface(X3, Y3, Z3_neg, alpha=0.6, color=surf_color3, edgecolor='none', antialiased=True, zorder=5)

x_line_cone = np.linspace(-r_max*a3, r_max*a3, 200)
z_line_cone_pos = (c3 / a3) * x_line_cone
z_line_cone_neg = -(c3 / a3) * x_line_cone
ax3.plot(x_line_cone, np.zeros_like(x_line_cone), z_line_cone_pos, color='#1a6e1a', linewidth=2.0, zorder=6)
ax3.plot(x_line_cone, np.zeros_like(x_line_cone), z_line_cone_neg, color='#1a6e1a', linewidth=2.0, zorder=6)

ax3.set_title(r'$\frac{x^2}{a^2}+\frac{y^2}{b^2}-\frac{z^2}{c^2}=0$', fontsize=14, y=1.02)


# ============================================================
# 调整布局
# ============================================================

plt.subplots_adjust(left=0.01, right=0.99, bottom=0.02, top=0.88, wspace=-0.05)

# ============================================================
# 输出 PDF
# ============================================================

output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fig.pdf')
fig.savefig(output_path, format='pdf', bbox_inches='tight', pad_inches=0.05)