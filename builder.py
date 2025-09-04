import os
import subprocess
import sys


def build_exe(script_path):
    if not os.path.exists(script_path):
        print(f"Error: File not found: {script_path}")
        return

    # Build command
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        script_path
    ]

    print(f"Running: {' '.join(cmd)}")

    try:
        subprocess.run(cmd, check=True)
        print("\n✅ Build complete! Look in the 'dist' folder.")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Build failed with error: {e}")


if __name__ == "__main__":
    # Change this to your main script
    pygame_script = "game.py"
    build_exe(pygame_script)