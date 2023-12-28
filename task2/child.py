import os
import sys
import random
import time

def main():
    seconds = int(sys.argv[1])
    pid = os.getpid()
    ppid = os.getppid()
    print(f"Child[{pid}]: I am started. My PID {pid}. Parent PID {ppid}.")
    time.sleep(seconds)
    if random.choice([True, False]):
        status = 0
    else:
        status = 1
    print(f"Child[{pid}]: I am ended. PID {pid}. Parent PID {ppid}.")
    sys.exit(status)

if __name__ == "__main__":
    main()
