import os
import subprocess

def compress_directory(source_dir, output_file):
    if not os.path.isdir(source_dir):
        print("Invalid source directory for compression.")
        return False
    try:
        # Use the '-C' option to change to the source directory before compressing
        subprocess.run(["tar", "-czvf", output_file, "-C", os.path.dirname(source_dir), os.path.basename(source_dir)])
        print(f"Directory {source_dir} compressed to {output_file}")
        return True
    except Exception as e:
        print(f"Error during compression: {e}")
        return False

def decompress_directory(compressed_file, output_dir):
    if not os.path.exists(compressed_file):
        print("Invalid compressed file for decompression.")
        return False
    try:
        # Use the '-C' option to change to the output directory before decompressing
        subprocess.run(["tar", "-xzvf", compressed_file, "-C", output_dir, "--strip-components=1", "--one-top-level"])
        compressed_filename = os.path.basename(compressed_file)
        if compressed_filename.endswith('.tar'):
            compressed_filename = compressed_filename[:-4]  # Remove .tar extension
        elif compressed_filename.endswith('.gz'):
            compressed_filename = compressed_filename[:-3]  # Remove .gz extension
        print(f"File {compressed_file} decompressed to {output_dir}/{compressed_filename}")
        return True
    except Exception as e:
        print(f"Error during decompression: {e}")
        return False
