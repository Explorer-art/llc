import os
import sys
import json
import argparse

# Стандартный шаблон программы на ассемблере
STD_ASSEMBLY ="""bits 16

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
"""

# Внешние функции
EXTERNAL_FUNCTIONS_IDS = ["f", "x"]

def load_file(filename):
	if not os.path.exists(filename):
		print("File not exists")
		sys.exit(1)

	with open(filename, "r") as file:
		data = file.read()

	return data

def preprocessor(code):
	processed_code = ""
	lines = code.split("\n")

	# Удаляем все комментарии
	for line in lines:
		comment_index = line.find(";")

		if comment_index != -1:
			line = line[:comment_index].rstrip()

		if line.strip():
			processed_code += line + "\n"

	i = 0
	buffer = ""

	return processed_code

def tokenize(code):
	tokens = []
	buffer = ""
	count_parents = 0

	for char in code:
		if (char == " " or char == "\n" or char == "\t") and not count_parents:
			if buffer:
				tokens.append(buffer)
				buffer = ""
		elif char == " " or char == "\n" or char == "\t":
			continue
		elif char == "(":
			count_parents += 1
			buffer += char
		elif char == ")":
			count_parents -= 1

			buffer += char

			if not count_parents:
				tokens.append(buffer)
				buffer = ""
		else:
			buffer += char

	if buffer:
		tokens.append(buffer)

	return tokens

def parse(tokens):
	ast = {}

	i = 0

	while i < len(tokens):
		if tokens[i] == "def" and len(tokens) > i + 4:
			func_id = tokens[i + 1]

			if func_id in ast:
				print(f"Error: function '{func_id}' redefined")
				return

			# Убираем скобки
			func_input = tokens[i + 2][1:][:-1]

			# Преобразуем строку в массив
			if func_input:
				func_input = func_input.split(",")
			else:
				func_input = None

			func_output = tokens[i + 4][1:][:-1]

			ast[func_id] = {
				"input": func_input,
				"output": func_output
			}

			i += 4
			continue

		i += 1

	return ast

def get_internal_function(ast, func_output):
	buffer = ""
	func_id = ""
	function = None
	count_parents = 0

	for i, char in enumerate(func_output):
		if char == "(":
			count_parents += 1

			func_id = buffer
			buffer = ""
		elif char == ")":
			count_parents -= 1

			# Проверка существования функции
			if not func_id in ast and not func_id in EXTERNAL_FUNCTIONS_IDS:
				print(f"Error: function '{func_id}' undefined")
				sys.exit()

			# Проверяем существуют ли аргументы
			if not buffer:
				print(f"Error: function '{func_id}' not args")
				sys.exit()

			# Получаем аргументы функции
			func_input = buffer.split(",")

			function = {
				"id": func_id,
				"input": func_input
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
		elif char == ",":
			buffer = ""
		else:
			buffer += char

	return function, func_output

def generate_assembly(ast):
	assembly = STD_ASSEMBLY

	for func_id in ast:
		assembly += f"{func_id}:\n"
		assembly += "push bp\n"
		assembly += "mov bp, sp\n"

		# func, func_output = get_internal_function(ast, ast[func_id]["output"])
		# print(func, func_output)

	return assembly

def compiler(code):
	print("Source code:")
	print(code)
	print("")

	# Препроцессор
	code = preprocessor(code)

	print("Preprocessor:")
	print(code)
	print("")

	# Токенизация
	tokens = tokenize(code)

	print("Tokens:")
	print(tokens)
	print("")

	# Построение AST
	ast = parse(tokens)

	print("AST:")
	print(json.dumps(ast, indent=4))

	assembly = generate_assembly(ast)

	print("Assembly:")
	print(assembly)

	with open(args.output_file, "w") as file:
		file.write(assembly)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()

	parser.add_argument("input_file", type=str, help="Input file")
	parser.add_argument("-o", "--output_file", type=str, default="output.asm", help="Output file")

	args = parser.parse_args()

	code = load_file(args.input_file)

	compiler(code)