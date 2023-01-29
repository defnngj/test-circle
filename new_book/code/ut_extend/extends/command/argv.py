# run.py
import sys


run_file = sys.argv[0]
print(f"run file -> {run_file}")

args = sys.argv[1:]

for a in args:
    print(f"hello, {a}")
