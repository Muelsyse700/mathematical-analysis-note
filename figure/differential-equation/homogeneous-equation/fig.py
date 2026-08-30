import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path


# ============================================================
# Matplotlib / LaTeX 风格
# ============================================================

plt.rcParams.update({
    "font.family": "serif",
    "mathtext.fontset": "cm",
    "axes.unicode_minus": False,
})


# ============================================================
# 绘图范围
# ============================================================

X_MIN, X_MAX = -3, 3
Y_MIN, Y_MAX = -3, 3

DENSITY = 23


# ============================================================
# 四阶 Runge-Kutta
# ============================================================

def rk4(f, x0, y0, x_end, step=0.003):
    """
    从初始点 (x0, y0) 出发，
    使用四阶 Runge-Kutta 方法求解

        y' = f(x, y)

    当解发散或离开计算范围时停止。
    """

    direction = 1 if x_end > x0 else -1
    h = direction * step

    x_list = [x0]
    y_list = [y0]

    x = x0
    y = y0

    max_steps = int(abs(x_end - x0) / step) + 1

    for _ in range(max_steps):

        # 到达终点
        if direction > 0 and x >= x_end:
            break

        if direction < 0 and x <= x_end:
            break

        # 最后一步
        if direction > 0:
            h_now = min(h, x_end - x)
        else:
            h_now = max(h, x_end - x)

        try:

            k1 = f(x, y)

            k2 = f(
                x + h_now / 2,
                y + h_now * k1 / 2
            )

            k3 = f(
                x + h_now / 2,
                y + h_now * k2 / 2
            )

            k4 = f(
                x + h_now,
                y + h_now * k3
            )

            y_new = y + h_now * (
                k1
                + 2 * k2
                + 2 * k3
                + k4
            ) / 6

        except (
            OverflowError,
            FloatingPointError
        ):
            break

        x_new = x + h_now

        # 数值发散
        if not np.isfinite(y_new):
            break

        # 提前停止，避免数值爆炸
        if abs(y_new) > 10:
            break

        x = x_new
        y = y_new

        x_list.append(x)
        y_list.append(y)

    return np.array(x_list), np.array(y_list)


# ============================================================
# 三个不同次数的齐次微分方程
#
# n = 0:
#
#       y' = y/x
#
# n = 1:
#
#       y' = x+y
#
# n = 2:
#
#       y' = x^2+y^2
# ============================================================

equations = [
    {
        "f": lambda x, y: y / x,
        "title": r"$y'=\dfrac{y}{x}$",
        "degree": r"$n=0$",
    },

    {
        "f": lambda x, y: x + y,
        "title": r"$y'=x+y$",
        "degree": r"$n=1$",
    },

    {
        "f": lambda x, y: x**2 + y**2,
        "title": r"$y'=x^2+y^2$",
        "degree": r"$n=2$",
    },
]


# ============================================================
# 创建画布
# ============================================================

fig, axes = plt.subplots(
    1,
    3,
    figsize=(12, 4),
)


# ============================================================
# 方向场网格
# ============================================================

x = np.linspace(
    X_MIN,
    X_MAX,
    DENSITY
)

y = np.linspace(
    Y_MIN,
    Y_MAX,
    DENSITY
)

X, Y = np.meshgrid(x, y)


# ============================================================
# 获取 Matplotlib 默认颜色
#
# 同一条解曲线的左右两个积分分支使用同一种颜色。
# ============================================================

colors = [
    "#0072B2",  # blue
    "#D55E00",  # vermilion
    "#009E73",  # green
    "#CC79A7",  # purple
    "#E69F00",  # orange
    "#56B4E9",  # sky blue
    "#F0E442",  # yellow
]


# ============================================================
# 开始绘制三个方程
# ============================================================

