#include <iostream>
#include <cmath>

extern "C" {

    // Rapidly transfers face normals from high-poly proxy data to low-poly split vertex normals
    // It maps based on closest proximity coordinates passed from Python
    void transfer_custom_normals(
        const float* low_poly_verts, int low_poly_count,
        const float* high_poly_normals, const float* high_poly_verts, int high_poly_count,
        float* output_low_poly_normals) {

        for (int i = 0; i < low_poly_count; ++i) {
            int l_idx = i * 3;
            float lx = low_poly_verts[l_idx];
            float ly = low_poly_verts[l_idx + 1];
            float lz = low_poly_verts[l_idx + 2];

            int closest_hp_idx = 0;
            float min_distance_sq = 1e10f; // Initialize with a very large distance

            // Fast brute-force proximity scan (Can be upgraded to BVH tree in production)
            for (int j = 0; j < high_poly_count; ++j) {
                int h_idx = j * 3;
                float hx = high_poly_verts[h_idx];
                float hy = high_poly_verts[h_idx + 1];
                float hz = high_poly_verts[h_idx + 2];

                float dx = lx - hx;
                float dy = ly - hy;
                float dz = lz - hz;
                float dist_sq = dx*dx + dy*dy + dz*dz;

                if (dist_sq < min_distance_sq) {
                    min_distance_sq = dist_sq;
                    closest_hp_idx = j;
                }
            }

            // Inject the closest high-poly normal vector into the low-poly output normal array
            int target_hp_normal_idx = closest_hp_idx * 3;
            output_low_poly_normals[l_idx]     = high_poly_normals[target_hp_normal_idx];
            output_low_poly_normals[l_idx + 1] = high_poly_normals[target_hp_normal_idx + 1];
            output_low_poly_normals[l_idx + 2] = high_poly_normals[target_hp_normal_idx + 2];
        }
    }
}
