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

# 柱面沿 z 轴方向的范围（此处仅用于参考平面网格）
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
# 子图 1：绕 z 轴旋转（旋转抛物面）
# ============================================================

ax1 = fig.add_subplot(
    1, 3, 1,
    projection='3d'
)

# 曲面参数：x^2 + y^2 = 2 z，z ∈ [0, 3]
z_vals = np.linspace(0, 3, 40)
phi = np.linspace(0, 2 * np.pi, 60)
Z, Phi = np.meshgrid(z_vals, phi)
R = np.sqrt(2 * Z)          # 半径
X_rot = R * np.cos(Phi)
Y_rot = R * np.sin(Phi)

# 绘制旋转曲面
ax1.plot_surface(
    X_rot, Y_rot, Z,
    alpha=0.7,
    color='#1f77b4',
    edgecolor='none',
    antialiased=True
)

# 准线（平面曲线）：在 yOz 平面，y^2 = 2 z，即 z = y^2/2
t = np.linspace(-2.5, 2.5, 200)
x_line = np.zeros_like(t)
y_line = t
z_line = t**2 / 2
ax1.plot(x_line, y_line, z_line, color='black', linewidth=3)

setup_axis(ax1)

# 添加标题：绕 z 轴，方程用半径替换形式表示
ax1.set_title(
    r'$(\pm\sqrt{x^2+y^2})^2 - 2z = 0$',
    fontsize=14,
    y=1.02
)


# ============================================================
# 子图 2：绕 x 轴旋转（旋转抛物面）
# ============================================================

ax2 = fig.add_subplot(
    1, 3, 2,
    projection='3d'
)

# 曲面参数：y^2 + z^2 = 2 x，x ∈ [0, 3]
x_vals = np.linspace(0, 3, 40)
phi = np.linspace(0, 2 * np.pi, 60)
X_mesh, Phi = np.meshgrid(x_vals, phi)
R = np.sqrt(2 * X_mesh)
Y_rot = R * np.cos(Phi)
Z_rot = R * np.sin(Phi)

# 绘制旋转曲面
ax2.plot_surface(
    X_mesh, Y_rot, Z_rot,
    alpha=0.7,
    color='#d62728',
    edgecolor='none',
    antialiased=True
)

# 准线（平面曲线）：在 xOz 平面，z^2 = 2 x，即 x = z^2/2
t = np.linspace(-2.5, 2.5, 200)
x_line = t**2 / 2
y_line = np.zeros_like(t)
z_line = t
ax2.plot(x_line, y_line, z_line, color='black', linewidth=3)

setup_axis(ax2)

ax2.set_title(
    r'$(\pm\sqrt{y^2+z^2})^2 -2x = 0$',
    fontsize=14,
    y=1.02
)


# ============================================================
# 子图 3：绕 y 轴旋转（旋转抛物面）
# ============================================================

ax3 = fig.add_subplot(
    1, 3, 3,
    projection='3d'
)

# 曲面参数：x^2 + z^2 = 2 y，y ∈ [0, 3]
y_vals = np.linspace(0, 3, 40)
phi = np.linspace(0, 2 * np.pi, 60)
Y_mesh, Phi = np.meshgrid(y_vals, phi)
R = np.sqrt(2 * Y_mesh)
X_rot = R * np.cos(Phi)
Z_rot = R * np.sin(Phi)

# 绘制旋转曲面
ax3.plot_surface(
    X_rot, Y_mesh, Z_rot,
    alpha=0.7,
    color='#2ca02c',
    edgecolor='none',
    antialiased=True
)

# 准线（平面曲线）：在 yOz 平面，z^2 = 2 y，即 y = z^2/2
t = np.linspace(-2.5, 2.5, 200)
x_line = np.zeros_like(t)
y_line = t**2 / 2
z_line = t
ax3.plot(x_line, y_line, z_line, color='black', linewidth=3)

setup_axis(ax3)

ax3.set_title(
    r'$(\pm\sqrt{x^2+z^2})^2 - 2y = 0$',
    fontsize=14,
    y=1.02
)


# ============================================================
# 调整布局（为标题留出空间）
# ============================================================

plt.subplots_adjust(
    left=0.01,
    right=0.99,
    bottom=0.02,
    top=0.88,        # 增大顶部空间，使标题不被裁剪
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