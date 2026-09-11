import bpy
from bpy.props import EnumProperty, BoolProperty, PointerProperty

class MWRT_ProjectProperties(bpy.types.PropertyGroup):
    # Dynamic control for texture resolution to save VRAM
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
    
    # Toggle for the live memory tracking system
    enable_memory_monitor: BoolProperty(
        name="Enable Memory Monitor",
        description="Monitor VRAM/RAM thresholds to prevent Blender from crashing",
        default=True
    )

def register():
    bpy.utils.register_class(MWRT_ProjectProperties)
    # Bind properties to the scene data block
    bpy.types.Scene.mwrt_props = PointerProperty(type=MWRT_ProjectProperties)

def unregister():
    bpy.utils.unregister_class(MWRT_ProjectProperties)
    del bpy.types.Scene.mwrt_props
