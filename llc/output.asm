bits 16

%define x 0

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
mov bx, _2
push bx
mov bx, _1
push bx
call _add
mov sp, bp
pop bp
ret

jmp _main