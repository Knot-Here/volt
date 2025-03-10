import numpy as np
import matplotlib.pyplot as plt

# Set up figure with higher resolution and quality
plt.rcParams["figure.dpi"] = 100
plt.rcParams["figure.figsize"] = [10, 8]

# Define parameters
sigmaB = 0.7  # Asset B volatility (fixed)

# Create higher resolution grid for smoother surface
resolution = 100
sigmaA_vals = np.linspace(0, 1.0, resolution)  # Asset A volatility range
rho_vals = np.linspace(-1, 1, resolution)  # Correlation range
X, Y = np.meshgrid(sigmaA_vals, rho_vals)

# Calculate the relative volatility
Z = np.sqrt(X**2 + sigmaB**2 - 2 * Y * X * sigmaB)

# Calculate min and max for better color scaling
z_min = np.min(Z)
z_max = np.max(Z)
print(f"Min V_rel: {z_min:.4f}, Max V_rel: {z_max:.4f}")

# Create the 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

# Use a colormap that shows the gradation more clearly
surf = ax.plot_surface(
    X, Y, Z, cmap="viridis", linewidth=0, antialiased=True, vmin=z_min, vmax=z_max
)

# Set viewing angle to better see the maximum points
ax.view_init(elev=30, azim=240)

# Add labels and title
ax.set_xlabel("Volatility of Asset A (σ_A)", fontsize=12, labelpad=10)
ax.set_ylabel("Correlation (ρ)", fontsize=12, labelpad=10)
ax.set_zlabel("Relative Volatility (V_rel)", fontsize=12, labelpad=10)
ax.set_title(f"3D Surface of V_rel for σ_B = {sigmaB:.1f}", fontsize=14)

# Add a color bar
cbar = fig.colorbar(surf, shrink=0.6, aspect=10)
cbar.set_label("Relative Volatility (V_rel)", fontsize=12)

# Add grid lines for better perspective
ax.grid(True)

# Add text annotation for key points
max_idx = np.unravel_index(np.argmax(Z), Z.shape)
max_sigmaA = sigmaA_vals[max_idx[1]]
max_rho = rho_vals[max_idx[0]]
max_value = Z[max_idx]

# Highlight maximum point with a marker
ax.scatter(
    [max_sigmaA],
    [max_rho],
    [max_value],
    color="red",
    s=100,
    marker="*",
    label=f"Max: {max_value:.2f}",
)

# Highlight minimum point
min_idx = np.unravel_index(np.argmin(Z), Z.shape)
min_sigmaA = sigmaA_vals[min_idx[1]]
min_rho = rho_vals[min_idx[0]]
min_value = Z[min_idx]
ax.scatter(
    [min_sigmaA],
    [min_rho],
    [min_value],
    color="blue",
    s=100,
    marker="o",
    label=f"Min: {min_value:.2f}",
)

ax.legend()

# Add contour lines on the bottom surface for clearer visualization
cset = ax.contourf(X, Y, Z, zdir="z", offset=0, cmap="viridis", alpha=0.5)

plt.tight_layout()
plt.show()
