#include <iostream>
#include <vector>
#include <cmath>

extern "C" {

    // Simple flat normal checker for planar simplification
    // Scans face normals to flags vertices that can be safely merged without changing the visual model edge silhouettes
    void identify_planar_vertices(const float* face_normals, const int* face_indices, int face_count, int* vert_dissolve_flags, float angle_threshold_radians) {
        
        // Loop through all adjacent faces to check normal variance
        for (int i = 0; i < face_count - 1; i++) {
            int idx1 = i * 3;
            float n1_x = face_normals[idx1];
            float n1_y = face_normals[idx1 + 1];
            float n1_z = face_normals[idx1 + 2];

            int idx2 = (i + 1) * 3;
            float n2_x = face_normals[idx2];
            float n2_y = face_normals[idx2 + 1];
            float n2_z = face_normals[idx2 + 2];

            // Dot product to find the angle between two polygon face normals
            float dot_product = (n1_x * n2_x) + (n1_y * n2_y) + (n1_z * n2_z);
            
            // Clamp value to prevent NaN issues in acos
            if (dot_product > 1.0f) dot_product = 1.0f;
            if (dot_product < -1.0f) dot_product = -1.0f;

            float angle = std::acos(dot_product);

            // If the angle difference is within the flat threshold, flag the shared face vertices for dissolution
            if (angle < angle_threshold_radians) {
                // Mark the index mapping slots as mergeable (1 = true)
                vert_dissolve_flags[face_indices[i * 3]] = 1;
                vert_dissolve_flags[face_indices[i * 3 + 1]] = 1;
                vert_dissolve_flags[face_indices[i * 3 + 2]] = 1;
            }
        }
    }
}
