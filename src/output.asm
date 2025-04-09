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
1:
push bp
mov bp, sp
mov bx, [bp + 4]mov bx, [bp + 6]2:
push bp
mov bp, sp
mov bx, [bp + 4]mov bx, [bp + 6]+:
push bp
mov bp, sp
mov bx, [bp + 4]mov bx, [bp + 6]mov bx, [bp + 8]mov bx, [bp + 10]main:
push bp
mov bp, sp
mov bx, [bp + 4]mov bx, [bp + 6]