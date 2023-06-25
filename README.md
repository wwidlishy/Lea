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
