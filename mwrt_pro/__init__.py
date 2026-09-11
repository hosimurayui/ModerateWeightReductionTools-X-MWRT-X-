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
from . import operators_texture
from . import operators_anim
from . import ui_panel

# Add all submodule components to the list
modules = [
    properties,
    operators_texture,
    operators_anim,
    ui_panel,
]

def register():
    for module in modules:
        module.register()
    print("MWRT Pro: All modules successfully registered (Blender 4.x)")

def unregister():
    for module in reversed(modules):
        module.unregister()
    print("MWRT Pro: Add-on successfully unregistered")

if __name__ == "__main__":
    register()
