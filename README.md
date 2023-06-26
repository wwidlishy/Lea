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
   Notice shortened if notation won't work (I will add that later):
   ```bash
   "i": 1
   if $"i" == 1 ?? echo "Hello World!" /echo /if
