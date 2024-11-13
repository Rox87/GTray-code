import sys

def fatorial(n):
    if n == 0 or n == 1:
        return 1
    return n * fatorial(n - 1)

n = int(sys.argv[1])
print(fatorial(n))
