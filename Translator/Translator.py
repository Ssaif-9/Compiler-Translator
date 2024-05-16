def translate(orig):
    # Define replacements using a dictionary
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
        'int': ''
    }
    
    # Apply replacements sequentially
    for key, value in replacements.items():
        orig = orig.replace(key, value)
    
    return orig

def main(file_name):
    with open(file_name, 'r') as file:
        content = file.read()
        translated_content = translate(content)
    
    with open('output.txt', 'w') as output_file:
        output_file.write(translated_content)

# Usage:
file_name = 'input.txt'  # Provide the path to the input file
main(file_name)