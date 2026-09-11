#include <iostream>
#include <cmath>

extern "C" {

    // Compresses vertex velocity data by removing unnoticeable tiny sub-millimeter movements
    // Helps reduce the final size of cached files on RAM/Disk during heavy MV animation sequences
    int compress_vertex_frames(const float* current_frame, const float* base_frame, float* compressed_output, int total_vertices, float threshold) {
        int optimized_count = 0;

        for (int i = 0; i < total_vertices; i++) {
            int idx = i * 3;
            
            // Calculate distance between current vertex position and base position
            float dx = current_frame[idx] - base_frame[idx];
            float dy = current_frame[idx + 1] - base_frame[idx + 1];
            float dz = current_frame[idx + 2] - base_frame[idx + 2];
            float delta = std::sqrt(dx*dx + dy*dy + dz*dz);

            // If the vertex movement is smaller than the threshold, clamp it to zero (Compress)
            if (delta < threshold) {
                compressed_output[idx]     = 0.0f;
                compressed_output[idx + 1] = 0.0f;
                compressed_output[idx + 2] = 0.0f;
            } else {
                compressed_output[idx]     = dx;
                compressed_output[idx + 1] = dy;
                compressed_output[idx + 2] = dz;
                optimized_count++;
            }
        }
        
        // Returns how many vertices actually had significant movement
        return optimized_count;
    }
}
