;
; LL
;

def 0 (f, x) -> (x)
def 1 (f, x) -> (f(x))
def 2 (f, x) -> (f(f(x)))

def sum (m, n) -> (m(f, n(f, x)))
def main () -> (sum(1, 2))