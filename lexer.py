from tokens import token
from string import digits
from copy import copy

WHITESPACE = " \n"

"""The lexer takes in a string and turns it into a list of tokens that represent different characters
This is passed to the interpreter for it to interpret. An example:
out math 5 * 5;;
Is equal to
TokenTypes.builtin:out, TokenTypes.builtin:math, TokenTypes.integer:5, TokenTypes.multiply, TokenTypes.integer:5, TokenTypes.semi, TokenTypes.semi
Tokens are defined in tokens.tokens.py and I'd recommend checking out those comments"""
class lexer:
  def __init__(self, command):
    # This is the lest of tokens
    self.tokens = []
    # This is so we can set self.char = to next(command) in advance
    self.command = iter(command)
    # Without this char is equal to nothing and raises an error
    self.advance()

  def advance(self):
    try:
      # Char is the current line of input
      self.char = next(self.command)
    except StopIteration:
      # if nothing is left in the string make it equal to None
      self.char = None

  def generate_tokens(self):
    # If there is no input left, exit the lexer
    while self.char is not None:
      # If the current character is whitespace ignore it. This makes
      # out     "Hello, world!"
      # as legal as
      # out "Hello, world!"
      if self.char in WHITESPACE:
        self.advance()
      # This is the standard for characters. if char == tokval
      # tokens.append(The result from tokens.py)
      elif self.char == "_":
        self.tokens.append(token.Result(token.TokenTypes.underscore))
        self.advance()
      # This is slightly more advanced
      # Checkout the generate_string function
      # This is more or less the same for single quotes as well
      elif self.char == "\"":
        # It does this before and after no matter what because it's solved in generate_string
        self.tokens.append(token.Result(token.TokenTypes.dquote))
        self.advance()
        # This is the first value. This would be represented as TokenTypes.string:Your string here
        self.tokens.append(token.Result(token.TokenTypes.string, self.generate_string()))
        self.advance()
        self.tokens.append(token.Result(token.TokenTypes.dquote))
      elif self.char == "'":
        self.tokens.append(token.Result(token.TokenTypes.squote))
        self.advance()
        self.tokens.append(token.Result(token.TokenTypes.string, self.generate_string("'")))
        self.advance()
        self.tokens.append(token.Result(token.TokenTypes.squote))
      # The rest of these should be pretty straightforward based on everything
      elif self.char == ";":
        self.tokens.append(token.Result(token.TokenTypes.semi))
        self.advance()
      elif self.char == "=":
        self.advance()
        if self.char == "=":
          self.tokens.append(token.Result(token.TokenTypes.iequal))
          self.advance()
        else:
          self.tokens.append(token.Result(token.TokenTypes.equal))
      # I forgot to mention, #s in QBall signify negetive signs
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
        # Run until char is \n
        self.generate_message()
      elif self.char == "(":
        self.advance()
        if self.char == "(":
          # This runs like:
          # Is the char equal to )? Is the next )? If so break!
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
      elif self.char == "!":
        self.advance()
        if self.char == "=":
          self.tokens.append(token.Result(token.TokenTypes.nequal))
          self.advance()
        else:
          self.tokens.append(token.Result(token.TokenTypes.exclamation))
      else:
        result = token.Result(token.TokenTypes.builtin, self.generate_function())
        # I don't remember why I need this, I just do
        if self.char is not None and self.char not in "=;[]":
          self.advance()
        self.tokens.append(result)
    return self.tokens
  def generate_function(self):
    function = ""
    # This is used for any unrecognized tokens
    while self.char is not None and self.char not in WHITESPACE + "=;[]+-*/": # Without this you would need to do out "Hello!" ;
      function += self.char
      self.advance()
    return function
  
  def generate_string(self, symbol: str='"'):
    string = ""
    # Cancatonate the char until the char is None or symbol. Symbol = ' or " depending on which you used
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
    # Similar to generate_string
    while self.char is not None and self.char in digits + "." + "#":
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
# You should now have a basic understanding of the lexer
