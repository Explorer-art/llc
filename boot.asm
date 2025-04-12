bits 16
org 0x7C00

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
push bp
mov bp, sp
mov ax, [bp + 6]
mov sp, bp
pop bp
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

_3:
push bp
mov bp, sp
mov bx, [bp + 6]
push bx
call [bp + 4]
push ax
call [bp + 4]
push ax
call [bp + 4]
mov sp, bp
pop bp
ret

_4:
push bp
mov bp, sp
mov bx, [bp + 6]
push bx
call [bp + 4]
push ax
call [bp + 4]
push ax
call [bp + 4]
push ax
call [bp + 4]
mov sp, bp
pop bp
ret

_5:
push bp
mov bp, sp
mov bx, [bp + 6]
push bx
call [bp + 4]
push ax
call [bp + 4]
push ax
call [bp + 4]
push ax
call [bp + 4]
push ax
call [bp + 4]
mov sp, bp
pop bp
ret

_add:
push bp
mov bp, sp
mov bx, x
push bx
mov bx, f
push bx
call [bp + 6]
push ax
mov bx, f
push bx
call [bp + 4]
mov sp, bp
pop bp
ret

_main:
push bp
mov bp, sp
mov bx, _5
push bx
mov bx, _0
push bx
call _add
mov sp, bp
pop bp
cli
hlt

times 510 - ($-$$) db 0
dw 0xAA55