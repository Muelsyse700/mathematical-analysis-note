import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

plt.rcParams.update({"font.family": "serif", "mathtext.fontset": "cm", "axes.unicode_minus": False})

colors = ["#0072B2", "#D55E00", "#009E73", "#CC79A7", "#E69F00", "#56B4E9", "#F0E442"]

x_min, x_max = -3, 3
y_min, y_max = -4, 4
density = 23

x = np.linspace(x_min, x_max, density)
y = np.linspace(y_min, y_max, density)
X, Y = np.meshgrid(x, y)

equations = [
    {
        "title": r"$y' + 2xy = 0$",
        "slope": lambda x, y: -2 * x * y,
        "solution": lambda x, C: C * np.exp(-x**2),
        "constants": [-2.5, -1.5, -0.8, 0, 0.8, 1.5, 2.5],
        "zero_slope": lambda x: np.zeros_like(x),
    },
    {
        "title": r"$y' + 2xy = 2x$",
        "slope": lambda x, y: 2 * x * (1 - y),
        "solution": lambda x, C: 1 + C * np.exp(-x**2),
        "constants": [-2.5, -1.5, -0.8, 0, 0.8, 1.5, 2.5],
        "zero_slope": lambda x: np.ones_like(x),
    },
    {
        "title": r"$y' - xy = 1-x^2$",
        "slope": lambda x, y: x * y + 1 - x**2,
        "solution": lambda x, C: x + C * np.exp(x**2 / 2),
        "constants": [-0.8, -0.4, 0, 0.4, 0.8],
        "zero_slope": lambda x: x - 1 / x,
    },
]

fig, axes = plt.subplots(1, 3, figsize=(12, 4.5))

for i, (ax, equation) in enumerate(zip(axes, equations)):
    ax.patch.set_alpha(0)

    # 坐标轴提前绘制，避免覆盖曲线
    ax.axhline(0, linewidth=0.8, zorder=0)
    ax.axvline(0, linewidth=0.8, zorder=0)

    # 绘制方向场
    slope = equation["slope"](X, Y)
    U = np.ones_like(slope)
    V = slope
    norm = np.sqrt(U**2 + V**2)
    U /= norm
    V /= norm

    arrow_length = 0.16
    U *= arrow_length
    V *= arrow_length

    ax.quiver(
        X, Y, U, V,
        angles="xy",
        scale_units="xy",
        scale=1,
        pivot="mid",
        color="black",
        alpha=0.45,
        width=0.0025,
        headwidth=3.5,
        headlength=4.5,
        zorder=1,
    )

    # 绘制解曲线
    x_solution = np.linspace(x_min, x_max, 4000)

    for color, C in zip(colors, equation["constants"]):
        y_solution = equation["solution"](x_solution, C)

        invalid = (
            ~np.isfinite(y_solution)
            | (y_solution < y_min)
            | (y_solution > y_max)
        )

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
            zorder=3,
        )

    # 绘制 y'=0 等斜线
    if i == 2:
        x_zero_left = np.linspace(x_min, -0.03, 2000)
        x_zero_right = np.linspace(0.03, x_max, 2000)

        y_zero_left = equation["zero_slope"](x_zero_left)
        y_zero_right = equation["zero_slope"](x_zero_right)

        invalid_left = (y_zero_left < y_min) | (y_zero_left > y_max)
        invalid_right = (y_zero_right < y_min) | (y_zero_right > y_max)

        y_zero_left[invalid_left] = np.nan
        y_zero_right[invalid_right] = np.nan

        ax.plot(
            x_zero_left,
            y_zero_left,
            color="#555555",
            linewidth=1.4,
            linestyle="--",
            alpha=0.8,
            zorder=2,
        )

        ax.plot(
            x_zero_right,
            y_zero_right,
            color="#555555",
            linewidth=1.4,
            linestyle="--",
            alpha=0.8,
            zorder=2,
        )
    else:
        y_zero = equation["zero_slope"](x_solution)

        invalid_zero = (
            ~np.isfinite(y_zero)
            | (y_zero < y_min)
            | (y_zero > y_max)
        )

        y_zero[invalid_zero] = np.nan

        ax.plot(
            x_solution,
            y_zero,
            color="#555555",
            linewidth=1.4,
            linestyle="--",
            alpha=0.8,
            zorder=2,
        )

    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)
    ax.set_aspect("equal", adjustable="box")

    ax.set_title(
        equation["title"],
        fontsize=16,
        pad=8,
    )

    ax.set_xlabel(r"$x$", fontsize=12)

    if i == 0:
        ax.set_ylabel(r"$y$", fontsize=12)
    else:
        ax.set_ylabel("")

    ax.grid(
        alpha=0.2,
        linewidth=0.6
    )

fig.subplots_adjust(
    left=0.06,
    right=0.99,
    bottom=0.12,
    top=0.90,
    wspace=-0.3,
)

output_path = Path(__file__).resolve().parent / "fig.pdf"

fig.savefig(
    output_path,
    format="pdf",
    bbox_inches="tight",
    transparent=True,
)

print(f"图片已保存至：{output_path}")