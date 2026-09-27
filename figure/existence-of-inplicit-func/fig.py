import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

plt.rcParams.update({
    "font.size": 13,
    "mathtext.fontset": "cm",
    "axes.unicode_minus": False,
})

# ---------- 配色 ----------
CURVE_COLOR  = "#7D7D7D"    # 主曲线（灰）
HIGHLIGHT    = "#D4AB43"    # 金黄：框内高亮曲线 / 局部高亮曲面
BOX_COLOR    = "#2A9D8F"    # 线框"在前面"的部分
SHADOW_COLOR = "#839E9B9D"  # 线框"在后面"的部分（阴影色，可调）
REGION_FILL  = "#DDE3E8"    # 淡灰：左图区域 D + 右图完整曲面

# ---------- 左图参数 ----------
cx, cy = 0.0, 0.0
rx, ry = 1.55, 1.45

def region_shape(t):
    return 1.0 + 0.08*np.sin(3*t + 0.4) + 0.05*np.cos(5*t + 0.9)

def region_boundary(t):
    r = region_shape(t)
    return cx + rx*r*np.cos(t), cy + ry*r*np.sin(t)

theta = np.linspace(0, 2*np.pi, 1200)
D_x, D_y = region_boundary(theta)

# ---------- 隐函数曲线：椭圆 ----------
t_ell = np.linspace(0, 2*np.pi, 1000)
a_e, b_e = 1.15, 0.85
ex = a_e * np.cos(t_ell)
ey = b_e * np.sin(t_ell)

t0 = 0.7
x0 = a_e * np.cos(t0)
y0 = b_e * np.sin(t0)

a_rect, b_rect = 0.58, 1.12
in_box = (ex >= a_rect) & (ex <= b_rect) & (ey > 0)
y_in = ey[in_box]
c_rect = y_in.min() - 0.08
d_rect = y_in.max() + 0.08

# ============================================================
# 画布：收窄宽度，使两图靠近
# ============================================================
fig = plt.figure(figsize=(11.0, 5.6))

# ---------- 左图 ----------
ax1 = fig.add_subplot(1, 2, 1)

ax1.fill(D_x, D_y, facecolor=REGION_FILL, alpha=0.9, edgecolor="none", zorder=1)
ax1.plot(ex, ey, color=CURVE_COLOR, linewidth=2.6, zorder=3)

rect = Rectangle((a_rect, c_rect), b_rect - a_rect, d_rect - c_rect,
                 fill=False, linewidth=2.2, linestyle="--",
                 edgecolor=BOX_COLOR, zorder=4)
ax1.add_patch(rect)

mask_rect = (ex >= a_rect) & (ex <= b_rect) & (ey >= c_rect) & (ey <= d_rect)
ax1.plot(ex[mask_rect], ey[mask_rect], color=HIGHLIGHT, linewidth=4.5, zorder=5)

ax1.scatter([x0], [y0], s=75, color="black", zorder=6)
ax1.text(x0 + 0.10, y0 + 0.1, r"$(x_0,y_0)$", fontsize=15,
         ha="left", va="top", zorder=6)
ax1.text(-1, 1, r"$F(x,y)=0$", fontsize=16,
         ha="left", va="center", zorder=6)

