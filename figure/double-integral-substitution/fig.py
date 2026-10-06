import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, ConnectionPatch

plt.rcParams['mathtext.fontset'] = 'cm'
plt.rcParams['font.family'] = 'serif'

# ============ 配色 ============
C_BG    = '#E8F0FE'
C_GRID  = '#A8B8CC'
C_EDGE  = '#34495E'
C_AXIS  = '#000000'   # 坐标轴及普通文字：纯黑
C_HL    = '#FFD166'
C_HL_ED = '#E09422'
C_ARROW = '#34495E'
C_PT    = '#C0392B'   # 特殊点文字仍为红色

# ============ 画布 ============
fig = plt.figure(figsize=(18, 9))
fig.patch.set_alpha(0.0)

ax1 = fig.add_axes([0.04, 0.08, 0.42, 0.80])
ax2 = fig.add_axes([0.54, 0.08, 0.42, 0.80])

# ============ 网格参数 ============
n = 4
r_edges     = np.linspace(0, 1, n + 1)
theta_edges = np.linspace(0, np.pi / 2, n + 1)

hi, hj = 2, 2
r0, r1 = r_edges[hi], r_edges[hi + 1]
t0, t1 = theta_edges[hj], theta_edges[hj + 1]

t0_scaled = t0 / (np.pi / 2)
t1_scaled = t1 / (np.pi / 2)

# ================= 左图：(r, θ) =================
ax1.set_facecolor('none')
ax1.add_patch(Rectangle((0, 0), 1, 1, facecolor=C_BG, edgecolor='none', zorder=1))

for r in r_edges:
    ax1.plot([r, r], [0, 1], color=C_GRID, lw=1.4, zorder=2)
for t in np.linspace(0, 1, n + 1):
    ax1.plot([0, 1], [t, t], color=C_GRID, lw=1.4, zorder=2)

ax1.add_patch(Rectangle((r0, t0_scaled), r1 - r0, t1_scaled - t0_scaled,
                        facecolor=C_HL, edgecolor=C_HL_ED, lw=3.0, zorder=3))
ax1.add_patch(Rectangle((0, 0), 1, 1, facecolor='none',
                        edgecolor=C_EDGE, lw=2.6, zorder=4))

ax1.annotate('', xy=(1.15, 0), xytext=(-0.02, 0),
             arrowprops=dict(arrowstyle='-|>', color=C_AXIS, lw=2.4, mutation_scale=28),
             zorder=5, annotation_clip=False)
ax1.annotate('', xy=(0, 1.15), xytext=(0, -0.02),
             arrowprops=dict(arrowstyle='-|>', color=C_AXIS, lw=2.4, mutation_scale=28),
             zorder=5, annotation_clip=False)

# ---- 左图 r 轴刻度 ----
for r in [0, 0.5, 1.0]:
    ax1.plot([r, r], [-0.03, 0.03], color=C_AXIS, lw=2.4, zorder=6, clip_on=False)
    ax1.text(r, -0.05, f'${r:g}$',               # <-- 横轴刻度位置：-0.09
             ha='center', va='top', fontsize=22, color=C_AXIS)

# ---- 左图 θ 轴刻度 ----
for t_scaled, lab in [(0, '$0$'), (0.5, r'$\pi/4$'), (1.0, r'$\pi/2$')]:
    ax1.plot([-0.03, 0.03], [t_scaled, t_scaled], color=C_AXIS, lw=2.4,
             zorder=6, clip_on=False)
    ax1.text(-0.05, t_scaled, lab, ha='right', va='center',
             fontsize=22, color=C_AXIS)

ax1.text(1.19, 0, '$r$', fontsize=32, color=C_AXIS, ha='left', va='center')
ax1.text(0, 1.135, r'$\theta$', fontsize=32, color=C_AXIS, ha='center', va='bottom')

# 左图四个点 P1..P4（红色）
P1 = (r0, t0_scaled)
P2 = (r1, t0_scaled)
P3 = (r0, t1_scaled)
P4 = (r1, t1_scaled)
for (x, y), lab, ox, oy in [(P1, '$P_1$', -0.07, -0.06),
                            (P2, '$P_2$',  0.07, -0.06),
                            (P3, '$P_3$', -0.07,  0.06),
                            (P4, '$P_4$',  0.07,  0.06)]:
    ax1.plot(x, y, 'o', color=C_PT, markersize=11, zorder=8)
    ax1.text(x + ox, y + oy, lab, fontsize=22, color=C_PT,
             ha='center', va='center', zorder=9)

ax1.set_xlim(-0.14, 1.24)
ax1.set_ylim(-0.14, 1.24)
ax1.set_aspect('equal')
ax1.set_box_aspect(1)
ax1.axis('off')

# ================= 右图：(x, y) =================
ax2.set_facecolor('none')

