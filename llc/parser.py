import sys
from ast import *

class Parser:
	def __init__(self, tokens):
		self.tokens = tokens
		self.pos = 0
		self.entry = None
		self.functions = []

	def current(self):
		"""Получить текущий токен"""
		return self.tokens[self.pos] if self.pos < len(self.tokens) else None

	def advance(self):
		"""Следующий токен"""
		self.pos += 1

	def expect(self, token_types: List):
		"""Проверка на соответствие типов"""
		if self.current() and self.current()[0] in token_types:
			return self.current()[1]
		else:
			raise ParserError(f"expected token type {token_types}", position=self.pos)

	def get_func_by_name(self, func_name: str) -> Func:
		"""Получение функции по имени"""
		for func in self.functions:
			if func.name == func_name:
				return func

	def parse(self) -> Program:
		"""Парсинг всех функций"""
		while self.pos < len(self.tokens):
			if self.current()[0] == "KEYWORD" and self.current()[1] == "def":
				self.advance()
				self.functions.append(self.parse_func())

			self.advance()

		self.entry = self.get_func_by_name("main")

		return Program(self.entry, self.functions)

	def parse_func(self) -> Func:
		"""Парсинг функции"""

		# Парсим название функции
		self.expect("CALL_FUNC_ID")

		func_name = self.current()[1]

		# Парсим параметры
		self.advance()
		self.expect("LPARENT")
		self.advance()

		params = []

		while self.current()[0] != "RPARENT":
			if self.current()[0] == "ID":
				params.append(self.current()[1])

			self.advance()

		# Проверяем "-> ("
		self.advance()
		self.expect("ARROW")
		self.advance()
		self.expect("LPARENT")
		self.advance()

		# Парсим тело функции
		body = self.parse_func_body()

		return Func(func_name, params, body)

	def parse_func_body(self) -> List:
		"""Парсинг тела функции"""
		if self.current()[0] == "CALL_FUNC_ID":
			return self.parse_call_func()
		elif self.current()[0] == "ID":
			return self.parse_func_ptr()

		print("error: expected call func or func ptr")
		sys.exit()

	def parse_call_func(self) -> CallFunc:
		"""Парсинг вызова функции"""
		func_name = self.current()[1]

		self.advance()
		self.expect("LPARENT")
		self.advance()

		# Получаем передаваемые аргументы
		args = []

		while self.current()[0] != "RPARENT":
			if self.current()[0] == "CALL_FUNC_ID":
				args.append(self.parse_call_func())
			elif self.current()[0] == "ID":
				args.append(self.parse_func_ptr())

			self.advance()

		return CallFunc(func_name, args)

	def parse_func_ptr(self) -> str:
		"""Парсинг указателя на функцию"""
		return FuncPtr(self.current()[1])

class ParserError(Exception):
	def __init__(self, message, position=None):
		super().__init__(f"{message} at token position {position}")