;
; LL
;

def 1 (f, x) -> (f(x))
def 2 (f, x) -> (f(f(x)))

def + (m, n, f, x) -> (m(f, n(f, x)))

def main (f, x) -> (+(1, 2))


;
; NASM
;

bits 16

f:
    push bp
    
    mov bp, sp
    
    mov ax, [bp + 4]
    inc ax
    
    mov sp, bp
    
    pop bp
    ret

x:
    ret

_1:
    push bp
    
    mov bp, sp
    
    mov bx, [bp + 6]
    push bx
    call [bp + 4]
    
    mov sp, bp
    
    pop bp
    ret

_2:
    push bp
    
    mov bp, sp
    
    mov bx, [bp + 6]
    push bx
    call [bp + 4]
    
    push ax
    call [bp + 4]
    
    mov sp, bp
    
    pop bp
    ret

_+:
    push bp
    
    mov bp, sp
    
    mov bx, [bp + 8]
    push bx
    mov bx, [bp + 10]
    push bx
    call [bp + 6]
    
    mov bx, [bp + 6]
    push bx
    mov bx, ax
    push ax
    call [bp + 4]
    
    mov sp, bp
    
    pop bp
    ret