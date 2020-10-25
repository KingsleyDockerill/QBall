from enum import Enum

class TokenTypes(Enum):
  builtin = 0
  plus = 1
  minus = 2
  multiply = 3
  divide = 4
  integer = 5
  floating = 6
  string = 7
  underscore = 8
  dquote = 9
  squote = 10
  semi = 11
  equal = 12
  lbrack = 13
  rbrack = 14

class Result:
  def __init__(self, type, value=None):
    self.type = type
    self.value = value

  def __repr__(self):
    return f"{self.type}:{self.value}"
