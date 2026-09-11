# ModerateWeightReductionTools-X-MWRT-X-v2.0.0

A high-performance, modular optimization add-on for **Blender 4.x**, specifically engineered to eliminate RAM/VRAM bottlenecks in high-fidelity **Game Development** and **Cinematic/MV Production** pipelines.

By offloading heavy geometric and memory operations from Python to a custom **native C++ Core Engine**, MWRT Pro keeps your viewport timeline fluid and prevents application crashes when handling dense assets, complex animation rigs, and high-resolution PBR textures.

---

## 🌟 Key Features

### 1. Live System Memory Guard
* **Real-Time Telemetry:** Queries system RAM and GPU VRAM utilizing low-level C++ OS bridge routines.
* **Crash Prevention:** Displays a real-time monitor panel in the sidebar, changing to a critical alert state if resource thresholds cross 85% to mitigate memory allocation failures.

### 2. Fast Texture Resolution Downsampling
* **VRAM Relief:** Instantly reduces high-resolution textures (4K/8K) to 1/2 or 1/4 size via a fast multithreaded bilinear C++ scaling loop.
* **Fluid Assembly:** Keeps the viewport responsive during heavy scene layout work.

### 3. Vertex Animation Cache Compressor
* **Timeline Optimization:** Processes dense skeletal animations and cloth/physics simulations inside the C++ backend.
* **Jitter Removal:** Strips out sub-millimeter noise data based on configurable distance thresholds, maximizing viewport playback FPS for precise camera-work timing.

---

## 📂 Repository Structure

* `mwrt_pro/`: Python front-end, properties, operators, and the Blender user interface panel.
* `cpp/`: Native C++ source files handling heavy structural computations.
* `CMakeLists.txt`: Build automation configuration file for compiling the C++ shared binary.
* `.github/workflows/`: GitHub Actions automation scripts for multi-platform compilation and release generation.

---

## 🔧 Installation Guide

1. Download the pre-compiled **`mwrt_pro.zip`** from the [Latest GitHub Releases](https://github.com/hosimurayui/ModerateWeightReductionTools-X-MWRT-X-/releases/tag/v2.0.0)
2. Open Blender 4.x and navigate to `Edit > Preferences > Add-ons`.
3. Click `Install...` at the top right, select the downloaded `mwrt_pro.zip`, and check the box to enable it.
4. Open the 3D Viewport sidebar by pressing **`N`** and select the **MWRT Pro** tab.

---

## 🛠️ Developer Roadmap & Upcoming Features

The pre-configured C++ framework already contains optimization hooks for the following upcoming modules:
* `atlas_packer`: Fast rectangular-packing calculation to bake multiple assets into a single PBR drawer layout (reducing Draw Calls).
* `frustum_culler`: Advanced camera view-frustum occlusion calculation to dynamically hide off-screen geometry.
* `planar_dissolver` & `normal_transfer`: Smart flat-normal planar simplification while preserving model specular highlights via fast proximity vertex normal projections.

---

## 📄 License
This project is open-source and available under the MIT License.
