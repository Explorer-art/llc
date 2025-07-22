def preprocess(code):
	processed_code = ""
	lines = code.split("\n")

	# Удаляем все комментарии и удалеяем лишние пробелы
	for line in lines:
		comment_index = line.find(";")

		if comment_index != -1:
			line = line[:comment_index].rstrip()

		if line.strip():
			processed_code += line + "\n"

	return processed_code