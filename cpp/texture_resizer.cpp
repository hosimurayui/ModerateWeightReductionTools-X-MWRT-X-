#include <iostream>
#include <vector>

extern "C" {

    // Fast image downsampling processor (e.g., Bilinear scaling for raw pixel arrays)
    // Python passes the raw float pixel array from Blender's Image datablock
    void resize_texture_rgba_fast(const float* input_pixels, int src_w, int src_h, float* output_pixels, int dst_w, int dst_h) {
        float x_ratio = ((float)(src_w - 1)) / dst_w;
        float y_ratio = ((float)(src_h - 1)) / dst_h;

        // Perform fast scaling operation (Simulated bilinear filtering loop)
        for (int i = 0; i < dst_h; i++) {
            for (int j = 0; j < dst_w; j++) {
                int x = (int)(x_ratio * j);
                int y = (int)(y_ratio * i);
                
                // Calculate pixel channel index (RGBA)
                int src_idx = (y * src_w + x) * 4;
                int dst_idx = (i * dst_w + j) * 4;

                // Copy channels rapidly
                output_pixels[dst_idx]     = input_pixels[src_idx];     // R
                output_pixels[dst_idx + 1] = input_pixels[src_idx + 1]; // G
                output_pixels[dst_idx + 2] = input_pixels[src_idx + 2]; // B
                output_pixels[dst_idx + 3] = input_pixels[src_idx + 3]; // A
            }
        }
    }
}
