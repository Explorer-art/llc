import sys

# Стандартный шаблон кода на ассемблере
assembly ="""bits 16
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

"""

ENTRY_POINT = "main"

# Внешние функции
EXTERNAL_FUNCTIONS_IDS = ["f", "x"]

# Стандартное смещение в стеке
# (с учетом того, что перед вызовом функции мы сохраняем в стек регистр BP)
DEFAULT_STACK_ARGS_OFFSET = 2

def get_internal_function(ast, func_input, func_output):
	buffer = ""
	func_id = ""
	function = None
	count_parents = 0

	for i, char in enumerate(func_output):
		if char == "(":
			count_parents += 1

			# Удаляем другие аргументы функции
			substring = buffer[:i]
			left_arg_index = substring.rfind(",")
			buffer = buffer[left_arg_index + 1:]

			func_id = buffer
			buffer = ""
		elif char == ")":
			count_parents -= 1

			# Проверка существования функции
			if func_input and not func_id in func_input and not func_id in ast:
				print(f"Error: function '{func_id}' undefined")
				sys.exit()

			if not func_input and not func_id in ast:
				print(f"Error: function '{func_id}' undefined")
				sys.exit()

			# Получаем аргументы функции
			_func_input = buffer.split(",")

			function = {
				"id": func_id,
				"input": _func_input
			}

			# Удаляем вызов функции из output
			substring = func_output[:i]
			left_index = substring.rfind("(")

			if left_index == -1:
				print("Error: left parent not found")
				sys.exit()

			substring = func_output[:left_index]

			left_arg_index = substring.rfind(",")
			left_func_index = substring.rfind("(")

			if left_arg_index > left_func_index:
				left_index = left_arg_index
			else:
				left_index = left_func_index

			func_output = func_output[:left_index + 1] + "ax" + func_output[i + 1:]

			break
		else:
			buffer += char

	return function, func_output

def unfold_calls(ast, func_id, func_output, original_input):
	global assembly

	function, _func_output = get_internal_function(ast, original_input, func_output)

	print(f"DEBUG: {func_id}:", function, _func_output)

	if function:
		for arg in function["input"][::-1]:
			# Проверяем есть ли значение в аргументах функции, иначе ассоциируем
			# его с функцией объявленной с помощью def
			if arg in original_input:
				arg_index = original_input.index(arg)
				arg_offset = 2 + arg_index * len(original_input)

				assembly += f"mov bx, [bp + {DEFAULT_STACK_ARGS_OFFSET + arg_offset}]\n"
				assembly += "push bx\n"
			elif arg in ast:
				if arg in EXTERNAL_FUNCTIONS_IDS:
					assembly += f"mov bx, {arg}\n"
					assembly += "push bx\n"
				else:
					assembly += f"mov bx, _{arg}\n"
					assembly += "push bx\n"
			elif arg == "ax":
				assembly += "push ax\n"
			else:
				print(f"Compile error: {arg} undefined")
				sys.exit()

		if function["id"] in original_input:
			arg_index = original_input.index(function["id"])
			arg_offset = 2 + arg_index * len(original_input)

			assembly += f"call [bp + {DEFAULT_STACK_ARGS_OFFSET + arg_offset}]\n"
		else:
			if function["id"] in EXTERNAL_FUNCTIONS_IDS:
				assembly += f"call {function["id"]}\n"
			else:
				assembly += f"call _{function["id"]}\n"

		if _func_output == "ax":
			assembly += "mov sp, bp\n"
			assembly += "pop bp\n"

			# Если это главная функция (точка входа) то после выполнения программы
			# отключаем прерывания и останавливаем процессор
			if func_id == ENTRY_POINT:
				assembly += "cli\n"
				assembly += "hlt\n\n"
			else:
				assembly += "ret\n\n"

			return

	if not "(" in func_output or not ")" in func_output:
		assembly += "ret\n\n"
		return

	unfold_calls(ast, func_id, _func_output, original_input)

def generate_assembly(ast):
	global assembly

	# Генерируем код каждой функции
	for func_id in ast:
		# Если это внешняя функция, то пропускаем её, так как её код изначально есть в программе
		if func_id in EXTERNAL_FUNCTIONS_IDS:
			continue

		# Знак нижнего подчеркивания добавляет что бы избежать ошибок при компиляции ассемблера
		# так как в NASM нельзя что бы функции начинались с цифр
		assembly += f"_{func_id}:\n"
		assembly += "push bp\n"
		assembly += "mov bp, sp\n"

		unfold_calls(ast, func_id, ast[func_id]["output"], ast[func_id]["input"])

	assembly += "times 510 - ($-$$) db 0\n"
	assembly += "dw 0xAA55"

	return assembly