import bpy

class MWRT_PT_MainPanel(bpy.types.Panel):
    bl_label = "MWRT Pro: Performance Controller"
    bl_idname = "MWRT_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'MWRT Pro'

    def draw(self, layout):
        scene = bpy.context.scene
        props = scene.mwrt_props

        # Texture Optimization Section
        box = layout.box()
        box.label(text="Texture VRAM Control", icon='IMAGE_DATA')
        box.prop(props, "texture_resolution")
        box.operator("mwrt.apply_texture_limit", text="Update Textures", icon='REFRESH')

        # Animation Optimization Section
        box = layout.box()
        box.label(text="Animation RAM Control", icon='ANIM')
        box.operator("mwrt.freeze_animation", text="Freeze Selected Rig/Physics", icon='PLAY')

        # System Monitor Toggle
        box = layout.box()
        box.label(text="System Protection", icon='SYSTEM')
        box.prop(props, "enable_memory_monitor")
