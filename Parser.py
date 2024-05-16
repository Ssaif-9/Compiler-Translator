import re
import os
from nltk.tree import Tree

# Token types
INCLUDE = 'INCLUDE'
STRING_CONSTANT = 'STRING_CONSTANT'
INT = 'INT'
FLOAT = 'FLOAT'
CHAR = 'CHAR'
DOUBLE = 'DOUBLE'
IDENTIFIER = 'IDENTIFIER'
INTEGER_CONSTANT = 'INTEGER_CONSTANT'
FLOAT_CONSTANT = 'FLOAT_CONSTANT'
SPECIAL_CHARACTER = 'SPECIAL_CHARACTER'
RELATIONAL_OP = 'RELATIONAL_OP'
ADDITIVE_OP = 'ADDITIVE_OP'
MULTIPLICATIVE_OP = 'MULTIPLICATIVE_OP'
INCREMENT_OP = 'INCREMENT_OP'
DECREMENT_OP = 'DECREMENT_OP'
ASSIGNMENT_OP = 'ASSIGNMENT_OP'
LEFT_PAREN = 'LEFT_PAREN'
RIGHT_PAREN = 'RIGHT_PAREN'
LEFT_BRACE = 'LEFT_BRACE'
RIGHT_BRACE = 'RIGHT_BRACE'
LEFT_BRACKET = 'LEFT_BRACKET'
RIGHT_BRACKET = 'RIGHT_BRACKET'
COMMA = 'COMMA'
SEMICOLON = 'SEMICOLON'
NEWLINE = 'NEWLINE'
KEYWORD = 'KEYWORD'

# Token types and their Regular Expression 
token_types = [
    (INCLUDE, r'#include'),
    (STRING_CONSTANT, r'"([^"]*)"'),
    (INT, r'int'),
    (FLOAT, r'float'),
    (CHAR, r'char'),
    (DOUBLE, r'double'),
    (KEYWORD, r"main|printf|if|else|for|while|do|return"),
    (IDENTIFIER, r'[a-zA-Z_][a-zA-Z0-9_]*'),
    (FLOAT_CONSTANT, r'\d*\.\d+([E][-+]?\d+)?'),
    (INTEGER_CONSTANT, r'\d+'),
    (RELATIONAL_OP, r"<|>|==|<=|>=|!= | \|\| | &&"),
    (SPECIAL_CHARACTER, r'[!@#$%^&:\'"\?\\|\~]'),
    (INCREMENT_OP, r'\+\+'),
    (DECREMENT_OP, r'--'),
    (ADDITIVE_OP, r'[+\-]'),
    (MULTIPLICATIVE_OP, r'[\*/]'),
    (ASSIGNMENT_OP, r'='),
    (LEFT_PAREN, r'\('),
    (RIGHT_PAREN, r'\)'),
    (LEFT_BRACE, r'\{'),
    (RIGHT_BRACE, r'\}'),
    (LEFT_BRACKET, r'\['),
    (RIGHT_BRACKET, r'\]'),
    (COMMA, r','),
    (SEMICOLON, r';'),
    (NEWLINE, r'\n')
]

# Function To remove comments before parsing     
def remove_comments(code):
    # Single-line in c //....
    code = re.sub(r'\/\/.*', '', code)

    # Multi-line comment in c /* ... */
    code = re.sub(r'\/\*[\s\S]*?\*\/', '', code)

    return code

# Tokenizer     (Error Handling: if the captured token does not match any specified pattern, Code will print invaled token and the token + remaining code)
def tokenize(code):
    tokens = []
    code = code.strip()
    while code:
        for token_name, pattern in token_types:
            matchi = re.match(pattern, code)
            if matchi:
                token_value = matchi.group(0)
                tokens.append((token_name, token_value))
                code = code[len(token_value):].strip()
                break
        else:
            raise ValueError('Invalid token: ' + code)
    return tokens
def translate(orig):
        replacements = {
            '(': ' ',
            ')': ' :',
            '&&': 'and',
            '||': 'or',
            '{': '',
            '}': '',
            ';': '',
            ',': ' ',
            '!=': 'not equal',
            'string': '',
            'double': '',
            'float': '',
            'bool': '',
            'wchar_t': '',
            'short': '',
            'long': '',
            'char': '',
            'else': ' else:',
            'int': '',
            '#include':'import',
            'printf(':'print(',
            '")': '")',
            }
        
        for key, value in replacements.items():
            orig = orig.replace(key, value)
        return orig
# Parser Class
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token = tokens[0] if tokens else None
        self.token_index = 0

    def match(self, token_type, token_value=None):             #(Error Handling: if the token received in this line is not as expected, it will print both the expected token and the actual token encountered)
        if self.current_token and self.current_token[0] == token_type:
            if token_value and self.current_token[1] != token_value:
                raise ValueError(f"Expected {token_type} {token_value}, but found {self.current_token}")
            print(self.current_token)
            self.token_index += 1
            if self.token_index < len(self.tokens):
                self.current_token = self.tokens[self.token_index]
            else:
                self.current_token = None
        else:
            print(self.current_token)
            raise ValueError(f"Expected {token_type}, but found {self.current_token[0]}")
        
    def __str__(self):
        if self.current_token:
            return f"Current token: {self.current_token}, index: {self.token_index}"
        else:
            return "No more tokens"

    # Context free Grammar
    def program(self):
        node = TreeNode('Program')
        while self.current_token and self.current_token[0] == INCLUDE :
            node.add_child(self.includes())
        node.add_child(self.main_function())
        return node

    def includes(self):
        node = TreeNode('INCLUDES')
        node.add_child(TreeNode(self.current_token[1]))
        self.match(INCLUDE)
        node.add_child(TreeNode(self.current_token[1]))
        self.match(STRING_CONSTANT)
        return node

    def main_function(self):
        node = TreeNode('MainFunction')
        node.add_child(TreeNode(self.current_token[1]))
        self.match(INT)
        node.add_child(TreeNode(self.current_token[1])) 
        self.match(KEYWORD,'main')
        node.add_child(TreeNode(self.current_token[1]))
        self.match(LEFT_PAREN)
        node.add_child(TreeNode(self.current_token[1]))
        self.match(RIGHT_PAREN)
        node.add_child(TreeNode(self.current_token[1]))
        self.match(LEFT_BRACE)
        node.add_child(self.declaration_list())
        node.add_child(self.statement_list())
        node.add_child(TreeNode(self.current_token[1]))
        self.match(RIGHT_BRACE)
        return node
    
    def return_statement(self):
        node = TreeNode('ReturnStatement')
        node.add_child(TreeNode(self.current_token[1]))
        self.match(KEYWORD,'return')
        node.add_child(TreeNode(self.current_token[1]))
        self.match(INTEGER_CONSTANT)
        node.add_child(TreeNode(self.current_token[1]))
        self.match(SEMICOLON)
        return node

    def declaration_list(self):
        node = TreeNode('DeclarationList')
        while self.current_token and self.current_token[0] in (INT, FLOAT, CHAR , DOUBLE):
            node.add_child(self.declaration())
        return node

    def declaration(self):
        node = TreeNode('Declaration')
        node.add_child(self.variable_declaration())
        node.add_child(TreeNode(self.current_token[1]))
        self.match(SEMICOLON)
        return node

    def variable_declaration(self):
        node = TreeNode('VariableDeclaration')
        node.add_child(self.type_specifier())
        node.add_child(self.identifier_list())
        return node

    def type_specifier(self):
        node = TreeNode('TypeSpecifier')
        if self.current_token and self.current_token[0] in (INT, FLOAT, CHAR, DOUBLE):
            node.add_child(TreeNode(self.current_token[1]))
            self.match(self.current_token[0])
        return node

    def identifier_list(self):
        node = TreeNode('IdentifierList')
        node.add_child(TreeNode(self.current_token[1]))
        self.match(IDENTIFIER)
        if self.current_token and self.current_token[0] == COMMA:
            node.add_child(TreeNode(self.current_token[1]))
            self.match(COMMA)
            node.add_child(self.identifier_list())
        elif self.current_token and self.current_token[0] == ASSIGNMENT_OP:
            node.add_child(TreeNode(self.current_token[1]))
            self.match(ASSIGNMENT_OP)
            node.add_child(self.expression())
        return node

    def statement_list(self):
        node = TreeNode('StatementList')
        while self.current_token and self.current_token[0] != RIGHT_BRACE:
            if self.current_token[0] == KEYWORD:
                if self.current_token[1] == 'if':
                    node.add_child(self.if_statement())
                elif self.current_token[1] == 'for':
                    node.add_child(self.for_statement())
                elif self.current_token[1] == 'printf':
                    node.add_child(self.printf_statement())
                elif self.current_token[1] == 'while':
                    node.add_child(self.while_statement())
                elif self.current_token[1] == 'do':
                    node.add_child(self.do_while_statement())
                elif self.current_token[1] == 'return':
                    node.add_child(self.return_statement())
            elif self.current_token[0] in  (INT, FLOAT, CHAR, DOUBLE):
                node.add_child(self.declaration_list())
            else:
                node.add_child(self.assignment_statement())
        return node

    def if_statement(self):
        node = TreeNode('IfStatement')
        node.add_child(TreeNode(self.current_token[1]))
        self.match(KEYWORD, 'if')
        node.add_child(TreeNode(self.current_token[1]))
        self.match(LEFT_PAREN)
        node.add_child(self.expression())
        node.add_child(TreeNode(self.current_token[1]))
        self.match(RIGHT_PAREN)
        node.add_child(TreeNode(self.current_token[1]))
        self.match(LEFT_BRACE)
        node.add_child(self.statement_list())
        node.add_child(TreeNode(self.current_token[1]))
        self.match(RIGHT_BRACE)
        if self.current_token and self.current_token[0] == KEYWORD and self.current_token[1] == 'else':
            node.add_child(TreeNode(self.current_token[1]))
            self.match(KEYWORD, 'else')
            node.add_child(TreeNode(self.current_token[1]))
            self.match(LEFT_BRACE)
            node.add_child(self.statement_list())
            node.add_child(TreeNode(self.current_token[1]))
            self.match(RIGHT_BRACE)
        return node

    def for_statement(self):
        node = TreeNode('ForStatement')
        node.add_child(TreeNode(self.current_token[1]))
        self.match(KEYWORD, 'for')
        node.add_child(TreeNode(self.current_token[1]))
        self.match(LEFT_PAREN)
        if self.current_token and self.current_token[0] in (INT, FLOAT, CHAR, DOUBLE):
            node.add_child(self.type_specifier())
        node.add_child(self.assignment_statement())
        node.add_child(self.expression())
        node.add_child(TreeNode(self.current_token[1]))
        self.match(SEMICOLON)
        node.add_child(self.step_statement())
        node.add_child(TreeNode(self.current_token[1]))
        self.match(RIGHT_PAREN)
        node.add_child(TreeNode(self.current_token[1]))
        self.match(LEFT_BRACE)
        node.add_child(self.statement_list())
        node.add_child(TreeNode(self.current_token[1]))
        self.match(RIGHT_BRACE)
        return node
    
    def while_statement(self):
        node = TreeNode('WhileStatement')
        node.add_child(TreeNode(self.current_token[1]))
        self.match(KEYWORD, 'while')
        node.add_child(TreeNode(self.current_token[1]))
        self.match(LEFT_PAREN)
        node.add_child(self.expression())
        node.add_child(TreeNode(self.current_token[1]))
        self.match(RIGHT_PAREN)
        node.add_child(TreeNode(self.current_token[1]))
        self.match(LEFT_BRACE)
        node.add_child(self.statement_list())
        node.add_child(TreeNode(self.current_token[1]))
        self.match(RIGHT_BRACE)
        return node
    
    def do_while_statement(self):
        node = TreeNode('DoWhileStatement')
        node.add_child(TreeNode(self.current_token[1]))
        self.match(KEYWORD, 'do')
        node.add_child(TreeNode(self.current_token[1]))
        self.match(LEFT_BRACE)
        node.add_child(self.statement_list())
        node.add_child(TreeNode(self.current_token[1]))
        self.match(RIGHT_BRACE)
        node.add_child(TreeNode(self.current_token[1]))
        self.match(KEYWORD, 'while')
        node.add_child(TreeNode(self.current_token[1]))
        self.match(LEFT_PAREN)
        node.add_child(self.expression())
        node.add_child(TreeNode(self.current_token[1]))
        self.match(RIGHT_PAREN)
        node.add_child(TreeNode(self.current_token[1]))
        self.match(SEMICOLON)
        return node
    
    def step_statement(self):
        node = TreeNode('StepStatement')
        node.add_child(TreeNode(self.current_token[1]))
        self.match(IDENTIFIER)
        node.add_child(TreeNode(self.current_token[1]))
        if self.current_token and self.current_token[0] == ASSIGNMENT_OP:
            self.match(ASSIGNMENT_OP)
            node.add_child(self.expression())
        elif self.current_token and self.current_token[0] == INCREMENT_OP:
            self.match(INCREMENT_OP)
        elif self.current_token and self.current_token[0] == DECREMENT_OP:
            self.match(DECREMENT_OP)
        return node


    def printf_statement(self):
        node = TreeNode('PrintfStatement')
        node.add_child(TreeNode(self.current_token[1]))
        self.match(KEYWORD, 'printf')
        node.add_child(TreeNode(self.current_token[1]))
        self.match(LEFT_PAREN)
        node.add_child(self.string_literal())
        if self.current_token and self.current_token[0] == COMMA:
            node.add_child(TreeNode(self.current_token[1]))
            self.match(COMMA)
            node.add_child(self.argument_list())
        node.add_child(TreeNode(self.current_token[1]))
        self.match(RIGHT_PAREN)
        node.add_child(TreeNode(self.current_token[1]))
        self.match(SEMICOLON)
        return node

    def string_literal(self):
        node = TreeNode('StringLiteral')
        node.add_child(TreeNode(self.current_token[1]))
        self.match(STRING_CONSTANT)
        return node

    def argument_list(self):
        node = TreeNode('ArgumentList')
        node.add_child(self.expression())
        if self.current_token and self.current_token[0] == COMMA:
            node.add_child(TreeNode(self.current_token[1]))
            self.match(COMMA)
            node.add_child(self.argument_list())
        return node

    def assignment_statement(self):
        node = TreeNode('AssignmentStatement')
        node.add_child(self.identifier())
        node.add_child(TreeNode(self.current_token[1]))
        self.match(ASSIGNMENT_OP)
        node.add_child(self.expression())
        node.add_child(TreeNode(self.current_token[1]))
        self.match(SEMICOLON)
        return node

    def expression(self):
        node = TreeNode('Expression')
        node.add_child(self.simple_expression())
        if self.current_token and self.current_token[0] == RELATIONAL_OP:
            node.add_child(TreeNode(self.current_token[1]))
            self.match(self.current_token[0])
            node.add_child(self.simple_expression())
        return node

    def simple_expression(self):
        node = TreeNode('SimpleExpression')
        node.add_child(self.term())
        while self.current_token and self.current_token[0] in (ADDITIVE_OP, RELATIONAL_OP):
            node.add_child(TreeNode(self.current_token[1]))
            self.match(self.current_token[0])
            node.add_child(self.term())
        return node

    def term(self):
        node = TreeNode('Term')
        node.add_child(self.factor())
        while self.current_token and self.current_token[0] in (MULTIPLICATIVE_OP, RELATIONAL_OP):
            node.add_child(TreeNode(self.current_token[1]))
            self.match(self.current_token[0])
            node.add_child(self.factor())
        return node

    def factor(self):
        node = TreeNode('Factor')
        if self.current_token and self.current_token[0] == IDENTIFIER:
            node.add_child(self.identifier())
        elif self.current_token and self.current_token[0] == INTEGER_CONSTANT:
            node.add_child(TreeNode(self.current_token[1]))
            self.match(INTEGER_CONSTANT)
        elif self.current_token and self.current_token[0] == FLOAT_CONSTANT:
            node.add_child(TreeNode(self.current_token[1]))
            self.match(FLOAT_CONSTANT)
        elif self.current_token and self.current_token[0] == LEFT_PAREN:
            node.add_child(TreeNode(self.current_token[1]))
            self.match(LEFT_PAREN)
            node.add_child(self.expression())
            node.add_child(TreeNode(self.current_token[1]))
            self.match(RIGHT_PAREN)
        else:
            raise ValueError(f"Invalid factor: {self.current_token}")
        return node
    
    def identifier(self):
        node = TreeNode('Identifier')
        node.add_child(TreeNode(self.current_token[1]))
        self.match(IDENTIFIER)
        return node



    
# Tree Class                     to Draw tree which save in text file 
class TreeNode:
    def __init__(self, label=None):
        self.label = label
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def __str__(self, level=0):
        tree_str = "  " * level + "|_" + str(self.label) + "\n"
        for child in self.children:
            tree_str += child.__str__(level + 1)
        return tree_str

    def to_nltk_tree(self):             #to Draw tree in runtime using NLTK lib
        if self.children:
            return Tree(self.label, [child.to_nltk_tree() for child in self.children])
        return self.label
    
#Take Current Directory of python file 
current_directory = os.path.dirname(os.path.abspath(__file__))

# Read the C code from a file
input_file =  os.path.join(current_directory, "input.txt")

with open(input_file, 'r') as f:
    code_with_comments = f.read()

# Remove comments
c_program = remove_comments(code_with_comments)
translated_content = translate(c_program)
# Tokenize the C code
tokenizer = tokenize(c_program)

# Create the parser
parser = Parser(tokenizer)
syntax_tree = parser.program()
print("Done") #only for debuging
# Print the parse tree
tree = syntax_tree.to_nltk_tree()
print("Done2")  #only for debuging

output_file = os.path.join(current_directory, "output.txt")
with open(output_file, "w") as f:
    f.write("code without comments")
    f.write("\n__________________________________________________________\n\n")
    f.write(str(c_program))
    f.write("Translate C code To Python Code")
    f.write("\n__________________________________________________________\n\n")
    f.write(str(translated_content))
    f.write("\n\nOutput of  Tokenizer")
    f.write("\n__________________________________________________________\n\n")
    f.write(str(tokenizer))
    f.write("\n\nParse Tree")
    f.write("\n__________________________________________________________\n\n")
    f.write(str(syntax_tree))

print("Tree saved to", output_file)
tree.draw()
print("Done3")   #only for debuging

# Save the parse tree to a file

