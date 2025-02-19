# Gallery Purge 🧹📸

A Python tool to quickly review and decide whether to keep or delete images and videos in a folder and its subdirectories. Deleted files are moved to a "Deleted" folder, keeping the folder structure intact.

## Features ✨

- **Review Media**: Supports images (PNG, JPG, JPEG, GIF, BMP, HEIC) and videos (MP4, AVI, MOV).
- **Recursive Search**: Finds all supported files in the directory and subdirectories.
- **Live Preview**: View images and videos in real-time.

## Installation ⚙️

Make sure Python 3.6+ is installed and install the dependencies: `pip install pillow opencv-python pillow-heif`


## How to Use 🚀

1. **Input Directory**: Enter the folder path containing your media files.
2. **Review Files**: Click "Begin" to start reviewing files one by one.
3. **Delete or Keep**:
   - Click "Delete" to move the file to the "Deleted" folder.
   - Click "Keep" to skip the file.
