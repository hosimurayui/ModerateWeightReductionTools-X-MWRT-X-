#include <iostream>
#include <vector>
#include <algorithm>

extern "C" {

    // Structure representing a single texture rect to be packed into the atlas
    struct TextureRect {
        int id;
        int width;
        int height;
        int x; // Output result computed by C++
        int y; // Output result computed by C++
        bool is_packed;
    };

    // Helper to sort textures by area (descending) for efficient packing algorithm
    bool compare_rect_area(const TextureRect& a, const TextureRect& b) {
        return (a.width * a.height) > (b.width * b.height);
    }

    // Fast Texture Atlas Packing calculation
    // Computes layout positions (X, Y) for multiple images to fit perfectly in a combined atlas texture
    void pack_textures_fast(TextureRect* rects, int count, int atlas_width, int atlas_height) {
        // Sort input rects to apply the standard "Greedy Shelf/MaxRects" approximation logic
        std::vector<TextureRect> rect_list(rects, rects + count);
        std::sort(rect_list.begin(), rect_list.end(), compare_rect_area);

        int current_x = 0;
        int current_y = 0;
        int max_row_height = 0;

        for (int i = 0; i < count; i++) {
            // Check if it fits horizontally on the current shelf row
            if (current_x + rect_list[i].width > atlas_width) {
                current_x = 0;
                current_y += max_row_height;
                max_row_height = 0;
            }

            // Check if it exceeds the maximum atlas boundary vertically
            if (current_y + rect_list[i].height > atlas_height) {
                rect_list[i].is_packed = false;
                continue;
            }

            // Assign successfully packed coordinates
            rect_list[i].x = current_x;
            rect_list[i].y = current_y;
            rect_list[i].is_packed = true;

            current_x += rect_list[i].width;
            if (rect_list[i].height > max_row_height) {
                max_row_height = rect_list[i].height;
            }
        }

        // Copy computed layout results back to the original array pointer for Python to read
        for (int i = 0; i < count; i++) {
            for (int j = 0; j < count; j++) {
                if (rects[i].id == rect_list[j].id) {
                    rects[i].x = rect_list[j].x;
                    rects[i].y = rect_list[j].y;
                    rects[i].is_packed = rect_list[j].is_packed;
                    break;
                }
            }
        }
    }
}
