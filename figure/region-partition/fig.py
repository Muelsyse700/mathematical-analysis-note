import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

# ----------------------------------------------------------------------
# 1. 随机生成一个边缘光滑的区域 D（星形区域，极坐标下用若干正弦项叠加）
# ----------------------------------------------------------------------
np.random.seed(2024)
theta = np.linspace(0, 2 * np.pi, 720)

r_base = 0.72
phases = np.random.uniform(0, 2 * np.pi, 3)
amps = np.random.uniform(0.04, 0.10, 3)

r = (r_base
     + amps[0] * np.sin(3 * theta + phases[0])
     + amps[1] * np.sin(5 * theta + phases[1])
     + amps[2] * np.cos(2 * theta + phases[2]))
r = np.clip(r, 0.50, 0.95)

x_bound = r * np.cos(theta)
y_bound = r * np.sin(theta)

# 包围 D 的正方形
A, B = -1.0, 1.0

# ----------------------------------------------------------------------
# 2. 判断点是否在 D 内
# ----------------------------------------------------------------------
def in_D(x, y):
    theta_pt = np.arctan2(y, x)
    theta_pt = np.where(theta_pt < 0, theta_pt + 2 * np.pi, theta_pt)
    r_bound = np.interp(theta_pt, theta, r)
    return np.sqrt(x ** 2 + y ** 2) <= r_bound

def classify(x0, x1, y0, y1, k=14):
    """判断小正方形与 D 的关系：'full' / 'partial' / 'out'"""
    xs = np.linspace(x0, x1, k)
    ys = np.linspace(y0, y1, k)
    X, Y = np.meshgrid(xs, ys)
    m = in_D(X, Y)
    if m.all():
        return "full"
    if m.any():
        return "partial"
    return "out"

# ----------------------------------------------------------------------
# 3. 现代美观配色
# ----------------------------------------------------------------------
C_FULL   = "#5B8FF9"   # 完全在 D 内的小正方形
C_PART   = "#F6BD16"   # 部分在 D 内的小正方形
C_GRID   = "#E0E0E0"   # 网格线
C_BOUND  = "#333333"   # 区域 D 边界
C_SQUARE = "#1A1A1A"   # 包围正方形

# ----------------------------------------------------------------------
# 4. 绘图：三幅图，网格由稀疏到超细
# ----------------------------------------------------------------------
fig, axes = plt.subplots(1, 3, figsize=(15, 5.2))
fig.patch.set_alpha(0.0)

for ax, n in zip(axes, (8, 32, 128)):
    ax.set_facecolor("none")
    edges = np.linspace(A, B, n + 1)
    step = edges[1] - edges[0]

    # 4.1 填充分割得到的小正方形
    for i in range(n):
        for j in range(n):
            x0, x1 = edges[i], edges[i + 1]
            y0, y1 = edges[j], edges[j + 1]
            kind = classify(x0, x1, y0, y1)
            if kind == "out":
                continue
            ax.add_patch(Rectangle(
                (x0, y0), x1 - x0, y1 - y0,
                facecolor=C_FULL if kind == "full" else C_PART,
                edgecolor="none", zorder=1, alpha=0.85))

    # 4.2 网格线（超细网格时淡化，避免糊成一片）
    lw_grid = 0.5 if n <= 32 else 0.15
    for e in edges:
        ax.plot([e, e], [A, B], color=C_GRID, lw=lw_grid, zorder=2)
        ax.plot([A, B], [e, e], color=C_GRID, lw=lw_grid, zorder=2)

    # 4.3 区域 D 的光滑边界
    ax.plot(np.append(x_bound, x_bound[0]),
            np.append(y_bound, y_bound[0]),
            color=C_BOUND, lw=1.5, zorder=3)

    # 4.4 框住 D 的正方形
    ax.add_patch(Rectangle((A, A), B - A, B - A,
                           facecolor="none", edgecolor=C_SQUARE,
                           lw=2.0, zorder=4))

    ax.set_xlim(A - 0.05, B + 0.05)
    ax.set_ylim(A - 0.05, B + 0.05)
    ax.set_aspect("equal")
    ax.axis("off")

plt.tight_layout()

# ----------------------------------------------------------------------
# 5. 保存图片（透明背景，生成于当前目录）
# ----------------------------------------------------------------------
fig.savefig("fig.pdf", transparent=True, bbox_inches="tight")

plt.show()