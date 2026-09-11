import bpy
import ctypes
from . import properties

class MWRT_PT_MainPanel(bpy.types.Panel):
    bl_label = "MWRT Pro: Performance Controller"
    bl_idname = "MWRT_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'MWRT Pro'

    def draw(self, layout):
        scene = bpy.context.scene
        props = scene.mwrt_props
        lib = properties.cpp_lib

        # --- System Monitor Section (Linked with C++ Memory Bridge) ---
        box = layout.box()
        box.label(text="Live System Monitor", icon='SYSTEM')
        
        if props.enable_memory_monitor:
            if lib is not None and hasattr(lib, 'get_system_ram_usage'):
                # Configure return types for C++ functions
                lib.get_system_ram_usage.restype = ctypes.c_float
                lib.get_available_vram_mb.restype = ctypes.c_int
                
                # Retrieve real-time metrics via C++ core engine
                ram_usage = lib.get_system_ram_usage()
                vram_available = lib.get_available_vram_mb()
                
                # Visual styling based on critical memory thresholds
                if ram_usage > 85.0:
                    row = box.row()
                    row.alert = True
                    row.label(text=f"RAM Usage: {ram_usage:.1f}% [CRITICAL]", icon='ERROR')
                else:
                    box.label(text=f"RAM Usage: {ram_usage:.1f}%", icon='INFO')
                    
                box.label(text=f"Available VRAM: {vram_available} MB", icon='NODE_COMPOSITING')
            else:
                box.label(text="RAM Usage: -- % (C++ core offline)", icon='QUESTION')
        else:
            box.label(text="Monitor Disabled", icon='MUTE')
            
        box.prop(props, "enable_memory_monitor")

        # --- Texture Optimization Section ---
        box = layout.box()
        box.label(text="Texture VRAM Control", icon='IMAGE_DATA')
        box.prop(props, "texture_resolution")
        box.operator("mwrt.apply_texture_limit", text="Update Textures", icon='REFRESH')

        # --- Animation Optimization Section ---
        box = layout.box()
        box.label(text="Animation RAM Control", icon='ANIM')
        box.operator("mwrt.freeze_animation", text="Freeze Selected Rig/Physics", icon='PLAY')
