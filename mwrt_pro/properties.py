import bpy
import os
import ctypes
import platform
from bpy.props import EnumProperty, BoolProperty, PointerProperty

# Global variable to hold the compiled C++ library instance
cpp_lib = None

def load_cpp_library():
    global cpp_lib
    if cpp_lib is not None:
        return cpp_lib
        
    # Get the directory of the current addon folder
    addon_dir = os.path.dirname(os.path.realpath(__file__))
    # Go up one level to search for compiled binaries (assuming a 'build' folder exists)
    root_dir = os.path.dirname(addon_dir)
    
    # Determine file extension based on the operating system
    system = platform.system()
    if system == "Windows":
        lib_name = "mwrt_core.dll"
    elif system == "Darwin": # macOS
        lib_name = "libmwrt_core.dylib"
    else: # Linux
        lib_name = "libmwrt_core.so"
        
    lib_path = os.path.join(root_dir, "build", lib_name)
    
    if os.path.exists(lib_path):
        try:
            cpp_lib = ctypes.CDLL(lib_path)
            print(f"MWRT Pro: Successfully loaded C++ core from {lib_path}")
        except Exception as e:
            print(f"MWRT Pro: Failed to load C++ library: {e}")
    else:
        print(f"MWRT Pro: C++ core binary not found at {lib_path}. Running in Python-only fallback mode.")
        
    return cpp_lib

class MWRT_ProjectProperties(bpy.types.PropertyGroup):
    texture_resolution: EnumProperty(
        name="Texture Resolution",
        description="Limit the texture resolution in the viewport to save VRAM",
        items=[
            ('ORIGINAL', "Original (4K/8K)", "Maintain original high-resolution textures"),
            ('HALF', "1/2 Resolution", "Limit viewport texture resolution to 50%"),
            ('QUARTER', "1/4 Resolution", "Drastically reduce VRAM usage by capping at 25%")
        ],
        default='ORIGINAL'
    )
    
    enable_memory_monitor: BoolProperty(
        name="Enable Memory Monitor",
        description="Monitor VRAM/RAM thresholds to prevent Blender from crashing",
        default=True
    )

def register():
    bpy.utils.register_class(MWRT_ProjectProperties)
    bpy.types.Scene.mwrt_props = PointerProperty(type=MWRT_ProjectProperties)
    # Attempt to load the C++ library when the addon is enabled
    load_cpp_library()

def unregister():
    global cpp_lib
    cpp_lib = None
    bpy.utils.unregister_class(MWRT_ProjectProperties)
    del bpy.types.Scene.mwrt_props
