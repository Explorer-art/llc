;
; LL
;

def test (y) -> (y)

def main(f, x) -> (test(test))


;
; NASM
;

test:
	mov ax, [sp + 2]
	ret

main:
	push test
	call test
	ret