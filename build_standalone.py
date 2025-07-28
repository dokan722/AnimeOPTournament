import os
import subprocess
import shutil

APP_NAME = "AnimeTournament"
MAIN_SCRIPT = "main.py"
DATA_DIR = "data_collection/data"
BUILD_DIR = "build"
DIST_DIR = "standalone"


def build_executable():
    cmd = [
        "pyinstaller",
        "--name", APP_NAME,
        "--onefile",
        "--distpath", DIST_DIR,
        "--workpath", BUILD_DIR,
        "--add-data", f"{DATA_DIR}{os.pathsep}data_collection/data",
        "--clean",
        MAIN_SCRIPT
    ]
    subprocess.run(cmd, check=True)


def main():
    for path in [BUILD_DIR, DIST_DIR, "AnimeTournament.spec"]:
        if os.path.exists(path):
            if os.path.isdir(path):
                shutil.rmtree(path)
            else:
                os.remove(path)
    build_executable()
    print(f"\nStandalone built in {DIST_DIR}/ directory!")


if __name__ == "__main__":
    main()