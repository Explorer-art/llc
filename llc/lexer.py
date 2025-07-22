import re

TOKEN_SPECIFICATION = {
	"ID": r"[A-Za-z0-9_]+",
	"LPARENT": r"\(",
	"RPARENT": r"\)",
	"ARROW": r"->",
	"COMMA": r",",
	"NEW_LINE": r"\n",
	"MISMATCH": r"."
}

KEYWORDS = [
	"def"
]

TOKEN_REGEX = "|".join(f"(?P<{name}>{pattern})" for name, pattern in TOKEN_SPECIFICATION.items())

class Lexer:
	def __init__(self, code):
		self.code = code

	def tokenize(self):
		tokens = []

		for match in re.finditer(TOKEN_REGEX, self.code):
			group = match.lastgroup
			value = match.group()

			if value in KEYWORDS:
				tokens.append(("KEYWORD", value))
			elif group != "MISMATCH":
				tokens.append((group, value))

		return tokens