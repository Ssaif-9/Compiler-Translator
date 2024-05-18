# C to Python Translator with Syntax Tree Generation

This project is a C to Python translator with syntax tree generation, built in Python. It tokenizes, parses, and translates simple C code to Python, and generates a syntax tree for the given C code.

## Features

- Tokenizes C code into various tokens.
- Parses tokens to generate a syntax tree.
- Translates C code to equivalent Python code.
- Displays and saves the syntax tree using NLTK.

## Prerequisites

- Python 3.6+
- NLTK library

## Installation

1. Clone the repository:
    ```
    git clone https://github.com/yourusername/c-to-python-translator.git
    cd c-to-python-translator
    ```

2. Install the required libraries:
    ```
    pip install nltk
    ```

3. Ensure you have an `input.txt` file with C code in the same directory.

## Code Structure

### Tokenizer

The `tokenize` function takes the input C code and tokenizes it based on predefined patterns.

### Parser

The `Parser` class takes the list of tokens and generates a syntax tree. It includes methods to parse different components of C code like declarations, statements, expressions, etc.

### Translation

The `translate_c_to_python` function translates the tokenized C code to equivalent Python code.

### Syntax Tree

The `TreeNode` class is used to build and print the syntax tree. The tree can also be visualized using NLTK.
