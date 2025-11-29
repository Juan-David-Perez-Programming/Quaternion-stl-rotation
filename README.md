================================================================================
AIRCRAFT QUATERNION ROTATION ANIMATOR
================================================================================

A Python-based 3D visualization tool that animates aircraft STL models using 
quaternion-based rotations. This project demonstrates sequential yaw-pitch-roll 
rotations with real-time visualization of orientation, quaternion components, 
and coordinate frame transformations.

================================================================================
FEATURES
================================================================================

- STL Model Loading: Imports and displays 3D aircraft models (tested with F-15)
- Quaternion Rotations: Smooth interpolation using SLERP (Spherical Linear 
  Interpolation)
- Sequential Animation: Demonstrates yaw → pitch → roll rotation sequence
- Dual Coordinate Systems: Displays both fixed global axes and rotating local 
  body axes
- Real-time Monitoring: Shows quaternion components (w, x, y, z) and rotation 
  progress
- Center of Mass Alignment: Automatically centers the aircraft at its COM for 
  realistic rotation
- Customizable: Easy-to-adjust rotation angles, animation speed, and 
  visualization parameters

================================================================================
REQUIREMENTS
================================================================================

numpy
matplotlib
trimesh
pyquaternion

================================================================================
INSTALLATION
================================================================================

1. Clone this repository:

git clone https://github.com/yourusername/aircraft-quaternion-animator.git
cd aircraft-quaternion-animator

2. Install dependencies:

pip install numpy matplotlib trimesh pyquaternion

3. Place your aircraft STL file (e.g., F15.stl) in the same directory as the 
   script.

================================================================================
USAGE
================================================================================

Run the animation:

python quaternion_rotator.py

--------------------------------------------------------------------------------
Customizing Rotations
--------------------------------------------------------------------------------

Modify the rotation angles in the code:

q_yaw = Quaternion(axis=[0, 0, 1], angle=np.pi/3)    # 60° yaw
q_pitch = Quaternion(axis=[0, 1, 0], angle=np.pi/6)  # 30° pitch
q_roll = Quaternion(axis=[1, 0, 0], angle=np.pi/4)   # 45° roll

--------------------------------------------------------------------------------
Animation Speed
--------------------------------------------------------------------------------

Adjust the frame rate:

n_frames = 601  # Total frames (higher = smoother but slower)
animation_interval = 1  # Milliseconds between frames

================================================================================
CODE STRUCTURE
================================================================================

- STL Loading & Preprocessing: Loads mesh, applies axis corrections, centers 
  at COM
- Quaternion Setup: Defines rotation quaternions for each axis
- SLERP Interpolation: slerp_sequential() smoothly interpolates between 
  rotation states
- Visualization: Renders aircraft mesh with dual coordinate systems
- Animation Loop: Updates mesh orientation and displays real-time quaternion 
  data

================================================================================
VISUALIZATION ELEMENTS
================================================================================

The animation displays:

- Aircraft mesh: Color-mapped surface with edges
- Global axes (dark): Fixed reference frame (darkred=X, darkgreen=Y, 
  darkblue=Z)
- Local axes (bright): Rotating body-fixed frame (red=X, lime=Y, cyan=Z)
- Quaternion components: Real-time w, x, y, z values
- Phase progress: Current rotation stage and completion percentage
- Target angles: Final rotation objectives for each axis

================================================================================
AEROSPACE CONVENTION
================================================================================

The code uses standard aerospace body-fixed axes:

- X-axis (Roll): Longitudinal (nose-to-tail)
- Y-axis (Pitch): Lateral (wing-to-wing)
- Z-axis (Yaw): Vertical (up-down)

Rotation sequence follows the 3-2-1 Euler angle convention (yaw → pitch → roll).

================================================================================
TECHNICAL DETAILS
================================================================================

Quaternion Multiplication: Uses intrinsic rotation order where 
q_combined = q_yaw * q_pitch * q_roll

SLERP: Ensures smooth, constant angular velocity transitions between 
orientations

Transformation Matrix: Quaternions are converted to 4×4 homogeneous 
transformation matrices for mesh rotation

================================================================================
TROUBLESHOOTING
================================================================================

File not found error: Ensure your STL file is in the same directory as the 
script, or provide the full path:

stl_path = '/full/path/to/your/F15.stl'

Incorrect orientation: Adjust the correction matrix to match your STL's native 
coordinate system.

================================================================================
REFERENCES
================================================================================

- pyquaternion Documentation: https://kieranwynn.github.io/pyquaternion/
- Trimesh Documentation: https://trimesh.org/
- Matplotlib 3D Animation Examples: 
  https://matplotlib.org/stable/gallery/animation/index.html

================================================================================
ACKNOWLEDGMENTS
================================================================================

Developed for aerospace engineering visualization and quaternion rotation 
demonstrations. Ideal for flight dynamics education and 3D orientation analysis.

--------------------------------------------------------------------------------
Author: David Perry
Date: November 2025
================================================================================
