ASM=nasm
FLOPPY_IMAGE=floppy.img

.PHONY: all clean

all:
	python3 llc/llc.py examples/example.ll -o boot.asm
	$(ASM) -f bin boot.asm -o boot.bin
	dd if=/dev/zero of=$(FLOPPY_IMAGE) bs=512 count=2880
	mkfs.fat -F 12 -n "NBOS" $(FLOPPY_IMAGE)
	dd if=boot.bin of=$(FLOPPY_IMAGE) conv=notrunc

clean:
	rm -f floppy.img
