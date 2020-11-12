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
Everything you need to know is in [documentation.md](documentation.md)

# Contribute
Fork this to run the QBall shell: https://repl.it/@qballlang/QBall
Changes are commited 8:00 PM EST every day I can

# Contribute
Fork this to run the [QBall shell](https://repl.it/@qballlang/QBall)
Changes are commited 8:00 PM EST every day I can.

# Trello board
The official Trello board: [The official Trello board](https://trello.com/b/cJM6HsR3/qball)

# We're on pip!
Run 
```py
pip install qball-lang
```
to install the package! To use the package use
```py
import QBall
```
It includes the functions evaluate and global_add. Consider this example:
```py
import QBall
# The following code runs evaluate's argument as QBall code
QBall.evaluate("out 'Hello, world!'")
QBall.global_add(a=5)
QBall.evaluate("out a")
```
## To-Do
The To-Do list for Qball!

- [ ] Sting Manipulation
- [ ] Finding
- [ ] Count (print s.count(' '))
- [ ] Slicing
- [ ] Split strings
- [ ] Starts with
- [ ] End with
- [ ] Repeat strings
- [ ] Replace
- [ ] Reverse
- [ ] Strip
> More at https://www.pythonforbeginners.com/basics/string-manipulation-in-python
