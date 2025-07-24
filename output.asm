bits 16
%define x 0

jmp _main

f:
push bp
mov bp, sp
mov ax, [bp + 4]
inc ax
mov sp, bp
pop bp
ret

_0:
mov ax, x
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
push bp
mov bp, sp
mov bx, [bp + 6]
push bx
call [bp + 4]
mov sp, bp
pop bp
push ax
call [bp + 4]
mov sp, bp
pop bp
ret

_+:
push bp
mov bp, sp
push bp
mov bp, sp
mov bx, [bp + 10]
push bx
mov bx, [bp + 8]
push bx
call [bp + 6]
mov sp, bp
pop bp
push ax
mov bx, [bp + 8]
push bx
call [bp + 4]
mov sp, bp
pop bp
ret

_main:
push bp
mov bp, sp
mov bx, _2
push bx
mov bx, _1
push bx
call _+
mov sp, bp
pop bp
ret

times 510 - ($-$$) db 0
dw 0xAA55