for equation_index, (ax, equation) in enumerate(
    zip(axes, equations)
):

    f = equation["f"]


    # ========================================================
    # 1. 绘制方向场
    # ========================================================

    with np.errstate(
        divide="ignore",
        invalid="ignore",
        over="ignore"
    ):

        slope = f(X, Y)

    slope[
        ~np.isfinite(slope)
    ] = np.nan


    # --------------------------------------------------------
    # 斜率 m 对应方向向量
    #
    #       (1,m)
    #
    # 归一化仅用于统一箭头长度。
    # --------------------------------------------------------

    U = np.ones_like(slope)
    V = slope

    length = np.sqrt(
        U**2 + V**2
    )

    U /= length
    V /= length


    # --------------------------------------------------------
    # quiver
    # --------------------------------------------------------

    ax.quiver(
        X,
        Y,
        U,
        V,
        angles="xy",
        pivot="mid",
        alpha=0.50,
        width=0.0025,
        headwidth=3.5,
        headlength=4.5,
    )


    # ========================================================
    # 2. 绘制解曲线
    # ========================================================

    if equation_index == 0:

        # ----------------------------------------------------
        # y' = y/x
        #
        # 精确解：
        #
        #       y = Cx
        #
        # x=0 是奇异点，因此左右两侧分别绘制。
        # ----------------------------------------------------

        constants = [
            -2,
            -1,
            -0.5,
            0.5,
            1,
            2,
        ]

        x_solution = np.linspace(
            X_MIN,
            X_MAX,
            1200
        )

        for color, C in zip(
            colors,
            constants
        ):

            y_solution = C * x_solution

            # x=0 处断开
            y_solution[
                np.abs(x_solution) < 1e-10
            ] = np.nan

            mask = (
                np.isfinite(y_solution)
                &
                (y_solution >= Y_MIN)
                &
                (y_solution <= Y_MAX)
            )

            ax.plot(
                x_solution[mask],
                y_solution[mask],
                color=color,
                linewidth=1.8
            )


    elif equation_index == 1:

        # ----------------------------------------------------
        # y' = x+y
        #
        # 精确解：
        #
        #       y = C e^x - x - 1
        # ----------------------------------------------------

        constants = [
            -0.8,
            -0.3,
            0.3,
            0.8,
            1.5,
        ]

        x_solution = np.linspace(
            X_MIN,
            X_MAX,
            2000
        )

        for color, C in zip(
            colors,
            constants
        ):

            y_solution = (
                C * np.exp(x_solution)
                - x_solution
                - 1
            )

            mask = (
                np.isfinite(y_solution)
                &
                (y_solution >= Y_MIN)
                &
                (y_solution <= Y_MAX)
            )

            ax.plot(
                x_solution[mask],
                y_solution[mask],
                color=color,
                linewidth=1.8
            )


    else:

        # ----------------------------------------------------
        # y' = x^2+y^2
        #
        # 使用数值积分。
        #
        # 每一个初始条件只对应一种颜色。
        #
        # 左右两个积分结果最后拼接成一条完整曲线，
        # 然后只调用一次 plot()。
        # ----------------------------------------------------

        initial_conditions = [
            (-2, -1),
            (-2, 0),
            (-2, 1),

            (0, -1),
            (0, 0),
            (0, 1),

            (2, -1),
            (2, 0),
            (2, 1),
        ]


        for color, (x0, y0) in zip(
            colors * 2,
            initial_conditions
        ):

            # ------------------------------------------------
            # 向左积分
            # ------------------------------------------------

            x_left, y_left = rk4(
                f,
                x0,
                y0,
                X_MIN
            )


            # ------------------------------------------------
            # 向右积分
            # ------------------------------------------------

            x_right, y_right = rk4(
                f,
                x0,
                y0,
                X_MAX
            )


            # ------------------------------------------------
            # 将左右两段拼成一条完整曲线
            #
            # 左边需要反转，因为当前顺序是：
            #
            #       x0 -> X_MIN
            #
            # 我们希望：
            #
            #       X_MIN -> x0 -> X_MAX
            # ------------------------------------------------

            x_full = np.concatenate([
                x_left[::-1],
                x_right[1:]
            ])

            y_full = np.concatenate([
                y_left[::-1],
                y_right[1:]
            ])


            # ------------------------------------------------
            # 只保留绘图区范围内的点
            #
            # 注意这里不再把不连续的两段强行连接。
            # ------------------------------------------------

            valid = (
                np.isfinite(x_full)
                &
                np.isfinite(y_full)
                &
                (y_full >= Y_MIN)
                &
                (y_full <= Y_MAX)
            )


            # ------------------------------------------------
            # 为了避免穿过发散点后产生错误连线，
            # 检查相邻点是否发生巨大跳跃。
            # ------------------------------------------------

            x_valid = x_full[valid]
            y_valid = y_full[valid]

            if len(x_valid) > 1:

                dx = np.diff(x_valid)
                dy = np.diff(y_valid)

                jump = np.sqrt(
                    dx**2 + dy**2
                )

                bad = np.where(
                    jump > 0.2
                )[0]

                if len(bad) > 0:

                    # 在第一个异常跳跃处截断
                    end = bad[0] + 1

                    x_valid = x_valid[:end]
                    y_valid = y_valid[:end]


            # ------------------------------------------------
            # 一次性绘制整条曲线
            # ------------------------------------------------

            ax.plot(
                x_valid,
                y_valid,
                color=color,
                linewidth=1.8
            )


    # ========================================================
    # 3. 坐标轴
    # ========================================================

    ax.axhline(
        0,
        linewidth=0.8
    )

    ax.axvline(
        0,
        linewidth=0.8
    )


    # ========================================================
    # 4. 坐标范围
    # ========================================================

    ax.set_xlim(
        X_MIN,
        X_MAX
    )

    ax.set_ylim(
        Y_MIN,
        Y_MAX
    )

    ax.set_aspect(
        "equal",
        adjustable="box"
    )


    # ========================================================
    # 5. 标题
    # ========================================================

    ax.set_title(
        equation["title"],
        fontsize=15,
        pad=8
    )

    ax.text(
        0.5,
        -0.18,
        equation["degree"],
        transform=ax.transAxes,
        ha="center",
        va="top",
        fontsize=12
    )


    # ========================================================
    # 6. 坐标标签
    # ========================================================

    ax.set_xlabel(
        r"$x$",
        fontsize=12
    )

    ax.set_ylabel(
        r"$y$",
        fontsize=12
    )


    # ========================================================
    # 7. 网格
    # ========================================================

    ax.grid(
        alpha=0.2,
        linewidth=0.6
    )

# ============================================================
# 保存 PDF 矢量图
# ============================================================

output_path = (
    Path(__file__).resolve().parent
    / "fig.pdf"
)

fig.savefig(
    output_path,
    format="pdf",
    bbox_inches="tight",
    transparent=True
)

print(
    f"图片已保存至：{output_path}"
)