# Lea

Basic programming language i'm developing using python

# Examples

1) Hello World!
   ```bash
   echo "Hello World!" /echo
   ```

2) Input and variable
   ```bash
   "text": input "Type your input: " /input
   echo "Input: " + $"text" /echo
   ```

3) If statements
   ```bash
   "i": 25
   "j": 50
   
   if $"i" == 25 ??
       echo "Hello World!" /echo
       if $"j"/2 == $"i" ??
           echo "Hello World!" /echo
       /if
   /if
   ```
   Or:
   ```bash
   "i": 1
   if $"i" == 1 ?? ;; echo "Hello World!" /echo ;; /if
4) Loops
   ```bash
   "i": 0
   "text": "Hello World!"
   
   loop $"i" != $"text".len ??
       echo $"text"[$"i"] /echo
       "i": $"i"++
   /loop
   ```
   Or:
   ```bash
   "i": 0
   "text": "Hello World!"
   loop $"i" <= 10 ?? ;; echo $"text"[$"i"] /echo ;; "i": $"i"++ ;; /loop
5) Functions
   ```bash
   function add ?? "add.1", "add.2"
      "add.result": $"add.1" + $"add.2"
      return $"add.result" /return
   /function
      
   "example_function_call": add 1, 2 /add
   echo $"example_function_call" /echo
   ```
   Or:
   ```bash
   function add ?? "add.1", "add.2" ;; return $"add.1" + $"add.2" /return ;; /function
   echo add 1, 2 /add /echo
   ```
