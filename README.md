# QBall
QBall is a high-level interpreted language written in Python. It is object oriented and has an easy to learn and use syntax. The following is an example of outputting "Hello, world!" into the console
```
out "Hello, world!";
```
It also has any easy function decleration system
```
$ This is a single line comment
((This is a
multiline comment))
$ This declares a function outarg that takes an argument a
_outarg a;
  out a;
end
outarg "Hello, world!";
```
# Docs
Everything you need to know is in documentation.txt
# Contribute
Go here to contribute: https://repl.it/@qballlang/QBall
Changes are commited 8:00 PM EST every day I can
# Trello board
The official Trello board: https://trello.com/b/cJM6HsR3/qball
# We're on pip!
Run 
```
pip install qball-lang
```
to install the package! To use the package use
```
import QBall
```
It includes the functions evaluate and global_add. Consider this example:
```
import QBall

# The following code runs evaluate's argument as QBall code
QBall.evaluate("out 'Hello, world!'")
# This adds the kwargs to the global variables
QBall.global_add(a=5)
# This will work
QBall.evaluate("out a")
```
