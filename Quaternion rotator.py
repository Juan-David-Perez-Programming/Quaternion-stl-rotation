import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import trimesh
from pyquaternion import Quaternion
import os

# Fix file path - use full path to your STL file
script_dir = os.path.dirname(os.path.abspath(__file__))
stl_path = os.path.join(script_dir, 'F15.stl')

# Verify file exists and load
if os.path.exists(stl_path):
    print(f"Loading: {stl_path}")
    aircraft = trimesh.load(stl_path)
    print(f"Loaded: {len(aircraft.vertices)} vertices, {len(aircraft.faces)} faces")
else:
    # Fallback: try direct path if file is in same folder
    print(f"File not found at: {stl_path}")
    print(f"Trying current directory...")
    aircraft = trimesh.load('F15.stl')

# Fix imported STL orientation
correction_matrix = np.array([
    [0, 0, -1, 0],
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 0, 1]
])
aircraft.apply_transform(correction_matrix)
print("Applied axis correction to imported mesh")

# Center mesh at COM (center of mass)
com = aircraft.center_mass
print(f"Center of Mass: {com}")
aircraft.vertices -= com
print("Centered mesh at COM")

# Define individual rotations
q_yaw = Quaternion(axis=[0, 0, 1], angle=np.pi/3)    # Yaw about Z-axis (60°)
q_pitch = Quaternion(axis=[0, 1, 0], angle=np.pi/6)  # Pitch about Y-axis (30°)
q_roll = Quaternion(axis=[1, 0, 0], angle=np.pi/4)   # Roll about X-axis (45°)

# Sequential quaternions
q_after_yaw = q_yaw
q_after_pitch = q_yaw * q_pitch
q_combined = q_yaw * q_pitch * q_roll

def slerp_sequential(t):
    """Apply rotations sequentially: yaw → pitch → roll"""
    if t <= 1/3:
        t_norm = t * 3
        return Quaternion.slerp(Quaternion(), q_after_yaw, t_norm)
    elif t <= 2/3:
        t_norm = (t - 1/3) * 3
        return Quaternion.slerp(q_after_yaw, q_after_pitch, t_norm)
    else:
        t_norm = (t - 2/3) * 3
        return Quaternion.slerp(q_after_pitch, q_combined, t_norm)

# Function to plot coordinate axes
def plot_axes(ax, origin, vectors, colors, label_prefix, linestyle='-', alpha=1.0, arrow_length_ratio=0.2, linewidth=2.5):
    for vec, color, label in zip(vectors, colors, ['x', 'y', 'z']):
        ax.quiver(*origin, *vec, color=color, linewidth=linewidth, 
                 label=f'{label_prefix}{label}', 
                 alpha=alpha, arrow_length_ratio=arrow_length_ratio)

# Global axes (identity rotation)
global_axes = np.eye(3) * 15000  # Scale to aircraft size
origin = np.zeros(3)
colors_global = ['darkred', 'darkgreen', 'darkblue']
colors_rotated = ['red', 'lime', 'cyan']

# Setup animation
fig = plt.figure(figsize=(14, 11))
ax = fig.add_subplot(111, projection='3d')
n_frames = 601
animation_interval = 1

