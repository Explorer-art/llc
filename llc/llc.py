import os
import sys
import json
import argparse
from preprocessor import preprocess
from lexer import tokenize
from parser import parse
from generator import generate_assembly

def compile(code):
	print("Source code:")
	print(code)
	print("")

	# Препроцессор
	code = preprocess(code)

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

	if not os.path.exists(args.input_file):
		print("File not exists")
		sys.exit(1)

	with open(args.input_file, "r") as file:
		code = file.read()

	compile(code)