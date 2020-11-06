import lexer
import interpreter

while True:
  command = input(">>> ")
  try:
    if command[:4] == "run ":
      command = open(f"{command[4:]}.qball").read()
    result = lexer.lexer(command).generate_tokens()
    interpret = interpreter.interpreter(result)
    pos = interpret.section
    interpret.interpret()
  except Exception as e:
    try:
      print(f"\033[91mError at section {pos}: {e}\033[00m")
    except NameError:
      print(f"\033[91mLexer error: {e}\033[00m")
