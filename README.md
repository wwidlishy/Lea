# Lea
A new programming language i created using python3.

If you want to look at my terrible code then you go to "src" branch.

# How to run .lea file?

To run your lea file you'll use:
```
lea [path_to_your_dot_lea_file]
```
Or for runing using python interpreter:
```
python lea.py [path_to_your_dot_lea_file]
```

# Example code snippets

(No inline comments for now)

Hello World!:
```
#This is a comment
echo "Hello World!" /echo
```
Printing user input to console:
```
#Declare a variable to store user input
"user input": input "Type something: " /input
echo $"user input" /echo
```
Basic loop:
```
"i": 0
"text": "Hello World!"

loop $"i" != $"text".len-- ?? 0
    echo $"text"[$"i"] /echo
    "i": $"i"++
/loop 0
```
If statement (no else-if and no else):
```
"i": 10

if $"i" == 10 ?? 0
    echo "Hello World!" /echo
/if 0
```
Functions:
```
function add ?? "add.1", "add.2"
    "add.result": $"add.1" + $"add.2"
    return $"add.result" /return
/function add

"example_function_call": add 1, 2 /add
echo $"example_function_call" /echo
```
# Versions
Current version 0.1
Features of v0.1:
    1) printing
    2) variables
    3) user input
    4) if statements
    5) loops
    6) functions
What new is planned for v0.2:
    1) type checking (check if a value is number or string)
    2) type conversion
What new is planned for v0.3:
    1) lists
