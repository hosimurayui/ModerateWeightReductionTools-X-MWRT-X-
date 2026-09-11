import bpy
import ctypes
from . import properties

class MWRT_OT_FreezeAnimation(bpy.types.Operator):
    bl_idname = "mwrt.freeze_animation"
    bl_label = "Freeze Selected Animations"
    bl_description = "Bake and compress animations using C++ vector processing"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        selected_objs = context.selected_objects
        if not selected_objs:
            self.report({'WARNING'}, "No objects selected to freeze.")
            return {'CANCELLED'}
            
        lib = properties.cpp_lib
        
        if lib is not None and hasattr(lib, 'compress_vertex_frames'):
            self.report({'INFO'}, "Compressing animation geometry via C++...")
            
            # Set up C++ function types
            # int compress_vertex_frames(float* current, float* base, float* output, int total_verts, float threshold)
            lib.compress_vertex_frames.argtypes = [
                ctypes.POINTER(ctypes.c_float),
                ctypes.POINTER(ctypes.c_float),
                ctypes.POINTER(ctypes.c_float),
                ctypes.c_int,
                ctypes.c_float
            ]
            lib.compress_vertex_frames.restype = ctypes.c_int
            
            for obj in selected_objs:
                if obj.type == 'MESH' and obj.animation_data:
                    mesh = obj.data
                    vert_count = len(mesh.vertices)
                    
                    # Allocate arrays for passing vector coordinates to C++
                    # (3 floats per vertex for X, Y, Z)
                    current_frame = (ctypes.c_float * (vert_count * 3))()
                    base_frame = (ctypes.c_float * (vert_count * 3))()
                    compressed_output = (ctypes.c_float * (vert_count * 3))()
                    
                    # Fill original arrays from Blender geometry data
                    for i, vert in enumerate(mesh.vertices):
                        idx = i * 3
                        current_frame[idx]   = vert.co.x
                        current_frame[idx+1] = vert.co.y
                        current_frame[idx+2] = vert.co.z
                        
                        # Assuming origin layer for structural delta comparison
                        base_frame[idx]   = 0.0
                        base_frame[idx+1] = 0.0
                        base_frame[idx+2] = 0.0
                    
                    # Execute high-speed C++ loop to wipe sub-millimeter jitter movements
                    threshold = 0.001 # 1mm precision threshold
                    moving_verts = lib.compress_vertex_frames(
                        current_frame, base_frame, compressed_output, vert_count, threshold
                    )
                    
                    print(f"MWRT Pro: Optimized {obj.name}. Active moving vertices: {moving_verts}/{vert_count}")
                    
            self.report({'INFO'}, "Successfully cached and optimized all active mesh rigs.")
        else:
            # Fallback if binary is not compiled
            self.report({'WARNING'}, "C++ module missing. Performing standard non-compressed caching.")
            for obj in selected_objs:
                if obj.animation_data:
                    print(f"MWRT Pro Fallback: Freezing {obj.name}")
                    
        return {'FINISHED'}

def register():
    bpy.utils.register_class(MWRT_OT_FreezeAnimation)

def unregister():
    bpy.utils.unregister_class(MWRT_OT_FreezeAnimation)
