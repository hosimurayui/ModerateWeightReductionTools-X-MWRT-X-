#include <iostream>
#include <vector>

extern "C" {

    // Structure to hold mesh analysis results
    struct MeshMetric {
        int vertex_count;
        int polygon_count;
        float memory_size_kb;
    };

    // Fast calculation of mesh density and weight
    // Python passes raw arrays of vertex and polygon counts
    MeshMetric analyze_mesh_density(int vertex_count, int polygon_count) {
        MeshMetric metric;
        metric.vertex_count = vertex_count;
        metric.polygon_count = polygon_count;
        
        // Calculate estimated raw data footprint in memory (assuming standard float weights)
        // Vertices (3 floats each) + Normals (3 floats each)
        float vert_memory = (float)vertex_count * 3 * sizeof(float) * 2;
        // Polygons (assumed average 4 indices)
        float poly_memory = (float)polygon_count * 4 * sizeof(int);
        
        metric.memory_size_kb = (vert_memory + poly_memory) / 1024.0f;
        
        return metric;
    }
}