# 从黄色高亮曲线段引标注线，黄色字体 y = f(x)
idx_hl = np.where(mask_rect)[0]
idx_label = idx_hl[len(idx_hl) // 2]
xl, yl = ex[idx_label], ey[idx_label]

ax1.annotate(r"$y=f(x)$",
             xy=(xl-0.2, yl+0.15),
             xytext=(1, 1.20),
             fontsize=16,
             color=HIGHLIGHT,
             ha="left", va="center",
             arrowprops=dict(arrowstyle="-", color=HIGHLIGHT, lw=1.5),
             zorder=7)

ax1.set_xlim(-2.50, 2.50)
ax1.set_ylim(-2.38, 2.38)
ax1.set_aspect("equal", adjustable="box")
ax1.axis("off")

# ---------- 右图 ----------
ax2 = fig.add_subplot(1, 2, 2, projection="3d")
ax2.computed_zorder = False

X = np.linspace(-1.30, 1.30, 80)
Y = np.linspace(-1.30, 1.30, 80)
X, Y = np.meshgrid(X, Y)
Z = 0.5 * (X**2 + Y**2)

# 1) 完整曲面
surf_full = ax2.plot_surface(
    X, Y, Z, color=REGION_FILL, alpha=0.75,
    linewidth=0, antialiased=True
)
surf_full.set_zorder(1)

xmin, xmax = -0.70, 0.70
ymin, ymax = -0.70, 0.70
zmin, zmax = -0.05, 0.50

# 2) 局部高亮曲面
mask = (X >= xmin) & (X <= xmax) & (Y >= ymin) & (Y <= ymax)
Z_local = np.where(mask, Z, np.nan)
surf_local = ax2.plot_surface(
    X, Y, Z_local, color=HIGHLIGHT, alpha=0.85,
    linewidth=0, antialiased=True
)
surf_local.set_zorder(2)

# 3) 矩形柱的 12 条边
corners = [
    (xmin, ymin, zmin),  # 0
    (xmax, ymin, zmin),  # 1
    (xmax, ymax, zmin),  # 2
    (xmin, ymax, zmin),  # 3
    (xmin, ymin, zmax),  # 4
    (xmax, ymin, zmax),  # 5
    (xmax, ymax, zmax),  # 6
    (xmin, ymax, zmax),  # 7
]

SHADOW_RANGES = {
    (0, 1): None,
    (1, 2): None,
    (2, 3): (0.28, 1.0),
    (3, 0): (0.0, 0.48),
    (4, 5): (0.0, 1.0),
    (5, 6): (0.0, 1.0),
    (6, 7): (0.0, 0.66),
    (7, 4): (0.8, 1.0),
    (0, 4): None,
    (1, 5): None,
    (2, 6): (0.6, 1.0),
    (3, 7): (0.0, 1.0),
}

def draw_shadowed_edge(ax, p, q, shadow_range, lw=1.9):
    p = np.array(p, dtype=float)
    q = np.array(q, dtype=float)

    if shadow_range is None:
        ax.plot([p[0], q[0]], [p[1], q[1]], [p[2], q[2]],
                linestyle="--", linewidth=lw, color=BOX_COLOR, zorder=10)
        return

    t0, t1 = shadow_range
    segs = []
    if t0 > 1e-6:
        segs.append((0.0, t0, BOX_COLOR))
    if t1 - t0 > 1e-6:
        segs.append((t0, t1, SHADOW_COLOR))
    if t1 < 1 - 1e-6:
        segs.append((t1, 1.0, BOX_COLOR))

    for ta, tb, col in segs:
        ts = np.linspace(ta, tb, 40)
        pts = p[None, :] + ts[:, None] * (q - p)[None, :]
        ax.plot(pts[:, 0], pts[:, 1], pts[:, 2],
                linestyle="--", linewidth=lw, color=col, zorder=10)

for (i, j), rng_ in SHADOW_RANGES.items():
    draw_shadowed_edge(ax2, corners[i], corners[j], rng_)

# 4) 点与文字
pt = ax2.scatter([0], [0], [0], s=75, color="black", depthshade=False)
pt.set_zorder(11)
t1 = ax2.text(-0.4, 0, -0.3, r"$(x_0,y_0,z_0)$", fontsize=13)
t1.set_zorder(12)

# 右图：从黄色局部高亮曲面引标注线
p_start = np.array([0.30, 0.68, 0.5 * (0.30**2 + 0.68**2)])
p_end   = np.array([0.85, 1.25, 1])

ln, = ax2.plot([p_start[0], p_end[0]],
               [p_start[1], p_end[1]],
               [p_start[2], p_end[2]],
               color=HIGHLIGHT, linewidth=1.5)
ln.set_zorder(12)

t2 = ax2.text(p_end[0], p_end[1]+0.1, p_end[2], r"$z=g(x,y)$",
              fontsize=16, color=HIGHLIGHT)
t2.set_zorder(13)

t3 = ax2.text(-1.05, -0.85, 1.20, r"$F(x,y,z)=0$",
              fontsize=16, color="black")
t3.set_zorder(13)

ax2.set_xlim(-1.55, 1.55)
ax2.set_ylim(-1.55, 1.55)
ax2.set_zlim(-0.10, 1.80)
ax2.view_init(elev=22, azim=-60)

ax2.set_xticks([]); ax2.set_yticks([]); ax2.set_zticks([])
ax2.set_axis_off()
ax2.grid(False)

# 左右边界拉满，负 wspace 让两图紧贴
fig.subplots_adjust(left=0.0, right=1.0, top=1.0, bottom=0.0, wspace=-0.10)

fig.savefig("fig.pdf", format="pdf", bbox_inches="tight", transparent=True)
plt.show()
print("已生成：fig.pdf")