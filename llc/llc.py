import os
import sys
import json
import argparse
from preprocessor import Preprocessor
from lexer import Lexer
from parser import Parser
from arch.x86 import LL16_Generator

DEBUG = True

def compile(code, flags):
	# Препроцессор
	preprocessor = Preprocessor(code)
	code = preprocessor.preprocess()

	if DEBUG:
		print("Preprocessor:")
		print(code)
		print("")

	# Если есть флаг -P для генерации кода препроцессора
	if flags["P"]:
		with open(args.output_file, "w") as file:
			file.write(code)
		return

	# Токенизация (Лексер)
	lexer = Lexer(code)
	tokens = lexer.tokenize()

	if DEBUG:
		print("Tokens:")
		print(tokens)
		print("")

	# Построение AST (Парсер)
	ast_parser = Parser(tokens)
	ast = ast_parser.parse()

	if DEBUG:
		print("AST:")
		print(ast)
		print("")

	# Генерация ассемблерного кода
	generator = LL16_Generator(ast)
	assembly = generator.generate()

	if DEBUG:
		print("Assembly:")
		print(assembly)

	with open(args.output_file, "w") as file:
		file.write(assembly)

if __name__ == "__main__":
	parser = argparse.ArgumentParser()

	parser.add_argument("input_file", type=str, help="Input file")
	parser.add_argument("-o", "--output_file", type=str, default="output.asm", help="Output file")
	parser.add_argument("-P", "--preprocess", action="store_true", help="Generate preprocess code")

	args = parser.parse_args()

	if not os.path.exists(args.input_file):
		print("File not exists")
		sys.exit(1)

	with open(args.input_file, "r") as file:
		code = file.read()

	flags = {"P": args.preprocess}

	compile(code, flags)