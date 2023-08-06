import os

def packagify(rootdir):
    '''

    A simple function which checks if the provided directory is a python package or if there exists a python package in it.
    
    '''
    for subdir, dirs, files in os.walk(rootdir):
        for f in files:
            if f=='__init__.py':
                return True
    return False



if __name__=="__main__":
    print(packagify(os.getcwd()))