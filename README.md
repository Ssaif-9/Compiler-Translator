# Compiler_Project

1-The ordinary flow of any C Language programing code which starts with preprocessor directives {#include and include as many as needed to be included} then calls the main function in which start to declare variables then define which type of statements that will be used.

2- The declaration and definition can be used as {int a; || a=0; || int a = 0;} and also can declare many variables in the same line {int a, b, c;}.

3- The statements that can be used are {if || for || while || do-while || printf || assign || return || else closure) statements.

4- All the data types are handled { int || float || double || char } and float Numbers.

5- First of all the code starts with taking the code from “input.c” file which is sent as an attachment with the code.

6- Then it calls a function called “remove comment” which search for the 2 regular expressions of comments in C Language {// or /* …*/} and remove it from the input code.

7- After that send the code which is now clean from any comments to the Tokenizer.

8- In the Tokenizer stored all the token types and regular expressions. Those were stored to match each token in the code with one of the saved patterns in the Tokenizer.

9- If it found a token that doesn’t match with any of the stored patterns, then this will raise an error: INVALID TOKEN.

10-The next stage is Parser which has the “MATCH” function that matches each token in the code with the token types of the Tokenizer.

11-If the matching was following some production rule and found a token that doesn’t follow it, the parser will raise an error that inform me that the expected token is not the given token and the found token is not the right one.

12-Also handled that each KEYWORD reserved must follow its production rule, such as: “printf” and “main” are keywords reserved for {printf statement & main function} but in each statement can’t use any other keyword like “if” instead of “main”, and if this happened this will raise an error {Expected main but found if}. if we don’t handle that the code will accept this error.

13-The tree is drawn 2 times , the first one by using a library called “NLTK” shown at runtime and the second one in a normal save in .txt file where output 3 things which are:
• The code without any comment
• The tokenizer output (Tokens)
• The Tree

Note: The code efficiently detects the path of input and output files, allowing you the flexibility to unzip the file and execute it with ease.

**Input**
![input](https://github.com/EsraaAhmed252/Compiler_Project/assets/99142254/2510ffc3-0644-441f-b46b-bd6549003637)

**Output**
![output_CodeWithoutComments](https://github.com/EsraaAhmed252/Compiler_Project/assets/99142254/cb8739af-739c-44c4-b825-6ed9e1d5725b)

![OutputTokens parseTree](https://github.com/EsraaAhmed252/Compiler_Project/assets/99142254/1aa0ede5-0006-4363-ba80-cf1aafa0860f)

![OutputRunTime](https://github.com/EsraaAhmed252/Compiler_Project/assets/99142254/c126e044-da8e-4dee-99cc-b7e799e216de)
