from flask import Flask, render_template, request
import ply.lex as lex
import ply.yacc as yacc
from anytree import Node
from anytree.exporter import JsonExporter

app = Flask(__name__)

# Definición de tokens
tokens = (
    'NUMBER',  
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE',  
    'LPAREN', 'RPAREN',  
)

# Expresiones regulares para los operadores
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'

# Regla para manejar números enteros y decimales
def t_NUMBER(t):
    r'\d+\.\d+|\d+'  # Acepta tanto enteros como decimales
    if '.' in t.value:
        t.value = float(t.value)  # Convertir a float si es decimal
    else:
        t.value = int(t.value)  # Si no tiene punto, convertir a int
    return t

# Ignorar espacios y tabulaciones
t_ignore = ' \t'

# Manejo de errores en el lexer
def t_error(t):
    print(f"Carácter no válido: {t.value[0]}")
    t.lexer.skip(1)

# Crear el lexer
lexer = lex.lex()

# Definición de precedencia de operadores
precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

# Definición de la regla para las operaciones binarias
def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    p[0] = Node(f"{p[2]}", children=[p[1], p[3]])

# Definición de la regla para paréntesis
def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

# Definición de la regla para números
def p_expression_number(p):
    'expression : NUMBER'
    p[0] = Node(f"NUM({p[1]})")

# Manejo de errores en el parser
def p_error(p):
    print("Error de sintaxis en:", p)

# Crear el parser
parser = yacc.yacc()

@app.route('/', methods=['GET', 'POST'])
def index():
    tokens_list = []
    total_tokens = 0
    total_numbers = 0
    total_operators = 0
    syntax_tree = None
    tree_structure = ""
    operation = ""
    result = ""

    if request.method == 'POST':
        operation = request.form['operation']
        lexer.input(operation)

        while tok := lexer.token():
            tokens_list.append(tok)
            total_tokens += 1
            if tok.type == 'NUMBER':
                total_numbers += 1
            elif tok.type in {'PLUS', 'MINUS', 'TIMES', 'DIVIDE'}:
                total_operators += 1

        try:
            syntax_tree = parser.parse(operation, lexer=lexer)
            result = eval(operation)  # Python maneja automáticamente los floats
            operation = str(result)
        except Exception as e:
            result = "Error"
            print(f"Error evaluando la operación: {e}")

        if syntax_tree:
            exporter = JsonExporter()
            tree_structure = exporter.export(syntax_tree)

    return render_template(
        'index.html',
        operation=operation,
        tokens_list=tokens_list,
        total_tokens=total_tokens,
        total_numbers=total_numbers,
        total_operators=total_operators,
        tree_structure=tree_structure
    )

if __name__ == '__main__':
    app.run(debug=True)
