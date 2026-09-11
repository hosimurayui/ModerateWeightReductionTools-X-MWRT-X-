#include <iostream>

#ifdef _WIN32
#include <windows.h>
#endif

// Export function as standard C interface for Python's ctypes
extern "C" {

    // 1. Get system RAM usage percentage (0.0 to 100.0)
    float get_system_ram_usage() {
#ifdef _WIN32
        MEMORYSTATUSEX memInfo;
        memInfo.dwLength = sizeof(MEMORYSTATUSEX);
        if (GlobalMemoryStatusEx(&memInfo)) {
            return (float)memInfo.dwMemoryLoad;
        }
#endif
        return 0.0f; // Return 0 if not on Windows or failed
    }

    // 2. Get available VRAM in Megabytes (Placeholder for GPU API integration)
    // In production, this can be linked with NVIDIA NVML or DirectX/Vulkan queries
    int get_available_vram_mb() {
        int mock_available_vram = 4096; // temporary mock value: 4GB
        // TODO: Integrate actual DXGI/NVML query logic here for precise metrics
        return mock_available_vram;
    }
}
