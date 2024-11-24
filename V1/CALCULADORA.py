import ply.lex as lex

tokens = (
    'NUMBER', 
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 
    'LPAREN', 'RPAREN',  
)

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value) 
    return t

t_ignore = ' \t'

def t_error(t):
    print(f"Carácter no válido: {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()

data = "3 + 5 * ( 10 - 2 )"
lexer.input(data)

total_tokens = 0
total_numbers = 0
total_operators = 0

tokens_list = []
while tok := lexer.token():
    print(tok)
    tokens_list.append(tok)
    total_tokens += 1
    if tok.type == 'NUMBER':
        total_numbers += 1
    elif tok.type in {'PLUS', 'MINUS', 'TIMES', 'DIVIDE'}:
        total_operators += 1

print("\n=== Resultados ===")
print(f"Total de tokens: {total_tokens}")
print(f"Total de números enteros: {total_numbers}")
print(f"Total de operadores: {total_operators}")
