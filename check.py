import interpreter
from tokens import token

class checker:
  def __init__(self, text):
    self.text = text
    self.check()
  def check(self):
    if self.text == "out":
      try:
        interpreter.interpreter(self.text.append(token.Result(token.TokenTypes.semi)))
        return 0
      except:
        return 1
