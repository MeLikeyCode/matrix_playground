import shutil
import subprocess
import argparse
import os


description = """Package everything in an installer."""

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=description)
    args = parser.parse_args()

    # get directory the script is in
    script_dir = os.path.dirname(os.path.realpath(__file__))

    os.chdir(script_dir)

    # run pyinstaller, will create folder dist/pomodoro
    subprocess.run(
        [
            "pyinstaller",
            "--noconfirm",
            "--name=matrix_playground",
            "main.py"
        ],
        check=True,
    )

    # create installer
    subprocess.run('makensis build_installer.nsi', shell=True, check=True)

    # copy commandinterpretter.py to dist/matrix_playground
    shutil.copy("commandinterpretter.py", "dist/matrix_playground")