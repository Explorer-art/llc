;
; LL
;

def 0 (f, x) -> (x)
def 1 (f, x) -> (f(x))
def 2 (f, x) -> (f(f(x)))

def main (f, x) -> (f(1))