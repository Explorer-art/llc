from ast import *

# Внутренние функции (Internal Library)
INTLIB = """%define x 0

call _main
cli
hlt

f:
push bp
mov bp, sp
mov ax, [bp + 4]
inc ax
mov sp, bp
pop bp
ret

"""

INTLIB_FUNC_NAMES = ["f", "x"]

# Стандартное смещение в стеке
# (с учетом того, что перед вызовом функции мы сохраняем в стек регистр BP и адрес возврата)
DEFAULT_STACK_ARGS_OFFSET = 4

class LL16_Generator:
	def __init__(self, program: Program):
		self.program = program
		self.code = ""

	def get_func_by_name(self, func_name):
		""""Получение функции по названию"""
		for func in self.program.functions:
			if func.name == func_name:
				return func

	def generate(self) -> str:
		"""Главная функция генерации ассемблерного кода"""
		self.code += "bits 16\n"
		self.code += "org 0x7C00\n"
		self.code += INTLIB

		# Генерируем код функций
		for func in self.program.functions:
			self.generate_func(func)

		# Заполняем все оставшееся байты нулями
		self.code += "times 510 - ($-$$) db 0\n"
		
		# Сигнатура для MBR
		self.code += "dw 0xAA55\n"

		return self.code

	def generate_func(self, func: Func):
		self.code += f"_{func.name}:\n"
		self.code += "push bp\n"
		self.code += "mov bp, sp\n"

		if isinstance(func.body, CallFunc):
			self.generate_call_func(func.body, func.params)
		elif isinstance(func.body, FuncPtr):
			self.code += f"mov ax, {str(func.body)}\n"

		self.code += "mov sp, bp\n"
		self.code += "pop bp\n"
		self.code += "ret\n\n"

	def generate_call_func(self, func: CallFunc, original_params, r_flag = False):
		for arg in func.args[::-1]:
			if str(arg) in original_params:
				if isinstance(arg, CallFunc):
					self.generate_call_func(arg, original_params, True)
					self.code += "push ax\n"
				elif isinstance(arg, FuncPtr):
					arg_index = original_params.index(str(arg))
					offset = DEFAULT_STACK_ARGS_OFFSET + (arg_index * 2)
					self.code += f"mov bx, [bp + {offset}]\n"
					self.code += "push bx\n"
			else:
				if isinstance(arg, CallFunc):
					self.generate_call_func(arg, original_params, True)
					self.code += "push ax\n"
				elif isinstance(arg, FuncPtr):
					if str(arg) in INTLIB_FUNC_NAMES:
						self.code += f"mov bx, {str(arg)}\n"
					else:
						self.code += f"mov bx, _{str(arg)}\n"

					self.code += "push bx\n"

		if func.name in original_params:
			arg_index = original_params.index(func.name)
			offset = DEFAULT_STACK_ARGS_OFFSET + (arg_index * 2)
			self.code += f"call [bp + {offset}]\n"
		else:
			if func.name in INTLIB_FUNC_NAMES:
				self.code += f"call {func.name}\n"
			else:
				self.code += f"call _{func.name}\n"