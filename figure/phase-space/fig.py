import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from matplotlib.colors import Normalize, LinearSegmentedColormap
from matplotlib.font_manager import FontProperties

# ================== 字体设置 ==================
# 不使用外部 LaTeX 渲染，避免中文无法识别
plt.rcParams.update({
    'text.usetex': False,

    # 数学公式使用 Computer Modern 风格
    'mathtext.fontset': 'cm',

    # 全局默认字体
    'font.family': 'serif',
    'font.serif': ['Source Han Serif SC', 'Noto Serif CJK SC'],

    'axes.unicode_minus': False,
    'font.size': 16,
    'axes.labelsize': 16,
    'legend.fontsize': 16,
})

# ================== 中文字体 ==================
# 思源宋体
chinese_font = FontProperties(
    family='Source Han Serif SC',
    size=16
)

# ================== 参数设置 ==================
L = 1.0
m = 1.0
g = 9.81
c = 0.2

def pendulum_eq(t, state):
    theta, omega = state
    dtheta_dt = omega
    domega_dt = -(g/L) * np.sin(theta) - (c/(m*L**2)) * omega
    return [dtheta_dt, domega_dt]

# ================== 创建相空间网格 ==================
theta_min, theta_max = -1.2*np.pi, 4.8*np.pi
omega_min, omega_max = -12, 12

n_theta = 31
n_omega = 31

theta_vals = np.linspace(theta_min, theta_max, n_theta)
omega_vals = np.linspace(omega_min, omega_max, n_omega)
Theta, Omega = np.meshgrid(theta_vals, omega_vals)

# ================== 计算向量场 ==================
U = Omega
V = -(g/L) * np.sin(Theta) - (c/(m*L**2)) * Omega
magnitude = np.sqrt(U**2 + V**2)

# ================== 创建图像 ==================
fig, ax = plt.subplots(figsize=(14, 7))

# ============================================================
# 颜色映射
# ============================================================
base_cmap = plt.get_cmap('Purples')

cmap = LinearSegmentedColormap.from_list(
    'DarkPurples',
    base_cmap(np.linspace(0.25, 1.0, 256))
)

vmin = np.percentile(magnitude, 10)
vmax = magnitude.max()

norm = Normalize(
    vmin=vmin,
    vmax=vmax
)

# ============================================================
# 屏幕坐标归一化方向
# ============================================================
dx = theta_max - theta_min
dy = omega_max - omega_min

fig.canvas.draw()

bbox = ax.get_window_extent()

pixel_width = bbox.width
pixel_height = bbox.height

pixel_per_x = pixel_width / dx
pixel_per_y = pixel_height / dy

U_screen = U * pixel_per_x
V_screen = V * pixel_per_y

screen_magnitude = np.sqrt(
    U_screen**2 + V_screen**2
)

screen_magnitude = np.maximum(
    screen_magnitude,
    1e-12
)

U_screen_dir = U_screen / screen_magnitude
V_screen_dir = V_screen / screen_magnitude

# ================== 箭头参数 ==================
arrow_length = 40.0

U_screen_plot = U_screen_dir * arrow_length
V_screen_plot = V_screen_dir * arrow_length

U_plot = U_screen_plot / pixel_per_x
V_plot = V_screen_plot / pixel_per_y

mask = magnitude < 1e-8

U_plot[mask] = 0
V_plot[mask] = 0

# ============================================================
# 绘制向量场
# ============================================================
ax.quiver(
    Theta,
    Omega,
    U_plot,
    V_plot,
    magnitude,
    cmap=cmap,
    norm=norm,
    angles='xy',
    scale_units='xy',
    scale=1,
    pivot='tail',
    width=0.0020,
    headwidth=4.0,
    headlength=4.8,
    headaxislength=3.4
)

# ================== 数值求解轨迹 1 ==================
theta0_1 = -2.0
omega0_1 = 0.0

t_span = (0, 50)

t_eval = np.linspace(
    t_span[0],
    t_span[1],
    2000
)

sol1 = solve_ivp(
    pendulum_eq,
    t_span,
    [theta0_1, omega0_1],
    t_eval=t_eval,
    rtol=1e-8,
    atol=1e-10
)

theta_traj1 = sol1.y[0]
omega_traj1 = sol1.y[1]

# ================== 数值求解轨迹 2 ==================
theta0_2 = -3.0
omega0_2 = 6.0

sol2 = solve_ivp(
    pendulum_eq,
    t_span,
    [theta0_2, omega0_2],
    t_eval=t_eval,
    rtol=1e-8,
    atol=1e-10
)

theta_traj2 = sol2.y[0]
omega_traj2 = sol2.y[1]

# ============================================================
# 绘制轨迹
# ============================================================

# 轨迹 1
line1, = ax.plot(
    theta_traj1,
    omega_traj1,
    color='#00CED1',
    linewidth=2.0,
    label='轨迹 1 (初速度较慢)',
    zorder=3
)

# 轨迹 1 初始状态
ax.plot(
    theta0_1,
    omega0_1,
    'o',
    color='#00CED1',
    markersize=7,
    markeredgecolor='white',
    markeredgewidth=1.5,
    zorder=4
)

# 轨迹 2
line2, = ax.plot(
    theta_traj2,
    omega_traj2,
    color='#FF8C00',
    linewidth=2.0,
    label='轨迹 2 (初速度较快)',
    zorder=3
)

# 轨迹 2 初始状态
ax.plot(
    theta0_2,
    omega0_2,
    'o',
    color='#FF8C00',
    markersize=7,
    markeredgecolor='white',
    markeredgewidth=1.5,
    zorder=4
)

# ================== 坐标轴 ==================
ax.set_xlabel(
    r'$\theta$ (rad)'
)

ax.set_ylabel(
    r'$\dot{\theta}$ (rad/s)'
)

# ================== 图例 ==================
ax.legend(
    handles=[line1, line2],
    loc='upper right',
    prop=chinese_font,
    frameon=True
)

# ================== 网格 ==================
# ax.grid(alpha=0.3)

# ================== 坐标范围 ==================
ax.set_xlim(
    theta_min,
    theta_max
)

ax.set_ylim(
    omega_min,
    omega_max
)

# ================== 标记周期位置 ==================
for k in range(-2, 5):
    ax.axvline(
        x=k*np.pi,
        color='gray',
        linestyle='--',
        alpha=0.5
    )

# ================== 自动布局 ==================
fig.tight_layout()

# ================== 输出 PDF ==================
output_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'fig.pdf'
)

fig.savefig(
    output_path,
    format="pdf",
    bbox_inches="tight",
    transparent=True,
)

print(f'Figure saved to: {output_path}')

# ================== 显示图像 ==================
plt.show()