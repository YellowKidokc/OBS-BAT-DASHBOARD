"""Create Windows directory junction for 00_MEDIA"""
import os, sys

link = r'O:\_Theophysics_v3\00_MEDIA'
target = r'O:\00_MEDIA'

if os.path.exists(link):
    print(f"Already exists: {link}")
    if os.path.islink(link):
        print(f"  -> is symlink/junction pointing to: {os.readlink(link)}")
    else:
        print("  -> is a regular directory (not a junction)")
    sys.exit(0)

# Create junction using os.symlink with target_is_directory
try:
    os.symlink(target, link, target_is_directory=True)
    print(f"Created junction: {link} -> {target}")
    # Verify
    if os.path.isdir(link):
        print(f"Verified: {link} is accessible")
        contents = os.listdir(link)
        print(f"Contents ({len(contents)} items): {contents[:5]}")
    else:
        print("WARNING: Junction created but not accessible as directory")
except Exception as e:
    print(f"Error: {e}")