t_q = np.linspace(0, np.pi / 2, 300)
qx = np.concatenate([[0], np.cos(t_q), [0]])
qy = np.concatenate([[0], np.sin(t_q), [0]])
ax2.fill(qx, qy, facecolor=C_BG, edgecolor='none', zorder=1)

for r in r_edges:
    if r == 0:
        continue
    t_arr = np.linspace(0, np.pi / 2, 150)
    ax2.plot(r * np.cos(t_arr), r * np.sin(t_arr), color=C_GRID, lw=1.4, zorder=2)
for th in theta_edges:
    ax2.plot([0, np.cos(th)], [0, np.sin(th)], color=C_GRID, lw=1.4, zorder=2)

t_hl = np.linspace(t0, t1, 80)
ix = r0 * np.cos(t_hl);  iy = r0 * np.sin(t_hl)
ox_ = r1 * np.cos(t_hl[::-1]);  oy_ = r1 * np.sin(t_hl[::-1])
ax2.fill(np.concatenate([ix, ox_]), np.concatenate([iy, oy_]),
         facecolor=C_HL, edgecolor=C_HL_ED, lw=3.0, zorder=3)

ax2.plot(np.cos(t_q), np.sin(t_q), color=C_EDGE, lw=2.6, zorder=4)

ax2.annotate('', xy=(1.15, 0), xytext=(-0.02, 0),
             arrowprops=dict(arrowstyle='-|>', color=C_AXIS, lw=2.4, mutation_scale=28),
             zorder=5, annotation_clip=False)
ax2.annotate('', xy=(0, 1.15), xytext=(0, -0.02),
             arrowprops=dict(arrowstyle='-|>', color=C_AXIS, lw=2.4, mutation_scale=28),
             zorder=5, annotation_clip=False)

# ---- 右图 x 轴刻度 ----
for x in [0, 0.5, 1.0]:
    ax2.plot([x, x], [-0.03, 0.03], color=C_AXIS, lw=2.4, zorder=6, clip_on=False)
    ax2.text(x, -0.05, f'${x:g}$',               # <-- 横轴刻度位置：-0.09
             ha='center', va='top', fontsize=22, color=C_AXIS)

# ---- 右图 y 轴刻度 ----
for y in [0, 0.5, 1.0]:
    ax2.plot([-0.03, 0.03], [y, y], color=C_AXIS, lw=2.4, zorder=6, clip_on=False)
    ax2.text(-0.05, y, f'${y:g}$', ha='right', va='center', fontsize=22, color=C_AXIS)

ax2.text(1.19, 0, '$x$', fontsize=32, color=C_AXIS, ha='left', va='center')
ax2.text(0, 1.15, '$y$', fontsize=32, color=C_AXIS, ha='center', va='bottom')

# 右图四个点 M1..M4（红色）
M1 = (r0 * np.cos(t0), r0 * np.sin(t0))
M2 = (r1 * np.cos(t0), r1 * np.sin(t0))
M3 = (r0 * np.cos(t1), r0 * np.sin(t1))
M4 = (r1 * np.cos(t1), r1 * np.sin(t1))

offsets = {
    'M1': (-0.00, -0.06),
    'M2': ( 0.09,  0.00),
    'M3': (-0.09,  0.00),
    'M4': ( 0.00,  0.06),
}
for (x, y), lab, key in [(M1, '$M_1$', 'M1'), (M2, '$M_2$', 'M2'),
                         (M3, '$M_3$', 'M3'), (M4, '$M_4$', 'M4')]:
    ax2.plot(x, y, 'o', color=C_PT, markersize=11, zorder=8)
    ox, oy = offsets[key]
    ax2.text(x + ox, y + oy, lab, fontsize=22, color=C_PT,
             ha='center', va='center', zorder=9)

ax2.set_xlim(-0.14, 1.24)
ax2.set_ylim(-0.14, 1.24)
ax2.set_aspect('equal')
ax2.set_box_aspect(1)
ax2.axis('off')

# ================= 连接箭头 =================
rc = (r0 + r1) / 2
tc = (t0 + t1) / 2
xc = rc * np.cos(tc)
yc = rc * np.sin(tc)

arrow = ConnectionPatch(
    xyA=(rc, tc / (np.pi / 2)), xyB=(xc, yc),
    coordsA='data', coordsB='data',
    axesA=ax1, axesB=ax2,
    arrowstyle='-|>', mutation_scale=36,
    color=C_ARROW, lw=3.0, zorder=10,
    shrinkA=0, shrinkB=0,
)
fig.add_artist(arrow)

fig.text(0.50, 0.05,
         r'$(r,\theta)\;\longmapsto\;(x,y)$',
         ha='center', va='center', fontsize=28, color=C_AXIS)

fig.savefig('fig.pdf', transparent=True, bbox_inches='tight')

plt.show()