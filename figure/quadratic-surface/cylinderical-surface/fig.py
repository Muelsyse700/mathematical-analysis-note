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

# 柱面沿 z 轴方向的范围
z_range = np.linspace(-3, 3, 40)

# xy 参考平面网格
X_plane = np.linspace(-4, 4, 17)
Y_plane = np.linspace(-4, 4, 17)
X_plane, Y_plane = np.meshgrid(X_plane, Y_plane)
Z_plane = np.zeros_like(X_plane)

# 统一视角
view_elev = 25
view_azim = -60

# 坐标范围
axis_limits = [-4, 4, -4, 4, -3, 3]

# 自定义坐标轴长度
axis_length = 4.5

# ============================================================
# 公共坐标系设置函数
# ============================================================

def setup_axis(ax):

    # --------------------------------------------------------
    # 完全关闭 Matplotlib 3D 自带的坐标轴背景
    # --------------------------------------------------------

    ax.set_axis_off()

    # 重新打开坐标轴对象的绘制能力后，
    # 手动绘制需要的内容
    ax.set_xlim(axis_limits[0], axis_limits[1])
    ax.set_ylim(axis_limits[2], axis_limits[3])
    ax.set_zlim(axis_limits[4], axis_limits[5])

    # 保持统一比例
    ax.set_box_aspect([1, 1, 0.7])

    # 设置视角
    ax.view_init(
        elev=view_elev,
        azim=view_azim
    )

    # --------------------------------------------------------
    # xy 参考平面
    # --------------------------------------------------------
    #
    # 使用非常浅的灰色，只保留网格，不绘制平面填充
    #

    ax.plot_wireframe(
        X_plane,
        Y_plane,
        Z_plane,
        color='#b0b0b0',
        alpha=0.28,
        linewidth=0.55,
        rstride=1,
        cstride=1
    )

    # --------------------------------------------------------
    # 自定义坐标轴
    # --------------------------------------------------------

    axis_color = '#222222'
    axis_width = 1.3

    # x 轴
    ax.plot(
        [0, axis_length],
        [0, 0],
        [0, 0],
        color=axis_color,
        linewidth=axis_width,
        solid_capstyle='round'
    )

    ax.quiver(
        0, 0, 0,
        axis_length, 0, 0,
        color=axis_color,
        linewidth=axis_width,
        arrow_length_ratio=0.055,
        pivot='tail'
    )

    # y 轴
    ax.plot(
        [0, 0],
        [0, axis_length],
        [0, 0],
        color=axis_color,
        linewidth=axis_width,
        solid_capstyle='round'
    )

    ax.quiver(
        0, 0, 0,
        0, axis_length, 0,
        color=axis_color,
        linewidth=axis_width,
        arrow_length_ratio=0.055,
        pivot='tail'
    )

    # z 轴
    ax.plot(
        [0, 0],
        [0, 0],
        [0, axis_length - 1],
        color=axis_color,
        linewidth=axis_width,
        solid_capstyle='round'
    )

    ax.quiver(
        0, 0, 0,
        0, 0, axis_length - 1,
        color=axis_color,
        linewidth=axis_width,
        arrow_length_ratio=0.075,
        pivot='tail'
    )

    # --------------------------------------------------------
    # 坐标轴标签
    # --------------------------------------------------------

    label_kwargs = {
        'fontsize': 14,
        'color': axis_color,
        'ha': 'center',
        'va': 'center'
    }

    ax.text(
        axis_length + 0.5,
        0,
        0,
        r'$x$',
        **label_kwargs
    )

    ax.text(
        0,
        axis_length + 0.5,
        0,
        r'$y$',
        **label_kwargs
    )

    ax.text(
        0,
        0,
        axis_length - 0.5,
        r'$z$',
        **label_kwargs
    )


# ============================================================
# 子图 1：椭圆柱面
# ============================================================

ax1 = fig.add_subplot(
    1, 3, 1,
    projection='3d'
)

a, b = 2.0, 1.2

theta = np.linspace(
    0,
    2 * np.pi,
    80
)

theta_grid, z_grid = np.meshgrid(
    theta,
    z_range
)

x_ell = a * np.cos(theta_grid)
y_ell = b * np.sin(theta_grid)
z_ell = z_grid

# 曲面
ax1.plot_surface(
    x_ell,
    y_ell,
    z_ell,
    alpha=0.7,
    color='#1f77b4',
    edgecolor='none',
    antialiased=True
)

# 准线
ax1.plot(
    a * np.cos(theta),
    b * np.sin(theta),
    0,
    color='black',
    linewidth=3
)

setup_axis(ax1)


# ============================================================
# 子图 2：双曲柱面
# ============================================================

ax2 = fig.add_subplot(
    1, 3, 2,
    projection='3d'
)

a_h, b_h = 1.0, 1.0

u = np.linspace(
    -2,
    2,
    50
)

u_grid, z_grid = np.meshgrid(
    u,
    z_range
)

# 第一支
x_h1 = a_h * np.cosh(u_grid)
y_h1 = b_h * np.sinh(u_grid)
z_h1 = z_grid

# 第二支
x_h2 = -a_h * np.cosh(u_grid)
y_h2 = b_h * np.sinh(u_grid)
z_h2 = z_grid

# 曲面
ax2.plot_surface(
    x_h1,
    y_h1,
    z_h1,
    alpha=0.7,
    color='#d62728',
    edgecolor='none',
    antialiased=True
)

ax2.plot_surface(
    x_h2,
    y_h2,
    z_h2,
    alpha=0.7,
    color='#d62728',
    edgecolor='none',
    antialiased=True
)

# 准线
u_curve = np.linspace(
    -2,
    2,
    200
)

x_curve = a_h * np.cosh(u_curve)
y_curve = b_h * np.sinh(u_curve)

ax2.plot(
    x_curve,
    y_curve,
    0,
    color='black',
    linewidth=3
)

ax2.plot(
    -x_curve,
    y_curve,
    0,
    color='black',
    linewidth=3
)

setup_axis(ax2)


# ============================================================
# 子图 3：抛物柱面
# ============================================================

ax3 = fig.add_subplot(
    1, 3, 3,
    projection='3d'
)

p = 1.0

t = np.linspace(
    -2.8,
    2.8,
    50
)

t_grid, z_grid = np.meshgrid(
    t,
    z_range
)

# y^2 = 2px
# x = y^2 / (2p)

x_par = (t_grid ** 2) / (2 * p)
y_par = t_grid
z_par = z_grid

# 曲面
ax3.plot_surface(
    x_par,
    y_par,
    z_par,
    alpha=0.7,
    color='#2ca02c',
    edgecolor='none',
    antialiased=True
)

# 准线
t_curve = np.linspace(
    -2.8,
    2.8,
    200
)

x_curve_par = (t_curve ** 2) / (2 * p)
y_curve_par = t_curve

ax3.plot(
    x_curve_par,
    y_curve_par,
    0,
    color='black',
    linewidth=3
)

setup_axis(ax3)


# ============================================================
# 调整布局
# ============================================================

plt.subplots_adjust(
    left=0.01,
    right=0.99,
    bottom=0.02,
    top=0.98,
    wspace=-0.1
)

# ============================================================
# 输出 PDF
# ============================================================

output_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'fig.pdf'
)

fig.savefig(
    output_path,
    format='pdf',
    bbox_inches='tight',
    pad_inches=0.05
)