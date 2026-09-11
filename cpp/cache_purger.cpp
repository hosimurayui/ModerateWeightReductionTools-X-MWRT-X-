#include <iostream>
#include <cstring>

extern "C" {

    // Fast string pattern matching engine to scan for orphan cache blocks on local drives
    // Prevents large files (like .abc or .usd frames) from hogging drive space and bloating RAM
    int scan_and_flag_orphan_caches(const char** scene_object_names, int obj_count, const char** directory_file_names, int file_count, int* output_delete_flags) {
        int marked_for_deletion = 0;

        // Double-loop optimized via simple C-string compare routines
        for (int i = 0; i < file_count; ++i) {
            bool is_referenced = false;
            
            for (int j = 0; j < obj_count; ++j) {
                // If a file string contains any active object name from the active scene, keep it protected
                if (std::strstr(directory_file_names[i], scene_object_names[j]) != nullptr) {
                    is_referenced = true;
                    break;
                }
            }

            // If the cache file belongs to no existing asset in the scene, mark it for rapid deletion (Flag = 1)
            if (!is_referenced) {
                output_delete_flags[i] = 1;
                marked_for_deletion++;
            } else {
                output_delete_flags[i] = 0;
            }
        }

        // Returns total number of bloated cache files ready to be purged safely
        return marked_for_deletion;
    }
}
