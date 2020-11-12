import subprocess
import tkinter as tk
import lexer
import interpreter

# MUSTS:
# Syntax highlighting
# File tab

# THIS IS TEMPORARY
root = tk.Tk()
root.title("QBE")  # QBall Editor
root.minsize(1530, 1000)
text = tk.Text(root, padx=int(5), pady=int(5))
text.insert(
    tk.INSERT,
    "out 'Hello, world!'\n$ Delete this and start writing your own code!")
var1 = tk.StringVar()
var1.set("File path or name:")
label1 = tk.Label(root, textvariable=var1, height=2)
var2 = tk.StringVar()
var2.set("File path or name:")
label2 = tk.Label(root, textvariable=var2, height=2)
ID1 = tk.StringVar()
ID2 = tk.StringVar()
box1 = tk.Entry(root, textvariable=ID1)
box1.pack()
box2 = tk.Entry(root, textvariable=ID2)
box2.pack()


def create_file():
    with open(box1.get() + ".qball", "w") as f:
        f.write(text.get(1.0, "end"))


def read_file():
    with open(box2.get() + ".qball", "r") as f:
        print(box2.get())
        text.delete(1.0, "end")
        f.seek(0)
        text.insert(1.0, f.read())


def run():
    a = text.get(1.0, "end")
    interpreter.interpreter(lexer.lexer(a).generate_tokens()).interpret()


buttonA = tk.Button(root, text="Save info", command=create_file)
buttonA.pack()
buttonB = tk.Button(root, text="Load info", command=read_file)
buttonB.pack()
label1.pack()
label2.pack()
buttonC = tk.Button(root, text="Run", command=run)
buttonC.pack()
box1.place(x=0, y=30)
box2.place(x=0, y=110)
buttonA.place(x=0, y=50)
buttonB.place(x=0, y=140)
label1.place(x=0, y=0)
label2.place(x=0, y=80)
text.pack()
root.mainloop()
