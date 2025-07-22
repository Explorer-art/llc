import sys

def parse(tokens):
	ast = {
		"f": {
			"input": ["x"],
			"output": "x"
		},
		"x": {
			"input": None,
			"output": ""
		}
	}

	i = 0

	while i < len(tokens):
		if tokens[i] == "def" and len(tokens) > i + 4:
			func_id = tokens[i + 1]

			if func_id in ast:
				print(f"Error: function '{func_id}' redefined")
				sys.exit()

			# Убираем скобки
			func_input = tokens[i + 2][1:][:-1]

			# Преобразуем строку в массив
			if func_input:
				func_input = func_input.split(",")
			else:
				func_input = []

			func_output = tokens[i + 4][1:][:-1]

			ast[func_id] = {
				"input": func_input,
				"output": func_output
			}

			i += 4
			continue

		i += 1

	return ast