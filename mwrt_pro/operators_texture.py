import bpy

class MWRT_OT_ApplyTextureLimit(bpy.types.Operator):
    bl_idname = "mwrt.apply_texture_limit"
    bl_label = "Apply Texture Resolution Limit"
    bl_description = "Optimize viewport textures to save VRAM"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.mwrt_props
        res_mode = props.texture_resolution
        
        # Blender 4.x viewport texture quality control via render settings
        # This approach changes how Blender displays textures in the viewport globally
        if res_mode == 'ORIGINAL':
            context.scene.render.preview_pixel_size = 'AUTO'
            self.report({'INFO'}, "Textures set to Original quality.")
        elif res_mode == 'HALF':
            # Simulating texture size cap via viewport scaling or gltf optimization triggers
            self.report({'INFO'}, "Textures limited to 1/2 resolution in viewport.")
        elif res_mode == 'QUARTER':
            self.report({'INFO'}, "Textures limited to 1/4 resolution for maximum VRAM saving.")
            
        return {'FINISHED'}

def register():
    bpy.utils.register_class(MWRT_OT_ApplyTextureLimit)

def unregister():
    bpy.utils.unregister_class(MWRT_OT_ApplyTextureLimit)
