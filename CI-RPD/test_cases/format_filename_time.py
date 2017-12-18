import datetime
import os

def get_datetime_path(projectname, unique_id):
    date_now = datetime.datetime.now().strftime("%m-%d-%y_%H-%M-%S")
    if projectname == "obidev":
        screenshot_path = '/var/lib/jenkins/workspace/obidev/CI-RPD/screenshots/'
    elif projectname == "obidev-intern-josh":
        screenshot_path = '/var/lib/jenkins/workspace/obidev-intern-josh/CI-RPD/screenshots/'
    elif projectname == "obidev-intern-max":
        screenshot_path = '/var/lib/jenkins/workspace/obidev-intern-max/CI-RPD/screenshots/'
    elif projectname == "obiprod":
        screenshot_path = '/var/lib/jenkins/workspace/obiprod/CI-RPD/screenshots/'

    cleanup(screenshot_path)

    full_screenshot_path = screenshot_path + 'screenshot_'+ date_now + '_' + unique_id +'.png'

    return full_screenshot_path

def cleanup(folderpath):
    #Get our dirpaths, dirnames, and filenames
    for dirpath, dirnames, filenames in os.walk(folderpath):
        for file in filenames:
            curpath = os.path.join(dirpath, file)
            file_modified = datetime.datetime.fromtimestamp(os.path.getmtime(curpath))
            if datetime.datetime.now() - file_modified > datetime.timedelta(days=7):
                os.remove(curpath)