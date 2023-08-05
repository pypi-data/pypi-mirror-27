import os
import stat
import errno

def on_same_file_system(file1, file2):
    "Return True if file1 and file2 are on the samde file system and False otherwise"
    dev1 = os.stat(file1).st_dev
    dev2 = os.stat(file2).st_dev
    return dev1 == dev2


def make_user_executable(path):
    "Emulate chmod u+x; Make a file or directory at path executable by the user"
    #https://stackoverflow.com/questions/12791997/how-do-you-do-a-simple-chmod-x-from-within-python
    st = os.stat(path)
    os.chmod(path, st.st_mode | stat.S_IEXEC)

def indent(lines, n=1):
    "Indent a list of lines with 4 spaces per indent level n (default n=1)"
    return ["    "*n + line for line in lines]

def mkdir_p(dirname):
    "Emulate mkdir -p; create a new directory including any intermediate directories"
    os.makedirs(dirname, exist_ok=True)


def link_force(target, link_name):
    "Emulate ln -f; create a hard link from link_name to target, replacing any existing file"
    # from https://stackoverflow.com/questions/8299386/modifying-a-symlink-in-python
    try:
        os.link(target, link_name)
    except OSError as e:
        if e.errno == errno.EEXIST:
            os.remove(link_name)
            os.link(target, link_name)
        else:
            raise e
