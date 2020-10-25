import lexer
import interpreter

while True:
  command = input(">>> ")
  try:
    result = lexer.lexer(command).generate_tokens()
    interpreter.interpreter(result).interpret()
  except Exception as e:
    print(e)
