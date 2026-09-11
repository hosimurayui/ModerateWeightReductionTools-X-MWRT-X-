#include <iostream>
#include <cmath>

extern "C" {

    // Structure for an Object's Axis-Aligned Bounding Box (AABB)
    struct BoundingBox {
        float min_x, min_y, min_z;
        float max_x, max_y, max_z;
    };

    // Structure for a Camera Plane (Ax + By + Cz + D = 0)
    struct Plane {
        float a, b, c, d;
    };

    // Fast Frustum Culling computation
    // Returns 1 if the object is inside/intersecting the camera view, 0 if it is completely outside (Cull it)
    int is_object_in_frustum(BoundingBox box, const Plane* frustum_planes, int plane_count) {
        for (int i = 0; i < plane_count; ++i) {
            Plane p = frustum_planes[i];

            // Find the positive vertex (farthest along the plane normal)
            float px = (p.a > 0.0f) ? box.max_x : box.min_x;
            float py = (p.b > 0.0f) ? box.max_y : box.min_y;
            float pz = (p.c > 0.0f) ? box.max_z : box.min_z;

            // If the positive vertex is outside the plane, the box is completely outside the frustum
            if ((p.a * px + p.b * py + p.c * pz + p.d) < 0.0f) {
                return 0; // Culleable (Outside the view)
            }
        }
        return 1; // Visible (Inside or clipping the view)
    }
}
