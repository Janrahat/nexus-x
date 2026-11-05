import platform, os
def run():
    print('Device:',platform.node())
    print('System:',platform.system(),platform.release())
    print('Machine:',platform.machine())
    print('Python:',platform.python_version())
    print('CPU count:',os.cpu_count())
