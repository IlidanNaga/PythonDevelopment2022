import venv
from tempfile import mkdtemp
from shutil import rmtree
import sys
import subprocess


def main():

    install_cmd = "/bin/pip install pyfiglet"
    launch_cmd = "/bin/python3"

    temp_dir = mkdtemp()
    venv_dir = temp_dir + "/env"
    venv.create(venv_dir, with_pip=True)

    install_cmd = venv_dir + install_cmd
    launch_cmd = venv_dir + launch_cmd

    launch_cmd = [launch_cmd, "-m", "figdate"]

    if sys.argv.__len__() > 1:
        launch_cmd += sys.argv[1:]

    subprocess.run(install_cmd.split(" "),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
                )
    subprocess.run(launch_cmd)

    rmtree(temp_dir)

if __name__ == '__main__':
    main()