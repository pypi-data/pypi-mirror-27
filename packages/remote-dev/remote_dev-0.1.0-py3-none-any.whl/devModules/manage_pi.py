"""
Functions to manage you raspberry pi(Inspiration from django manage.py)
"""
import argparse

from devModules.filesystem import *
from devModules.piCommunication import *
from devModules.piDev import PiDev
import sys


settings = yaml_file_to_dict("settings.yaml")
pidev = PiDev(settings)
comm = PiCommunication(settings["username"], settings["pi_address"])

def start():
    """
    Starts a session.
    Does the following things:
        1) deletes the project dir in the pi
        2) copies all the project files to the pi
        3) Creates a file to keep track of which files where copied and when they were last modified
    :param username:
    :param pi_address:
    :param project_dir:
    :return:
    """
    pidev.delete_project()
    pidev.create_project()
    # Scp the files
    pidev.create_venv()
    pidev.install_dependencies()
    pidev.scp_project()
    pidev.update_session()
    pidev.run_extra_commands()


def test():
    pidev.runt_tests()


def run():
    """
    Runs a given command on the raspberry in the project root
    :param args:
    :param settings:
    :return:
    """
    global pidev
    global comm
    pidev.upload_changes()
    pidev.run_command(sys.argv[1])


def delete_project():
    """
    Deletes the project on the pi
    :param args:
    :param settings:
    :return:
    """
    global comm
    global pidev
    pidev.delete_project()




