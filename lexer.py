from tokens import token
from string import digits
from copy import copy

WHITESPACE = " \n"

class lexer:
  def __init__(self, command):
    self.tokens = []
    self.command = iter(command)
    self.advance()

  def advance(self):
    try:
      self.char = next(self.command)
    except StopIteration:
      self.char = None

  def generate_tokens(self):
    while self.char is not None:
      if self.char in WHITESPACE:
        self.advance()
      elif self.char == "_":
        self.tokens.append(token.Result(token.TokenTypes.underscore))
        self.advance()
      elif self.char == "\"":
        self.tokens.append(token.Result(token.TokenTypes.dquote))
        self.advance()
        self.tokens.append(token.Result(token.TokenTypes.string, self.generate_string()))
        self.advance()
        self.tokens.append(token.Result(token.TokenTypes.dquote))
      elif self.char == "'":
        self.tokens.append(token.Result(token.TokenTypes.squote))
        self.advance()
        self.tokens.append(token.Result(token.TokenTypes.string, self.generate_string("'")))
        self.advance()
        self.tokens.append(token.Result(token.TokenTypes.squote))
        self.advance()
      elif self.char == ";":
        self.tokens.append(token.Result(token.TokenTypes.semi))
        self.advance()
      elif self.char == "=":
        self.advance()
        if self.char == "=":
          self.tokens.append(token.Result(token.TokenTypes.iequal))
        else:
          self.tokens.append(token.Result(token.TokenTypes.equal))
      elif self.char in digits or self.char == "." or self.char == "#":
        a = self.generate_number()
        if type(a) == int:
          self.tokens.append(token.Result(token.TokenTypes.integer, a))
        else:
          self.tokens.append(token.Result(token.TokenTypes.floating, a))
      elif self.char == "[":
        self.tokens.append(token.Result(token.TokenTypes.lbrack))
        self.advance()
      elif self.char == "]":
        self.tokens.append(token.Result(token.TokenTypes.rbrack))
        self.advance()
      elif self.char == "$":
        self.generate_message()
      elif self.char == "(":
        self.advance()
        if self.char == "(":
          self.generate_multiline_message()
          self.advance()
        else:
          self.tokens.append(token.Result(token.TokenTypes.lparen))
          self.advance()
      elif self.char == "+":
        self.advance()
        self.tokens.append(token.Result(token.TokenTypes.plus))
      elif self.char == "-":
        self.advance()
        self.tokens.append(token.Result(token.TokenTypes.minus))
      elif self.char == "*":
        self.advance()
        self.tokens.append(token.Result(token.TokenTypes.multiply))
      elif self.char == "/":
        self.advance()
        self.tokens.append(token.Result(token.TokenTypes.divide))
      elif self.char == "&":
        self.tokens.append(token.Result(token.TokenTypes.and_))
        self.advance()
      elif self.char == "|":
        self.tokens.append(token.Result(token.TokenTypes.or_))
        self.advance()
      elif self.char == "^":
        self.tokens.append(token.Result(token.TokenTypes.xor))
        self.advance()
      elif self.char == "<":
        self.advance()
        if self.char != "=":
          self.tokens.append(token.Result(token.TokenTypes.less))
        else:
          self.tokens.append(token.Result(token.TokenTypes.lesse))
          self.advance()
      elif self.char == ">":
        self.advance()
        if self.char != "=":
          self.tokens.append(token.Result(token.TokenTypes.greater))
        else:
          self.tokens.append(token.Result(token.TokenTypes.greatere))
          self.advance()
      elif self.char == ")":
        self.tokens.append(token.Result(token.TokenTypes.rparen))
        self.advance()
      else:
        result = token.Result(token.TokenTypes.builtin, self.generate_function())
        if self.char is not None and self.char not in "=;[]":
          self.advance()
        self.tokens.append(result)
    return self.tokens
  def generate_function(self):
    function = ""
    while self.char is not None and self.char not in WHITESPACE + "=;[]":
      function += self.char
      self.advance()
    return function
  
  def generate_string(self, symbol: str='"'):
    string = ""
    while self.char is not None and self.char not in symbol:
        if self.char == "\\":
          self.advance()
          if self.char == "t":
            string += "\t"
            self.advance()
          elif self.char == "b":
            string += "\b"
            self.advance()
          elif self.char == "n":
            string += "\n"
            self.advance()
          elif self.char in digits:
            numspace = ""
            while self.char in digits:
              numspace += self.char
              self.advance()
            numspace = int(numspace)
            while numspace != 0:
              string += " "
              numspace -= 1
          else:
            string += self.char
            self.advance()
        else:
            string += self.char
            self.advance()
    if self.char is None:
      raise Exception("No end of string found")
    return string

  def generate_number(self):
    val_type = ""
    num = ""
    while self.char is not None and self.char in digits + "." + "-":
      if self.char in digits + "-" and val_type != "float":
        val_type = "integer"
        num += self.char
      elif self.char == "." or val_type == "float":
        val_type = "float"
        num += self.char
      self.advance()
    if val_type == "integer":
      return int(num)
    elif val_type == "float":
      return float(num)

  def generate_message(self):
    while self.char is not None and self.char != "\n":
      self.advance()
  
  def generate_multiline_message(self):
    while self.char is not None:
      if self.char == ")":
        self.advance()
        if self.char == ")":
          break
      self.advance()
