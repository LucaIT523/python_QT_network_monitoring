import os
import sys
def resource_path(relative_path):
    if getattr(sys, 'frozen', False):  # Running as an executable
        base_path = sys._MEIPASS
    else:  # Running as a script
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path).replace("\\", "/")
def get_base_dir(dir_name):
    srcBaseDirectory = os.path.join(os.getcwd(), dir_name)
    if not os.path.exists(srcBaseDirectory):
        os.makedirs(srcBaseDirectory)
    return srcBaseDirectory