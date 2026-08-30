import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# Matplotlib / LaTeX 风格
plt.rcParams.update({
    "font.family": "serif",
    "mathtext.fontset": "cm",
    "axes.unicode_minus": False,
})

# Okabe–Ito 配色
colors = [
    "#0072B2", "#D55E00", "#009E73", "#CC79A7",
    "#E69F00", "#56B4E9", "#F0E442",
]

special_color = "#222222"

# 绘图范围
x_min, x_max = -3, 3
y_min, y_max = -3, 5
density = 25

# 网格
x = np.linspace(x_min, x_max, density)
y = np.linspace(y_min, y_max, density)
X, Y = np.meshgrid(x, y)

# 三个可分离变量的一阶微分方程
equations = [
    {
        "title": r"$y'=x(1+y)$",
        "slope": lambda X, Y: X * (1 + Y),
        "solution": lambda x, C: C * np.exp(x**2 / 2) - 1,
        "constants": [-0.8, -0.4, -0.15, 0.15, 0.4, 0.8],
    },
    {
        "title": r"$y'=y(1-y)$",
        "slope": lambda X, Y: Y * (1 - Y),
        "solution": lambda x, C: 1 / (1 + C * np.exp(-x)),
        "constants": [-2.0, -0.8, -0.2, 0.2, 0.8, 2.0, 5.0],
    },
    {
        "title": r"$y'=y\,\sin x$",
        "slope": lambda X, Y: Y * np.sin(X),
        "solution": lambda x, C: C * np.exp(-np.cos(x)),
        "constants": [-2.0, -1.0, -0.4, 0.4, 1.0, 2.0, 3.0],
    },
]

# 创建画布
fig, axes = plt.subplots(1, 3, figsize=(12, 4.5))

for i, (ax, equation) in enumerate(zip(axes, equations)):
    ax.patch.set_alpha(0)

    # 方向场
    slope = equation["slope"](X, Y)
    U = np.ones_like(slope)
    V = slope
    length = np.sqrt(U**2 + V**2)
    U /= length
    V /= length

    ax.quiver(
        X, Y, U, V,
        angles="xy",
        pivot="mid",
        alpha=0.45,
        width=0.0025,
        headwidth=3.5,
        headlength=4.5,
    )

    # 坐标轴
    ax.axhline(0, linewidth=0.8)
    ax.axvline(0, linewidth=0.8)

    # 通解曲线
    x_solution = np.linspace(x_min, x_max, 4000)

    for color, C in zip(colors, equation["constants"]):
        y_solution = equation["solution"](x_solution, C)

        invalid = (
            ~np.isfinite(y_solution)
            | (y_solution < y_min)
            | (y_solution > y_max)
        )

        # 检测竖直渐近线造成的跳变
        jump = np.zeros_like(y_solution, dtype=bool)
        jump[1:] = np.abs(np.diff(y_solution)) > 0.2

        invalid |= jump
        invalid[:-1] |= jump[1:]

        y_plot = y_solution.copy()
        y_plot[invalid] = np.nan

        ax.plot(
            x_solution,
            y_plot,
            color=color,
            linewidth=1.8,
        )

    # 第一幅：特殊解 y=-1
    if i == 0:
        ax.plot(
            x_solution,
            -np.ones_like(x_solution),
            color=special_color,
            linewidth=2.2,
        )

    # 第二幅：特殊解 y=0 和 y=1
    if i == 1:
        ax.plot(
            x_solution,
            np.zeros_like(x_solution),
            color=special_color,
            linewidth=2.2,
        )

        ax.plot(
            x_solution,
            np.ones_like(x_solution),
            color=special_color,
            linewidth=2.2,
        )

    # 坐标范围
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_aspect("equal", adjustable="box")

    # 标题
    ax.set_title(
        equation["title"],
        fontsize=16,
        pad=8,
    )

    # 坐标标签
    ax.set_xlabel(r"$x$", fontsize=12)

    if i == 0:
        ax.set_ylabel(r"$y$", fontsize=12)
    else:
        ax.set_ylabel("")

    # 网格
    ax.grid(
        alpha=0.2,
        linewidth=0.6,
    )

# 压缩子图间距
fig.subplots_adjust(
    left=0.06,
    right=0.99,
    bottom=0.12,
    top=0.90,
    wspace=-0.3,
)

# 保存为透明背景 PDF 矢量图
output_path = (
    Path(__file__).resolve().parent
    / "fig.pdf"
)

fig.savefig(
    output_path,
    format="pdf",
    bbox_inches="tight",
    transparent=True,
)

print(f"图片已保存至：{output_path}")