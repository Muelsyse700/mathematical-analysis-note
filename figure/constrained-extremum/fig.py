import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from pathlib import Path


# ============================================================
# Functions
# ============================================================

def f(x, y):
    return x**2 - y**2


# Constraint:
# x^2 / 4 + y^2 = 1
theta = np.linspace(0, 2 * np.pi, 800)

xc = 2 * np.cos(theta)
yc = np.sin(theta)
zc = f(xc, yc)


# ============================================================
# Four constrained stationary points
# ============================================================

# Parameter theta:
# ( 2,  0)
# ( 0,  1)
# (-2,  0)
# ( 0, -1)

points_xy = np.array([
    [ 2,  0],
    [ 0,  1],
    [-2,  0],
    [ 0, -1],
])

points_z = np.array([
    f( 2,  0),
    f( 0,  1),
    f(-2,  0),
    f( 0, -1),
])


# ============================================================
# Surface
# ============================================================

x = np.linspace(-2.4, 2.4, 300)
y = np.linspace(-1.7, 1.7, 300)

X, Y = np.meshgrid(x, y)
Z = f(X, Y)


# ============================================================
# Figure
# ============================================================

fig = plt.figure(figsize=(14, 6))

ax1 = fig.add_subplot(1, 2, 1)
ax2 = fig.add_subplot(1, 2, 2, projection="3d")


# ============================================================
# Four colors for corresponding points
# ============================================================

point_colors = [
    "tab:blue",
    "tab:orange",
    "tab:green",
    "tab:red",
]


# ============================================================
# Left: top view
# ============================================================

levels = np.arange(-4, 4.1, 0.5)

contours = ax1.contour(
    X,
    Y,
    Z,
    levels=levels,
    cmap="viridis",
    linewidths=1.0,
)

# Contour labels
ax1.clabel(
    contours,
    inline=True,
    fontsize=9,
    fmt=lambda value: rf"$f={value:g}$",
)

# Constraint ellipse
ax1.plot(
    xc,
    yc,
    linewidth=2.8,
)

ax1.text(
    -0.32,
    1.1,
    r"$\varphi(x,y)=0$",
    fontsize=12,
)

# Four corresponding points
for (px, py), color in zip(points_xy, point_colors):
    ax1.scatter(
        px,
        py,
        s=65,
        color=color,
        edgecolor="black",
        linewidth=0.6,
        zorder=10,
    )


# Only label x<0 and y<0 point
ax1.annotate(
    r"$\nabla f\parallel\nabla\varphi$",
    xy=(0, 0),
    xytext=(-232, -4),
    textcoords="offset points",
    fontsize=11,
)

ax1.annotate(
    r"$\nabla f\parallel\nabla\varphi$",
    xy=(0, 0),
    xytext=(-16.5, -112),
    textcoords="offset points",
    fontsize=11,
)


ax1.set_xlabel(r"$x$")
ax1.set_ylabel(r"$y$")
ax1.set_aspect("equal")

ax1.set_xlim(-2.45, 2.45)
ax1.set_ylim(-1.65, 1.65)

ax1.grid(alpha=0.15)

ax1.text(
    0.5, 1.02,
    r"$Oxy$",
    transform=ax1.transAxes,
    ha="center",
    va="bottom",
    fontsize=12,
)


# ============================================================
# Right: 3D saddle surface
# ============================================================

ax2.plot_surface(
    X,
    Y,
    Z,
    cmap=cm.viridis,
    alpha=0.65,
    linewidth=0,
    antialiased=True,
)


# ============================================================
# Ellipse on xy-plane
# ============================================================

z_plane = -2.8

ax2.plot(
    xc,
    yc,
    np.full_like(xc, z_plane),
    color="gray",
    linewidth=2.0,
    alpha=0.8,
)


# ============================================================
# Transparent vertical curtain connecting
# xy-plane ellipse and surface path
# ============================================================

# Reduce number of points for the curtain to keep PDF size reasonable
idx = np.linspace(0, len(theta) - 1, 250).astype(int)

theta_c = theta[idx]
xc_c = xc[idx]
yc_c = yc[idx]
zc_c = zc[idx]

Z_bottom = np.full_like(zc_c, z_plane)

# Construct the vertical curtain
curtain_X = np.vstack([
    xc_c,
    xc_c,
])

curtain_Y = np.vstack([
    yc_c,
    yc_c,
])

curtain_Z = np.vstack([
    Z_bottom,
    zc_c,
])

ax2.plot_surface(
    curtain_X,
    curtain_Y,
    curtain_Z,
    color="gray",
    alpha=0.18,
    linewidth=0,
    shade=False,
)


# ============================================================
# Constraint path on the saddle surface
# ============================================================

ax2.plot(
    xc,
    yc,
    zc,
    linewidth=3.5,
)


# ============================================================
# Four corresponding points on surface
# ============================================================

for (px, py), pz, color in zip(
    points_xy,
    points_z,
    point_colors,
):
    ax2.scatter(
        px,
        py,
        pz,
        s=75,
        color=color,
        edgecolor="black",
        linewidth=0.6,
        depthshade=False,
        zorder=20,
    )


# ============================================================
# Only label x<0 and y<0 point
# ============================================================

ax2.text(
    -2,
    0,
    4.35,
    r"$\nabla f\parallel\nabla\varphi$",
    fontsize=11,
)

ax2.text(
    0,
    -1,
    -1.65,
    r"$\nabla f\parallel\nabla\varphi$",
    fontsize=11,
)


# ============================================================
# 3D axes
# ============================================================

ax2.set_xlabel(r"$x$")
ax2.set_ylabel(r"$y$")
ax2.set_zlabel(r"$z$")

ax2.text2D(
    0.5, 0.95,
    r"$z=f(x,y)=x^2-y^2$",
    transform=ax2.transAxes,
    ha="center",
    va="top",
    fontsize=12,
)

ax2.set_xlim(-2.4, 2.4)
ax2.set_ylim(-1.7, 1.7)
ax2.set_zlim(z_plane, 4.5)

ax2.view_init(
    elev=28,
    azim=-55,
)

ax2.set_box_aspect(
    (1.4, 1, 0.8)
)


# ============================================================
# Transparent background
# ============================================================

fig.patch.set_alpha(0)

ax1.patch.set_alpha(0)
ax2.patch.set_alpha(0)


# ============================================================
# Save
# ============================================================

plt.tight_layout()

output = Path(__file__).resolve().parent / "fig.pdf"

fig.savefig(
    output,
    transparent=True,
    bbox_inches="tight",
)

plt.show()