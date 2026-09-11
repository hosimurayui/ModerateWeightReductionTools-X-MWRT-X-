bl_info = {
    "name": "Moderate Weight Reduction Tools Pro",
    "author": "Your Name",
    "version": (2, 0, 0),
    "blender": (4, 2, 0),
    "location": "View3D > Sidebar > MWRT Pro",
    "description": "Optimize VRAM/RAM consumption for high-fidelity assets and animations",
    "warning": "",
    "doc_url": "",
    "tracker_url": "",
    "category": "3D View"
}

import bpy
from . import properties

# List of modules to register
modules = [
    properties,
]

def register():
    for module in modules:
        module.register()
    print("MWRT Pro: Add-on successfully registered (Blender 4.x)")

def unregister():
    for module in reversed(modules):
        module.unregister()
    print("MWRT Pro: Add-on unregistered")

if __name__ == "__main__":
    register()
