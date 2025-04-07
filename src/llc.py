import os
import sys
import json
import argparse

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
	ast = {
		"program": []
	}

	i = 0

	while i < len(tokens):
		if tokens[i] == "def" and len(tokens) > i + 4:
			function_id = tokens[i + 1]

			if function_id in ast["program"]:
				print(f"Error: {function_id} redefined")
				return

			function_input = tokens[i + 2]
			function_output = tokens[i + 4]

			function = {
				"def": function_id,
				"input": function_input,
				"output": function_output
			}

			ast["program"].append(function)

			i += 4
			continue

		i += 1

	return ast

def inline_function(functions, function_id):
	pass

def compiler(filename):
	code = load_file(filename)

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

if __name__ == "__main__":
	parser = argparse.ArgumentParser()

	parser.add_argument("input_file", type=str, help="Input file")

	args = parser.parse_args()

	compiler(args.input_file)