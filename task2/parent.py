import os
import sys
import random
import time
import signal

def main():
    try:
        num_children = int(sys.argv[1])
    except ValueError:
        print("N must be an integer")
        sys.exit(1)

    for _ in range(num_children):
        child_pid = os.fork()
        if child_pid == 0:
            os.execve("./child", ["child", str(random.randint(5, 10))], {})
            sys.exit(0)
        else:
            print(f"Parent[{os.getpid()}]: I ran children process with PID {child_pid}.")

    while True:
        try:
            pid, status = os.wait()
            if os.WIFEXITED(status):
                exit_status = os.WEXITSTATUS(status)
                if exit_status != 0:
                    print(f"Parent[{os.getpid()}]: Child with PID {pid} terminated. Exit Status {exit_status}.")
                    new_child_pid = os.fork()
                    if new_child_pid == 0:
                        os.execve("./child", ["child", str(random.randint(5, 10))], {})
                        sys.exit(0)
                    else:
                        print(f"Parent[{os.getpid()}]: I ran children process with PID {new_child_pid}.")
            elif os.WIFSIGNALED(status):
                print(f"Parent[{os.getpid()}]: Child with PID {pid} terminated by signal {os.WTERMSIG(status)}.")
        except OSError:
            break

if __name__ == "__main__":
    main()
