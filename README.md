# LLC
LLC - это компилятор языка LL в ассемблер NASM под 16-битную архитектуру.

### Использование
```
llc.py <input_file>
```

# LL

LL (LISP and Lambda) - это компилируемый функциональный язык программирования в котором все является функцией. Да, все является функцией. Вообще все. За основу взяты лямбда-исчисления (по факту просто с измененным синтаксисом). Получилось что то на подобии LISP.

# Спецификация

## Основные принципы языка
1. Есть функция и результат выполнения функции. У любой функции должен быть результат.
2. Существует абстрактная функция f которая представляет некоторую операцию и существует для определения чисел. Она не определена в исходном коде, и определяется при компиляции.
3. Существует функция x (начальное число). На самом деле это не функция, а число ноль. Ну или функция которая не принимает аргументов и всегда возвращает ноль. Функция x так же, как и функция f не определена в исходном коде и определяется при компиляции. На самом деле этот принцип скорее всего требует доработки.
4. У любой программы есть главная функция (точка входа) - main. При запуске программы управление автоматически передается функции main.
5. У главной функции main есть аргументы f и x - это внешние функции которые определены в самом компиляторе и передаются в main на этапе компиляции.


## Функции

Функцию можно объявить и присвоить ей имя с помощью ключевого слова def для дальнейшего использования:
`def <name> (<input>) -> (<output>)`

Пример:
`def nothing_func (x) -> (x)`

Если функция была заранее определена, то вызывается она следующим образом:
`nothing_func(a)`


## Комментарии
В языке можно писать комментарии. При компиляции они будут игнорироваться. Синтаксис:
`; комментарий`


## Пример
```
def 0 () -> (x)			; ноль
def 1 () -> (f(x))		; один
def 2 () -> (f(f(x)))	; два

; функция сложения
def + (m, n) -> (m(f, n(f, x)))

; главная функция (точка входа)
def main () -> (+(1, 2))
```


# Компиляция
Компиляция программы на языке LL происходит в несколько этапов: препроцессор, лексер, парсер, генерация кода в и оптимизация кода. Разберем каждый из них.

## Препроцессор
Удаляет комментарии, пустые строки и лишние пробелы, реализует макросы.


## Лексер
Разбивает код на токены, на выходе выдает массив токенов. Например:
`['def', '0', '()', '->', '(x)', 'def', '1', '()', '->', '(f(x))', 'def', '2', '()', '->', '(f(f(x)))']`


## Парсер
Строит абстрактное синтаксическое дерево (AST) которое необходимо для определения связей между функциями. Например:

```
Program
│
├── Def 1
          ├── Input: ()
          └── Output: f(x)
│
├── Def 2
          ├── Input: ()
          └── Output: f(f(x))
│
├── Def +
          ├── Input: m, n
          └── Output: m(f, n(f, x))
│
└── Def main
          ├── Input: f, x
          └── Output: +(1, 2)
```


## Генерация кода
На этом этапе происходит трансляция кода в целевой язык, в данном случае ассемблер NASM под 16-битную архитектуру.


## Пример компияции
Исходный код на языке LL:
```
def test (y) -> (y)

def main(f, x) -> (test(test))
```

Скомпилированный код в ассемблер NASM (16 bits):
```
bits 16

test:
	push bp				; сохраняем BP в стек

	mov bp, sp 			; копируем указатель на вершину стека в BP
	mov ax, [bp + 4]	; передаем аргумент (аргументы в функции передаются через стек) в регистр AX
						; (результат выполнения функций передается в регистр AX)

	mov sp, bp			; обновляем указатель на вершину стека (копируем в SP из BP)
	pop bp				; извлекаем BP из стека
	ret

main:
	push test			; передаем аргумент в вызываемую функцию через стек
	call test			; вызываем функцию
	ret
```