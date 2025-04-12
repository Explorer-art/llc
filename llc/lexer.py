def tokenize(code):
	tokens = []
	buffer = ""
	count_parents = 0

	# Переводим код в массив токенов
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