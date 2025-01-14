def fabonacci(n):
    if n in [0,1,2]:
        return 1
    else:
        return (fabonacci(n-1) +
                fabonacci(n-2) *
                fabonacci(n-3))
