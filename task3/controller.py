import os
import signal
import sys

def main():
    pipe1_0_read, pipe1_0_write = os.pipe()
    pipe0_2_read, pipe0_2_write = os.pipe()
    pipe2_0_read, pipe2_0_write = os.pipe()

    pid1 = os.fork()
    if pid1 == 0:
        os.close(pipe1_0_read)
        os.dup2(pipe1_0_write, sys.stdout.fileno())
        os.execve("./producer", ["producer"], {})
        sys.exit(0)

    pid2 = os.fork()
    if pid2 == 0:
        os.close(pipe1_0_write)
        os.close(pipe0_2_read)
        os.close(pipe2_0_write)
        os.dup2(pipe0_2_write, sys.stdout.fileno())
        os.dup2(pipe2_0_read, sys.stdin.fileno())
        os.execve("/usr/bin/bc", ["bc"], {})
        sys.exit(0)

    os.close(pipe1_0_write)
    os.close(pipe0_2_write)
    os.close(pipe2_0_read)

    def sigusr1_handler(signum, frame):
        print(f"Produced: {produced}")

    signal.signal(signal.SIGUSR1, sigusr1_handler)

    produced = 0
    while True:
        try:
            expr = os.read(pipe1_0_read, 100).decode("utf-8")
            if not expr:
                break
            produced += 1
            os.write(pipe0_2_write, expr.encode("utf-8"))
            result = os.read(pipe2_0_read, 100).decode("utf-8")
            print(f"{expr.strip()} = {result.strip()}")
        except OSError:
            break

if __name__ == "__main__":
    main()
