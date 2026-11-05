import platform, os, shutil
def run():
    print("OS:", platform.platform())
    print("Python:", platform.python_version())
    print("Architecture:", platform.machine())
    print("CPU cores:", os.cpu_count())
    print("Disk usage:", shutil.disk_usage("."))
