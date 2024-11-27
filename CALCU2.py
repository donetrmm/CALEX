from flask import Flask, render_template, request
import ply.lex as lex
import ply.yacc as yacc
from anytree import Node
from anytree.exporter import JsonExporter

app = Flask(__name__)

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
    r'\d+\.\d+|\d+' 
    if '.' in t.value:
        t.value = float(t.value)  
    else:
        t.value = int(t.value)  
    return t

t_ignore = ' \t'

def t_error(t):
    print(f"Carácter no válido: {t.value[0]}")
    t.lexer.skip(1)

lexer = lex.lex()

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
)

def p_expression_binop(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression'''
    p[0] = Node(f"{p[2]}", children=[p[1], p[3]])

def p_expression_group(p):
    'expression : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_number(p):
    'expression : NUMBER'
    p[0] = Node(f"NUM({p[1]})")

def p_error(p):
    print("Error de sintaxis en:", p)

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
            result = eval(operation) 
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
