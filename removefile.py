import os
import sys
import time


time.sleep(15)
local_file_path = sys.argv[1]
os.remove(local_file_path)