def update(frame):
    ax.cla()
    
    # Get interpolated quaternion
    t = frame / (n_frames - 1)
    q_interp = slerp_sequential(t)
    
    # Convert to transformation matrix and apply
    rotated_mesh = aircraft.copy()
    rotated_mesh.apply_transform(q_interp.transformation_matrix)
    
    # Plot mesh
    ax.plot_trisurf(rotated_mesh.vertices[:, 0],
                   rotated_mesh.vertices[:, 1],
                   rotated_mesh.vertices[:, 2],
                   triangles=rotated_mesh.faces,
                   cmap='coolwarm', alpha=0.85, edgecolor='k', linewidth=0.1)
    
    # Plot global axes (fixed) - darker and thinner
    plot_axes(ax, origin, global_axes, colors_global, 'Global ', 
             linestyle='-', alpha=0.3, arrow_length_ratio=0.15, linewidth=1.5)
    
    # Rotate axes using interpolated quaternion
    rotated_axes = np.array([q_interp.rotate(vec) for vec in global_axes])
    
    # Plot local rotated axes - bright colors, thick, solid
    plot_axes(ax, origin, rotated_axes, colors_rotated, 'Local ', 
             linestyle='-', alpha=1.0, arrow_length_ratio=0.3, linewidth=4)
    
    # Determine phase
    if t <= 1/3:
        phase = "Yaw (Z-axis)"
        progress = t * 3 * 100
        phase_color = 'blue'
    elif t <= 2/3:
        phase = "Pitch (Y-axis)"
        progress = (t - 1/3) * 3 * 100
        phase_color = 'green'
    else:
        phase = "Roll (X-axis)"
        progress = (t - 2/3) * 3 * 100
        phase_color = 'red'
    
    # Set view - centered at origin (COM)
    ax.set_xlim([-25000, 25000])
    ax.set_ylim([-25000, 25000])
    ax.set_zlim([-25000, 25000])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(f'{phase} - Overall: {t*100:.0f}%', fontsize=14)
    ax.view_init(elev=30, azim=20)
    
    # Add text showing rotation progress
    ax.text2D(0.05, 0.95, f'Overall: {t*100:.0f}%', transform=ax.transAxes, fontsize=12)
    
    if t <= 1/3:
        ax.text2D(0.05, 0.90, f'Yaw: {progress:.0f}%', transform=ax.transAxes, fontsize=10, color='blue')
    elif t <= 2/3:
        ax.text2D(0.05, 0.90, f'Pitch: {progress:.0f}%', transform=ax.transAxes, fontsize=10, color='green')
    else:
        ax.text2D(0.05, 0.90, f'Roll: {progress:.0f}%', transform=ax.transAxes, fontsize=10, color='red')
    
    # Display quaternion components (w, x, y, z)
    ax.text2D(0.05, 0.85, 'Current Quaternion:', transform=ax.transAxes, fontsize=11, weight='bold')
    ax.text2D(0.05, 0.81, f'w = {q_interp.w:.4f}', transform=ax.transAxes, fontsize=9, family='monospace')
    ax.text2D(0.05, 0.77, f'x = {q_interp.x:.4f}', transform=ax.transAxes, fontsize=9, family='monospace', color='red')
    ax.text2D(0.05, 0.73, f'y = {q_interp.y:.4f}', transform=ax.transAxes, fontsize=9, family='monospace', color='green')
    ax.text2D(0.05, 0.69, f'z = {q_interp.z:.4f}', transform=ax.transAxes, fontsize=9, family='monospace', color='blue')
    
    # Display magnitude (should always be 1 for unit quaternions)
    mag = np.sqrt(q_interp.w**2 + q_interp.x**2 + q_interp.y**2 + q_interp.z**2)
    ax.text2D(0.05, 0.65, f'|q| = {mag:.4f}', transform=ax.transAxes, fontsize=9, family='monospace')
    
    # Display target angles
    ax.text2D(0.05, 0.58, 'Target Angles:', transform=ax.transAxes, fontsize=10, weight='bold')
    ax.text2D(0.05, 0.54, f'Yaw:   60°', transform=ax.transAxes, fontsize=9, color='blue')
    ax.text2D(0.05, 0.50, f'Pitch: 30°', transform=ax.transAxes, fontsize=9, color='green')
    ax.text2D(0.05, 0.46, f'Roll:  45°', transform=ax.transAxes, fontsize=9, color='red')
    
    # Add legend for axes
    ax.legend(loc='upper right', fontsize=8)
    
    return []

ani = FuncAnimation(fig, update, frames=n_frames,
                   interval=animation_interval, blit=False, repeat=True)
plt.show()
