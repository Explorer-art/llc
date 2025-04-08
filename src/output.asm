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
2:
+:
main:
