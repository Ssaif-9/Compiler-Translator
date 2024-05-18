import re
import os
from nltk.tree import Tree

# Token types
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
    (STRING_CONSTANT, r'"([^"]*)"'),
    (INT, r'int'),
    (FLOAT, r'float'),
    (CHAR, r'char'),
    (DOUBLE, r'double'),
    (KEYWORD, r"if|else|for|while"),
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
        
        while self.current_token and self.current_token[0] in (INT, FLOAT, CHAR , DOUBLE , KEYWORD , IDENTIFIER):
            if self.current_token and self.current_token[0] == KEYWORD :
                if self.current_token[1] == 'if':
                    node.add_child(self.if_statement())
                elif self.current_token[1] == 'for':
                    node.add_child(self.for_statement())
                elif self.current_token[1] == 'while':
                    node.add_child(self.while_statement())
            elif self.current_token and self.current_token[0] in (INT, FLOAT, CHAR , DOUBLE):
                node.add_child(self.declaration()) 
            else:
                node.add_child(self.assignment_statement())
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
        node = TreeNode('AssignmentStatement')
        node.add_child(self.identifier())

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
                elif self.current_token[1] == 'while':
                    node.add_child(self.while_statement())
            elif self.current_token[0] in  (INT, FLOAT, CHAR, DOUBLE):
                node.add_child(self.declaration_list())
            else:
                node.add_child(self.assignment_statement())
        return node
    
    def condition(self):
        node = TreeNode('condition')
        node.add_child(self.identifier())
        if self.current_token and self.current_token[0] == RELATIONAL_OP:
            node.add_child(TreeNode(self.current_token[1]))
            self.match(RELATIONAL_OP)
            node.add_child(self.expression())

        
        return node

    def if_statement(self):
        node = TreeNode('IfStatement')
        node.add_child(TreeNode(self.current_token[1]))
        self.match(KEYWORD, 'if')
        node.add_child(TreeNode(self.current_token[1]))
        self.match(LEFT_PAREN)
        node.add_child(self.condition())
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
        node.add_child(self.condition())
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
        node.add_child(self.condition())
        node.add_child(TreeNode(self.current_token[1]))
        self.match(RIGHT_PAREN)
        node.add_child(TreeNode(self.current_token[1]))
        self.match(LEFT_BRACE)
        node.add_child(self.statement_list())
        node.add_child(TreeNode(self.current_token[1]))
        self.match(RIGHT_BRACE)
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
        node.add_child(self.term())
        if self.current_token and self.current_token[0] == ADDITIVE_OP :
            node.add_child(TreeNode(self.current_token[1]))
            self.match(ADDITIVE_OP)
            node.add_child(self.expression())
        
        return node


    def term(self):
        node = TreeNode('Term')
        node.add_child(self.factor())
        while self.current_token and self.current_token[0] in (MULTIPLICATIVE_OP):
            node.add_child(TreeNode(self.current_token[1]))
            self.match(self.current_token[0])
            node.add_child(self.term())
        
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



def translate_c_to_python(tokens):
    python_code = []
    indent_level = 0

    def indent():
        return '    ' * indent_level

    i = 0
    while i < len(tokens):
        if len(tokens[i]) != 2:
            i += 1
            continue

        token_type, token_value = tokens[i]

        if token_type == 'INCLUDE':
            # Skip include statements
            i += 2  # Skip include and the string constant
        elif token_type == 'INT' and tokens[i+1][0] == 'KEYWORD' and tokens[i+1][1] == 'main':
            python_code.append("def main():")
            indent_level += 1
            i += 4  # Skip 'int main() {'
        elif token_type == 'INT':
            # Handle variable declarations
            var_name = tokens[i+1][1]
            if tokens[i+2][0] == 'ASSIGNMENT_OP':
                var_value = tokens[i+3][1]
                python_code.append(f"{indent()}{var_name} = {var_value}")
                i += 5  # Skip 'int var_name = value;'
            else:
                python_code.append(f"{indent()}{var_name} = None")
                i += 3  # Skip 'int var_name;'
        elif token_type == 'KEYWORD' and token_value == 'if':
            condition = []
            i += 2  # Skip 'if ('
            while tokens[i][0] != 'RIGHT_PAREN':
                condition.append(tokens[i][1])
                i += 1
            condition_str = ' '.join(condition)
            python_code.append(f"{indent()}if {condition_str}:")
            indent_level += 1
            i += 2  # Skip ') {'
        elif token_type == 'KEYWORD' and token_value == 'for':
            # Handle for loop
            init_var = tokens[i+3][1]
            init_val = tokens[i+5][1]
            cond_var = tokens[i+8][1]
            cond_op = tokens[i+9][1]
            cond_val = tokens[i+9][1]
            iter_var = tokens[i+12][1]
            iter_op = tokens[i+13][1]
            if cond_op == '<':
                range_end = cond_val
            else:
                # Handle other relational operators if needed
                range_end = cond_val

            if iter_op == '++':
                python_code.append(f"{indent()}for {init_var} in range({init_val}, {range_end}):")
            elif iter_op == '--':
                python_code.append(f"{indent()}for {init_var} in range({init_val}, {range_end}, -1):")

            indent_level += 1
            i += 14  # Skip 'for (int var = val; var < val; var++) {'
        elif token_type == 'KEYWORD' and token_value == 'while':
            condition = []
            i += 2  # Skip 'while ('
            while tokens[i][0] != 'RIGHT_PAREN':
                condition.append(tokens[i][1])
                i += 1
            condition_str = ' '.join(condition)
            python_code.append(f"{indent()}while {condition_str}:")
            indent_level += 1
            i += 2  # Skip ') {'
        elif token_type == 'KEYWORD' and token_value == 'printf':
            message = tokens[i+2][1].strip('"')
            if tokens[i+3][0] == 'COMMA':
                var_name = tokens[i+4][1]
                python_code.append(f"{indent()}print(\"{message}\" % {var_name})")
                i += 7  # Skip 'printf("message", var_name);'
            else:
                python_code.append(f"{indent()}print(\"{message}\")")
                i += 5  # Skip 'printf("message");'
        elif token_type == 'IDENTIFIER' and tokens[i+1][0] == 'ASSIGNMENT_OP':
            var_name = token_value
            expression = []
            i += 2  # Skip 'var_name ='
            while tokens[i][0] != 'SEMICOLON':
                expression.append(tokens[i][1])
                i += 1
            expression_str = ' '.join(expression)
            python_code.append(f"{indent()}{var_name} = {expression_str}")
            i += 1  # Skip ';'
        elif token_type == 'IDENTIFIER' and tokens[i+1][0] == 'INCREMENT_OP':
            var_name = token_value
            if tokens[i+1][1] == '++':
                python_code.append(f"{indent()}{var_name} += 1")
            elif tokens[i+1][1] == '--':
                python_code.append(f"{indent()}{var_name} -= 1")
            i += 3  # Skip 'var_name++' or 'var_name--'
        elif token_type == 'KEYWORD' and token_value == 'return':
            return_value = tokens[i+1][1]
            python_code.append(f"{indent()}return {return_value}")
            i += 3  # Skip 'return value;'
        elif token_type == 'LEFT_BRACE':
            i += 1  # Skip '{'
        elif token_type == 'RIGHT_BRACE':
            indent_level -= 1
            i += 1  # Skip '}'
        else:
            i += 1  # Skip other tokens

    return '\n'.join(python_code)
    
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
    c_program = f.read()

# Tokenize the C code
tokenizer = tokenize(c_program)

# Translate the C code to Python
translated_content = translate_c_to_python(tokenizer)

# Create the parser
parser = Parser(tokenizer)
syntax_tree = parser.program()

print("Done") #only for debuging

# Print the parse tree
tree = syntax_tree.to_nltk_tree()

print("Done2")  #only for debuging

output_file = os.path.join(current_directory, "output.txt")
with open(output_file, "w") as f:
    f.write("\n/********************************************************/\n")
    f.write("/*\t\t\t\t\t\tInput C code\t\t\t\t\t\t/*")
    f.write("\n/********************************************************/\n\n")
    f.write(str(c_program))
    f.write("\n/********************************************************/\n")
    f.write("/*\t\t\t\t\t\tTranslate C code To Python Code\t\t\t\t\t\t*/")
    f.write("\n/********************************************************/\n\n")
    f.write(str(translated_content))
    f.write("\n/********************************************************/\n")
    f.write("/*\t\t\t\t\t\tOutput of  Tokenizer\t\t\t\t\t\t")
    f.write("\n/********************************************************/\n\n")
    f.write(str(tokenizer))
    f.write("\n/********************************************************/\n")
    f.write("/*\t\t\t\t\t\tParse Tree\t\t\t\t\t\t/*")
    f.write("\n/********************************************************/\n\n")
    f.write(str(syntax_tree))

print("Tree saved to", output_file)
tree.draw()
print("Done3")   #only for debuging

# Save the parse tree to a file

