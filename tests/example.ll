;
; LL
;

def 1 (f, x) -> (f(x))
def 2 (f, x) -> (f(f(x)))

def + (m, n, f, x) -> (m(f, n(f, x)))

def main (f, x) -> (+(1, 2))