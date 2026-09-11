import bpy
import ctypes
from . import properties

class MWRT_OT_ApplyTextureLimit(bpy.types.Operator):
    bl_idname = "mwrt.apply_texture_limit"
    bl_label = "Apply Texture Resolution Limit"
    bl_description = "Optimize viewport textures using high-performance C++ backend"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        props = context.scene.mwrt_props
        res_mode = props.texture_resolution
        
        # Access the loaded C++ library
        lib = properties.cpp_lib
        
        if lib is not None and hasattr(lib, 'resize_texture_rgba_fast'):
            self.report({'INFO'}, "Processing textures via C++ Core Engine...")
            
            # Set up ctypes argument and result types for C++ function binding
            # void resize_texture_rgba_fast(float* src, int sw, int sh, float* dst, int dw, int dh)
            lib.resize_texture_rgba_fast.argtypes = [
                ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.c_int,
                ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.c_int
            ]
            
            # Scan all images inside the Blender scene
            for img in bpy.data.images:
                if img.type == 'IMAGE' and img.pixels:
                    src_w, src_h = img.size[0], img.size[1]
                    
                    # Determine target dimensions based on user setting
                    scale = 1.0
                    if res_mode == 'HALF': scale = 0.5
                    elif res_mode == 'QUARTER': scale = 0.25
                    
                    if scale == 1.0:
                        continue
                        
                    dst_w = int(src_w * scale)
                    dst_h = int(src_h * scale)
                    
                    # Extract original pixel data arrays from Blender
                    # Moving data to native C arrays for rapid processing
                    src_pixels = (ctypes.c_float * len(img.pixels))(*img.pixels)
                    dst_pixels = (ctypes.c_float * (dst_w * dst_h * 4))()
                    
                    # Execute high-speed C++ downsampling loop
                    lib.resize_texture_rgba_fast(src_pixels, src_w, src_h, dst_pixels, dst_w, dst_h)
                    
                    # Apply optimized downsampled pixels back to Blender's image buffer
                    img.scale(dst_w, dst_h)
                    img.pixels = list(dst_pixels)
                    img.update()
                    
            self.report({'INFO'}, "All scene textures optimized using C++ engine.")
        else:
            # Fallback behavior if binary is missing
            self.report({'WARNING'}, "C++ backend unavailable. Using standard Blender scaling fallback.")
            if res_mode == 'ORIGINAL':
                context.scene.render.preview_pixel_size = 'AUTO'
            else:
                self.report({'INFO'}, f"Fallback applied for mode: {res_mode}")
                
        return {'FINISHED'}

def register():
    bpy.utils.register_class(MWRT_OT_ApplyTextureLimit)

def unregister():
    bpy.utils.unregister_class(MWRT_OT_ApplyTextureLimit)
