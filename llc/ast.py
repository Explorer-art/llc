from typing import List

class ASTNode:
	pass

class Program(ASTNode):
	def __init__(self, entry: ASTNode, functions: List):
		self.entry = entry
		self.functions = functions

	def __repr__(self):
		return f"Program {{ {str(self.entry)} }}\n\n{"\n".join(str(func) for func in self.functions)}"

class Func(ASTNode):
	def __init__(self, name: str, params: List, body: ASTNode):
		self.name = name
		self.params = params
		self.body = body

	def __repr__(self):
		return f"Func {self.name} ({", ".join(str(param) for param in self.params)}) {{ {str(self.body)} }}"

class CallFunc(ASTNode):
	def __init__(self, name: str, args: List):
		self.name = name
		self.args = args

	def __repr__(self):
		return f"{self.name}({", ".join(str(arg) for arg in self.args)})"

class FuncPtr(ASTNode):
	def __init__(self, name: str):
		self.name = name

	def __repr__(self):
		return f"{self.name}"