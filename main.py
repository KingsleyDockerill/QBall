import lexer
import interpreter

while True:
  command = input(">>> ")
  if command[:4] == "run ":
    command = open(f"{command[4:]}.qball").read()
  try:
    result = lexer.lexer(command).generate_tokens()
    interpreter.interpreter(result).interpret()
  except Exception as e:
    print(f"\033[91m{e}\033[00m")
