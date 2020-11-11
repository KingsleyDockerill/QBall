from tokens import token
import lexer
import check
from copy import deepcopy
import os
import time
import re
import socket
import threading
import requests
import string

class dictionary(dict):
  def __init__(self):
    self = dict(self)
  
  def add(self, key, value):
    self[key] = value

  def remove(self, key):
    try:
      del self[key]
    except KeyError:
      pass

class object:
  def __init__(self, args: list, funcs: list):
    self.args = args
    self.funcs = funcs
    self.local = dictionary()
    self.global_ = dictionary()

class os_obj:
  def __init__(self):
    self.name = os.name
  def mkdir(self, directory):
    os.mkdir(directory)
  def rename(self, path, name):
    os.rename(path, name)
  def exists(self, path):
    return os.path.exists(path)
  def makefile(self, filename, mode="r"):
    return open(filename, mode)

class regex_obj:
  def __init__(self, string, regex):
    self.string = string
    self.regex = regex

class client_obj:
  def __init__(self):
    self.ip = socket.gethost(socket.gethostname())

class server_obj:
  def __init__(self):
    self.ip = socket.gethostbyname(socket.gethostname())

class requests_obj:
  def __init__(self):
    pass
  def post(self):
    pass

class FunctionReturn(Exception):
  pass

class IllegalBreak(Exception):
  pass

class GlobalVar:
  pass

class LocalVar:
  pass

global_vars = dictionary()
local_vars = dictionary()
function = dictionary()
arg = dictionary()
argvars = dictionary()
using = {"os": False, "regex": False, "server": False, "client": False}
# All reserved keywords that use "end"
ends = ["for", "while", "if", "try"]
EOF = -1

class interpreter:
  def __init__(self, toks, func=False, class_=False, classname=""):
    self.toks = iter(toks)
    self.func = func
    self.class_ = class_
    self.classname = classname
    self.section = 0
    self.tok = token.Result(token.TokenTypes.eof)
    self.advance()

  def advance(self):
    try:
      self.tok = next(self.toks)
    except StopIteration:
      self.section = EOF
      self.tok = None

  def arg(self):
    value = ""
    if self.tok.type in (token.TokenTypes.dquote, token.TokenTypes.squote):
      self.advance()
      value = self.tok.value
      self.advance()
      self.advance()
    elif self.tok.type in (token.TokenTypes.integer, token.TokenTypes.floating):
      value = self.tok.value
      self.advance()
    elif self.tok.value in global_vars:
      name = self.tok.value
      self.advance()
      if self.tok is not None and self.tok.type == token.TokenTypes.lbrack:
        self.advance()
        index = self.arg()
        if self.tok.type != token.TokenTypes.rbrack:
          raise Exception("Expected [index]")
        self.advance()
        value = global_vars[name][index]
      else:
        value = global_vars[name]
      if using["os"] and type(value) == os_obj:
        # cmp using f string to prevent TypeError
        if self.tok is None or f"{self.tok.value}" not in   ("name", "exists"):
          value = os_obj()
        elif self.tok.value == "name":
          value = os_obj().name
          self.advance()
        elif self.tok.value == "exists":
          self.advance()
          value = os_obj().exists(path=self.arg())
      elif using["regex"] and type(value) == regex_obj:
        self.advance()
        if self.tok is None or self.tok.value ==  token.TokenTypes.semi:
          raise Exception("regex requires 2 arguments")
        regex = regex_obj(self.arg(), self.arg())
        if self.tok is None or self.tok.value ==  token.TokenTypes.semi:
          value = regex_obj()
        elif self.tok.value == "findall":
          value = re.findall(regex.regex, regex.string)
          self.advance()
        elif self.tok.value == "search":
          value = re.search(regex.regex, regex.string)
          self.advance()
        elif self.tok.value == "sub":
          self.advance()
          value = re.sub(regex.regex, self.arg(), regex.string)
          self.advance()
        else:
          raise Exception(f"regex object has no atrribute   {self.tok.value}")
      elif type(value) == list:
        string = "["
        for i in value:
          if type(i) == str:
            string += f"'{i}' "
          else:
            string += str(i)
        value = string + "\b]"
    elif self.tok.value in local_vars:
      value = local_vars[self.tok.value]
      self.advance()
    elif self.tok.value == "True":
      value = 1
    elif self.tok.value == "False":
      value = 0
    elif self.tok.value.lower() == "math":
      mathstr = ""
      self.advance()
      while self.tok is not None and self.tok.type != token.TokenTypes.semi:
        if self.tok.type == token.TokenTypes.plus:
          mathstr += "+"
        elif self.tok.type == token.TokenTypes.minus:
          mathstr += "-"
        elif self.tok.type == token.TokenTypes.multiply:
          mathstr += "*"
        elif self.tok.type == token.TokenTypes.divide:
          mathstr += "/"
        elif self.tok.type == token.TokenTypes.and_:
          mathstr += "&"
        elif self.tok.type == token.TokenTypes.or_:
          mathstr += "|"
        elif self.tok.type == token.TokenTypes.xor:
          mathstr += "^"
        elif self.tok.type == token.TokenTypes.greater:
          mathstr += ">>"
        elif self.tok.type == token.TokenTypes.less:
          mathstr += "<<"
        elif self.tok.type == token.TokenTypes.lparen:
          mathstr += "("
        elif self.tok.type == token.TokenTypes.rparen:
          mathstr += ")"
        elif self.tok.type in (token.TokenTypes.integer, token.TokenTypes.floating):
          mathstr += str(self.tok.value)
        elif self.tok.type in (token.TokenTypes.dquote, token.TokenTypes.squote):
          mathstr += self.arg()
        elif self.tok.value in global_vars and type(global_vars[self.tok.value]) == int:
          mathstr += str(global_vars[self.tok.value])
        elif self.tok.value in local_vars and type(local_vars[self.tok.value]) == int:
          mathstr += str(local_vars[self.tok.value])
        elif self.tok.value in global_vars and type(global_vars[self.tok.value]) == str:
          mathstr += f"'{global_vars[self.tok.value]}'"
        elif self.tok.value in local_vars and type(local_vars[self.tok.value]) == str:
          mathstr += f"'{local_vars[self.tok.value]}'"
        else:
          raise Exception("Illegal math operator!")
        self.advance()
      self.advance()
      value = eval(mathstr)
    elif using["os"] and self.tok.value == "os":
      self.advance()
      if self.tok is None or self.tok.value == token.TokenTypes.semi:
        value = os_obj()
      elif self.tok.value == "name":
        value = os_obj().name
        self.advance()
      elif self.tok.value == "exists":
        self.advance()
        value = os_obj().exists(path=self.arg())
      else:
        raise Exception(f"os object has no attribute {self.tok.value}")
    elif using["regex"] and self.tok.value == "regex":
      self.advance()
      if self.tok is None or self.tok.value ==  token.TokenTypes.semi:
          raise Exception("regex expects 2 arguments")
      regex = regex_obj(self.arg(), self.arg())
      if self.tok is None or self.tok.type == token.TokenTypes.semi:
        value = regex
      elif self.tok.value == "findall":
        value = re.findall(regex.regex, regex.string)
        self.advance()
      elif self.tok.value == "search":
        value = re.search(regex.regex, regex.string)
        self.advance()
      elif self.tok.value == "sub":
        self.advance()
        value = re.sub(regex.regex, self.arg(), regex.string)
        self.advance()
      else:
        raise Exception(f"regex object has no atrribute {self.tok.value}")
    elif self.tok.value in using:
      raise Exception(f"""Did you mean do add
  using {self.tok.value}
to your program?""")
    elif self.tok.type == token.TokenTypes.lbrack:
      self.advance()
      value = []
      while self.tok is not None and self.tok.type != token.TokenTypes.rbrack and self.tok.type != token.TokenTypes.semi:
        a = self.arg()
        value.append(a)
      self.advance() if self.tok.type != token.TokenTypes.semi else print(end="")
    elif self.tok.type == token.TokenTypes.and_:
      self.advance()
      value = id(self.arg())
    else:
      raise Exception("Illegal argument")
    if type(value) != str and str(value) == "True":
      value = 1
    return value

  # Since both functions and if/for/etc use end, this handles that
  def ends_in_func(self):
    toks = []
    while self.tok is not None and self.tok.value != "end":
      if self.tok.value in ends:
        toks.append(self.tok)
        self.advance()
        e = self.ends_in_func()
        for i in e:
          toks.append(i)
      toks.append(self.tok)
      self.advance()
    return toks

  def condition(self, temp=[]):
    cond = ""
    if len(temp) < 1:
      del temp
      while self.tok is not None and self.tok.type != token.TokenTypes.semi:
        if self.tok.type == token.TokenTypes.iequal:
          cond += "=="
          self.advance()
        elif self.tok.type == token.TokenTypes.nequal:
          cond += "!="
          self.advance()
        elif self.tok.value == "in":
          cond += "in "
          self.advance()
        elif self.tok.type == token.TokenTypes.exclamation:
          self.advance()
          if self.tok is not None and self.tok.type == token.TokenTypes.builtin and self.tok.value == "in":
            cond += "not in "
            self.advance()
          else:
            cond += "not "
        elif self.tok.type == token.TokenTypes.greater:
          cond += ">"
          self.advance()
        elif self.tok.type == token.TokenTypes.less:
          cond += "<"
          self.advance()
        elif self.tok.type == token.TokenTypes.greatere:
          cond += ">="
          self.advance()
        elif self.tok.type == token.TokenTypes.lesse:
          cond += "<="
          self.advance()
        elif self.tok.type == token.TokenTypes.or_:
          cond += " or "
          self.advance()
        elif self.tok.type == token.TokenTypes.and_:
          cond += " and "
          self.advanc()
        else:
          temp = self.arg()
          cond += f"'{temp}'" if type(temp) == str else str(temp)
    else:
      i = 0
      while i < len(temp):
        try:
          if temp[i].type == token.TokenTypes.iequal:
            cond += "=="
            i += 1
          elif temp[i].type == token.TokenTypes.nequal:
            cond += "!="
            i += 1
          elif temp[i].type == "in":
            cond += "in "
            i += 1
          elif temp[i].type == token.TokenTypes.exclamation:
            i += 1
            if self.tok is not None and self.tok.type ==    token.TokenTypes.builtin and self.tok.value == "in":
              cond += "not in "
              i += 1
            else:
              cond += "not "
              i += 1
          elif temp[i].type == token.TokenTypes.greater:
            cond += ">"
            i += 1
          elif temp[i].type == token.TokenTypes.less:
            cond += "<"
            i += 1
          elif temp[i].type == token.TokenTypes.greatere:
            cond += ">="
            i += 1
          elif temp[i].type == token.TokenTypes.lesse:
            cond += "<="
            i += 1
          else:
            raise Exception("")
        except:
          if type(temp[i]) == GlobalVar:
            i += 1
            cond += str(global_vars[temp[i]])
            i += 1
          elif type(temp[i]) == LocalVar:
            i += 1
            cond += str(local_vars[temp[i]])
            i += 1
          else:
            cond += f"'{temp[i]}'" if type(temp[i]) == str else str(temp[i])
            i += 1
    return eval(cond)
      
  def interpret(self):
    global arg
    while self.tok is not None:
      self.section += 1
      if self.tok.type == token.TokenTypes.builtin:
        if self.tok.value == "out":
          self.advance()
          to_print = []
          sep = " "
          newline = 1
          while self.tok is not None and self.tok.type is not token.TokenTypes.semi:
            if self.tok.value == "sep":
              self.advance()
              if self.tok is not None and self.tok.type == token.TokenTypes.equal:
                self.advance()
                sep = str(self.arg())
              else:
                to_print.append(sep)
                self.advance()
            elif self.tok.value == "newline":
              self.advance()
              if self.tok is not None and self.tok.type == token.TokenTypes.equal:
                self.advance()
                newline = self.arg()
                self.advance() if self.tok.value is not None else print(end="")
              else:
                to_print.append(newline)
                self.advance()
            else:
              to_print.append(str(self.arg()))
          print(sep.join(to_print), end="\n" if newline else "")
          if self.tok is not None and self.tok.type != token.TokenTypes.semi:
            raise Exception("Expected EOL")
          if self.tok is not None:
            self.advance()
        elif self.tok.value == "in":
          self.advance()
          if self.tok in local_vars:
            local_vars[self.tok.value] = input()
          else:
            global_vars[self.tok.value] = input()
          self.advance()
          if self.tok is not None and self.tok.type != token.TokenTypes.semi:
            raise Exception("Expected EOL")
          if self.tok is not None:
            self.advance()
        elif self.tok.value.lower() == "global":
          self.advance()
          name = self.tok.value
          self.advance()
          if self.tok is None or self.tok.type == token.TokenTypes.semi:
            value = ""
          elif self.tok.type == token.TokenTypes.equal:
            self.advance()
            value = self.arg()
            self.advance() if self.tok is not None and self.tok.type in (token.TokenTypes.dquote, token.TokenTypes.squote) else print(end="")
          if self.tok is not None and self.tok.type != token.TokenTypes.semi:
            raise Exception("No ; or EOL")
          if self.tok is not None:
            self.advance()
          global_vars.add(name, value)
        elif self.tok.value.lower() == "local" and self.func is True:
          self.advance()
          name = self.tok.value
          self.advance()
          if self.tok is None or self.tok.type == token.TokenTypes.semi:
            value = ""
          elif self.tok.type == token.TokenTypes.equal:
            self.advance()
            value = self.arg()
            self.advance() if self.tok.type in (token.TokenTypes.dquote, token.TokenTypes.squote) else print(end="")
          if self.tok is not None and self.tok.type != token.TokenTypes.semi:
            raise Exception("No ; or EOL")
          if self.tok is not None:
            self.advance()
          local_vars.add(name, value)
        elif self.tok.value.lower() == "local":
          raise Exception("Local outside of function")
        elif self.tok.value.lower() == "break":
          raise IllegalBreak("Illegal break")
        elif self.tok.value.lower() == "using":
          self.advance()
          using[self.tok.value] = True
          self.advance()
          if self.tok is not None and self.tok.type != token.TokenTypes.semi:
            raise Exception("Expected EOL")
          if self.tok is not None:
            self.advance()
        elif self.tok.value in global_vars:
          name = self.tok.value
          self.advance()
          if self.tok.type == token.TokenTypes.equal:
            self.advance()
            global_vars[name] = self.arg()
          elif self.tok.type == token.TokenTypes.lbrack:
            self.advance()
            index = self.arg()
            if self.tok.type != token.TokenTypes.rbrack:
              raise Exception("Expected [index]")
            self.advance()
            if self.tok.type != token.TokenTypes.equal:
              raise Exception("Expected [index] = arg")
            self.advance()
            a = self.arg()
            try:
              global_vars[name][index] = a
            except:
              try:
                global_vars[name].insert(index, a)
              except:
                global_vars[name] += str(a)
          elif self.tok.type == token.TokenTypes.plus:
            self.advance()
            if self.tok.type == token.TokenTypes.equal:
              self.advance()
              global_vars[name] += self.arg()
            else:
              raise Exception("After + expected =")
          elif self.tok.type == token.TokenTypes.minus:
            self.advance()
            if self.tok.type == token.TokenTypes.equal:
              self.advance()
              global_vars[name] -= self.arg()
            else:
              raise Exception("After - expected =")
          elif self.tok.type == token.TokenTypes.multiply:
            self.advance()
            if self.tok.type == token.TokenTypes.equal:
              self.advance()
              global_vars[name] *= self.arg()
            else:
              raise Exception("After * expected =")
          elif self.tok.type == token.TokenTypes.divide:
            self.advance()
            if self.tok.type == token.TokenTypes.equal:
              self.advance()
              global_vars[name] /= self.arg()
            else:
              raise Exception("After / expected =")
          elif self.tok.type == token.TokenTypes.and_:
            self.advance()
            if self.tok.type == token.TokenTypes.equal:
              self.advance()
              global_vars[name] &= self.arg()
            else:
              raise Exception("After & expected =")
          elif self.tok.type == token.TokenTypes.or_:
            self.advance()
            if self.tok.type == token.TokenTypes.equal:
              self.advance()
              global_vars[name] |= self.arg()
            else:
              raise Exception("After | expected =")
          elif self.tok.type == token.TokenTypes.xor:
            self.advance()
            if self.tok.type == token.TokenTypes.equal:
              self.advance()
              global_vars[name] ^= self.arg()
            else:
              raise Exception("After ^ expected =")
          if self.tok is not None and self.tok.type != token.TokenTypes.semi:
            raise Exception("Expected EOL")
          if self.tok is not None:
            self.advance()
        elif self.tok.value in local_vars:
          name = self.tok.value
          self.advance()
          if self.tok.type == token.TokenTypes.equal:
            self.advance()
            local_vars[name] = self.arg()
          elif self.tok.type == token.TokenTypes.lbrack:
            self.advance()
            index = self.arg()
            if self.tok.type != token.TokenTypes.rbrack:
              raise Exception("Expected [index]")
            self.advance()
            if self.tok.type != token.TokenTypes.equal:
              raise Exception("Expected [index] = arg")
            self.advance()
            a = self.arg()
            try:
              local_vars[name][index] = a
            except:
              try:
                local_vars[name].insert(index, a)
              except:
                local_vars[name] += str(a)
          if self.tok is not None and self.tok.type != token.TokenTypes.semi:
            raise Exception("Expected EOL")
          if self.tok is not None:
            self.advance()
        elif self.tok.value == "if":
          self.advance()
          a = self.condition()
          self.advance()
          toks = []
          while self.tok is not None and self.tok.value != "end" and self.tok.value != "else":
            if self.tok.value in ends:
              e = self.ends_in_func()
              for i in e:
                toks.append(i)
            else:
              toks.append(self.tok)
              self.advance()
          elsetoks = []
          if self.tok is not None and self.tok.value == "else":
            self.advance()
            if self.tok is not None and self.tok.type != token.TokenTypes.semi:
              raise Exception("Expected ; after else")
            self.advance()
            while self.tok is not None and self.tok.value != "end":
              if self.tok.value in ends:
                e = self.ends_in_func()
                for i in e:
                  elsetoks.append(i)
              else:
                elsetoks.append(self.tok)
                self.advance()
          self.advance()
          if a:
            interpreter(toks, True if self.func else False).interpret()
          elif not a:
            interpreter(elsetoks, True if self.func else False).interpret()
        elif self.tok.value == "while":
          self.advance()
          conditional = []
          while self.tok.type != token.TokenTypes.semi:
            try:
              if self.tok.value in global_vars:
                conditional.append(GlobalVar())
                conditional.append(self.tok.value)
                self.advance()
              elif self.tok.value in local_vars:
                conditional.append(LocalVar())
                conditional.append(self.tok.value)
                self.advance()
              else:
                a = self.arg()
                conditional.append(a)
            except:
              conditional.append(self.tok)
              self.advance()
          self.advance()
          a = self.condition(conditional)
          toks = []
          while self.tok is not None and self.tok.value != "end":
            if self.tok.value in ends:
              e = self.ends_in_func()
              for i in e:
                toks.append(i)
            else:
              toks.append(self.tok)
              self.advance()
          self.advance()
          while a:
            interpreter(toks).interpret()
            a = self.condition(conditional)
        elif self.tok.value == "until":
          self.advance()
          conditional = []
          while self.tok.type != token.TokenTypes.semi:
            try:
              if self.tok.value in global_vars:
                conditional.append(GlobalVar())
                conditional.append(self.tok.value)
                self.advance()
              elif self.tok.value in local_vars:
                conditional.append(LocalVar())
                conditional.append(self.tok.value)
                self.advance()
              else:
                a = self.arg()
                conditional.append(a)
            except:
              conditional.append(self.tok)
              self.advance()
          self.advance()
          a = self.condition(conditional)
          toks = []
          while self.tok is not None and self.tok.value != "end":
            print(self.tok)
            if self.tok.value in ends:
              e = self.ends_in_func()
              for i in e:
                toks.append(i)
            else:
              toks.append(self.tok)
              self.advance()
          self.advance()
          while not a:
            interpreter(toks).interpret()
            a = self.condition(conditional)
        elif self.tok.value == "try":
          self.advance()
          if self.tok is not None and self.tok.type != token.TokenTypes.semi:
            raise Exception("No ; after try")
          if self.tok is not None:
            self.advance()
          trytoks = []
          while self.tok is not None and self.tok.value != "except":
            trytoks.append(self.tok)
            self.advance()
          self.advance()
          name = ""
          if self.tok is not None and self.tok.type != token.TokenTypes.semi:
            name = self.tok.value
            self.advance()
            if self.tok is not None and self.tok.type != token.TokenTypes.semi:
              raise Exception("No ; after except")
          if self.tok is not None:
            self.advance()
          tokexcept = []
          while self.tok is not None and self.tok.value != "end":
            if self.tok.value in ends:
              e = self.ends_in_func()
              for i in e:
                toks.append(i)
            else:
              tokexcept.append(self.tok)
              self.advance()
          self.advance()
          try:
            interpreter(trytoks).interpret()
          except Exception as e:
            if name:
              local_vars.add(name, e)
            interpreter(tokexcept).interpret()
            local_vars.remove(name)
        elif self.tok.value in function:
          funcname = self.tok.value
          self.advance()
          for i in arg[funcname]:
            value = ""
            if self.tok.value in local_vars:
              value = local_vars[self.tok.value]
              argvars.add(i, ["local", self.tok.value])
              self.advance()
            elif self.tok.value in global_vars:
              value = global_vars[self.tok.value]
              argvars.add(i, ["global", self.tok.value])
              self.advance()
            else:
              value = self.arg()
            local_vars.add(i, value)
          try:
            interpreter(function[funcname], True).interpret()
          except FunctionReturn:
            pass
          for i in arg[funcname]:
            local_vars.remove(i)
          if self.tok is not None and self.tok.type != token.TokenTypes.semi:
            raise Exception("Expected ; or EOL")
          if self.tok is not None and self.tok.type == token.TokenTypes.semi:
            self.advance()
        elif self.tok.value == "thread":
          self.advance()
          funcname = self.tok.value
          self.advance()
          argstr = ""
          while self.tok is not None and self.tok.type != token.TokenTypes.semi:
            a = self.arg()
            if type(a) != str:
              argstr += str(a)
            else:
              argstr += f"'{a}'"
            argstr += " "
          tokens = lexer.lexer(f"{funcname} {argstr}").generate_tokens()
          threading.Thread(interpreter(tokens).interpret()).start()
        elif self.tok.value == "free":
          self.advance()
          if self.tok.value in global_vars:
            global_vars.remove(self.tok.value)
          elif self.tok.value in local_vars:
              local_vars.remove(self.tok.value)
              self.advance()
          else:
            raise Exception("Expected var arguement")
          self.advance()
          if self.tok is not None and self.tok.type != token.TokenTypes.semi:
            raise Exception("free takes one arguement only")
          if self.tok is not None and self.tok.type == token.TokenTypes.semi:
            self.advance()
        elif self.tok.value == "memcop":
          self.advance()
          var1 = self.tok.value
          self.advance()
          var2 = self.tok.value
          self.advance()
          if var2 in global_vars:
            if var1 in global_vars:
              global_vars[var2] = deepcopy(global_vars[var1])
            elif var1 in local_vars:
              global_vars[var2] = deepcopy(local_vars[var1])
            else:
              raise Exception("Cannot have var1 as a value, must be variable")
          elif var2 in local_vars:
            if var1 in global_vars:
              local_vars[var2] = deepcopy(global_vars[var1])
            elif var1 in local_vars:
              local_vars[var2] = deepcopy(local_vars[var1])
            else:
              raise Exception("Cannot have var1 as a value, must be variable")
          else:
            raise Exception("var2 must be a variable, not a value")
          if self.tok is not None and self.tok.type != token.TokenTypes.semi:
            raise Exception("free takes one arguement only")
          if self.tok is not None and self.tok.type == token.TokenTypes.semi:
            self.advance()
        elif self.tok.value == "slp":
          self.advance()
          a = self.arg()
          time.sleep(a)
          if self.tok is not None and self.tok.type != token.TokenTypes.semi:
            raise Exception("free takes one arguement only")
          if self.tok is not None and self.tok.type == token.TokenTypes.semi:
            self.advance()
        elif self.tok.value == "raise":
          self.advance()
          exception = self.arg()
          raise Exception(exception)
        elif self.tok.value == "str":
          self.advance()
          if self.tok.value in global_vars:
            global_vars[self.tok.value] = str(global_vars[self.tok.value])
            self.advance()
          elif self.tok.value in local_vars:
              local_vars[self.tok.value] = str(global_vars[self.tok.value])
              self.advance()
          if self.tok is not None and self.tok.type != token.TokenTypes.semi:
            raise Exception("No EOL")
          if self.tok is not None:
            self.advance()
        elif self.tok.value == "int":
          self.advance()
          if self.tok.value in global_vars:
            global_vars[self.tok.value] = int(global_vars[self.tok.value])
            self.advance()
          elif self.tok.value in local_vars:
              local_vars[self.tok.value] = int(global_vars[self.tok.value])
              self.advance()
          if self.tok is not None:
            raise Exception("No EOL")
          if self.tok is not None and self.tok.type == token.TokenTypes.semi:
            self.advance()
        elif self.tok.value == "type":
          self.advance()
          typefind = self.arg()
          if self.tok.value in local_vars:
            local_vars[self.tok.value] = type(typefind)
          else:
            global_vars[self.tok.value] = type(typefind)
          self.advance()
          if self.tok is not None:
            raise Exception("No EOL")
          if self.tok is not None and self.tok.type == token.TokenTypes.semi:
            self.advance()
        elif self.tok.value == "sys":
          self.advance()
          a = self.arg()
          os.system(a)
          if self.tok is not None and self.tok.type in (token.TokenTypes.squote, token.TokenTypes.dquote):
            self.advance()
          if self.tok is not None and self.tok.type != token.TokenTypes.semi:
            raise Exception("No ; or EOL")
          if self.tok is not None:
            self.advance()
        elif self.tok.value == "id":
          # This is the equivelent of "out &var"
          self.advance()
          if self.tok.value in global_vars:
            print(str(hex(id(global_vars[self.tok.value])))[1:])
          elif self.tok.value in local_vars:
              print(str(hex(id(local_vars[self.tok.value])))[1:])
          self.advance()
          if self.tok is not None and self.tok.type != token.TokenTypes.semi:
            raise Exception("No EOL")
          if self.tok is not None and self.tok.type == token.TokenTypes.semi:
            self.advance()
        elif self.tok.value.lower() == "for":
          self.advance()
          name = self.tok.value
          self.advance()
          if self.tok.value != "in":
            raise Exception("for loop with no in")
          self.advance()
          iterobj = self.arg()
          self.advance() if self.tok.type in (token.TokenTypes.dquote, token.TokenTypes.squote) else print(end="")
          if self.tok.type != token.TokenTypes.semi:
            raise Exception("No ; in for loop")
          self.advance()
          toks = []
          while self.tok is not None and self.tok.value != "end":
            if self.tok.value in ends:
              e = self.ends_in_func()
              for i in e:
                toks.append(i)
            else:
              toks.append(self.tok)
              self.advance()
          self.advance()
          for i in iterobj:
            global_vars.add(name, i)
            if self.func:
              try:
                interpreter(toks, True).interpret()
              except IllegalBreak:
                break
            else:
              try:
                interpreter(toks).interpret()
              except IllegalBreak:
                break
          global_vars.remove(name)
        elif self.tok.value == "pass":
          self.advance()
          if self.tok is not None and self.tok.type != self.tok.type != token.TokenTypes.semi:
            raise Exception("Expected ; or EOL")
          if self.tok is not None:
            self.advance()
        elif self.tok.value == "return" and self.func:
          self.advance()
          name = self.tok.value
          globalv = True if argvars[name][0] == "global" else False
          name = argvars[name][1]
          self.advance()
          val = self.arg()
          if not globalv:
            local_vars[name] = val
          else:
            global_vars[name] = val
          self.advance()
          if self.tok is not None and self.tok.type != self.tok.type != token.TokenTypes.semi:
            raise Exception("Expected ; or EOL")
          if self.tok is not None:
            self.advance()
          raise FunctionReturn
        elif self.tok.value == "return":
          raise Exception("return outside of function")
        elif self.tok.value == "import":
          self.advance()
          name = f"stdlib/{self.tok.value}.qball"
          raw_name = self.tok.value
          self.advance()
          if os.path.exists(name):
            importopen = open(name).read()
            tokens = lexer.lexer(importopen).generate_tokens()
            interpreter(tokens).interpret()
          elif f"{raw_name}.qball" in os.listdir("stdlib"):
            importopen = open(f"stdlib/{raw_name}/main.qball").read()
            tokens = lexer.lexer(importopen)
            interpreter(tokens).interpret()
          elif raw_name in os.listdir():
            importopen = open(f"{raw_name}/main.qball").read()
            tokens = lexer.lexer(importopen).generate_tokens()
            interpreter(tokens).interpret()
          elif raw_name in os.listdir("stdlib"):
            importopen = open(f"stdlib/{raw_name}/main.qball").read()
            tokens = lexer.lexer(importopen).generate_tokens()
            interpreter(tokens).interpret()
          else:
            importopen = open(f"{raw_name}.qball").read()
            tokens = lexer.lexer(importopen).generate_tokens()
            interpreter(tokens).interpret()
          if self.tok is not None and self.tok.type != self.tok.type != token.TokenTypes.semi:
            raise Exception("Expected ; or EOL")
          if self.tok is not None:
            self.advance()
        elif self.tok.value == "py":
          self.advance()
          arg = self.arg()
          x = compile(arg, "python", "exec")
          # For some unknown reason for py "" code to run you must call it somewhere first. Deleting this single line of code will break this function
          x
          exec(x)
          self.advance()
          if self.tok is not None and self.tok.type != self.tok.type != token.TokenTypes.semi:
            raise Exception("Expected ; or EOL")
          if self.tok is not None:
            self.advance()
        elif self.tok.value == "qstr":
          self.advance()
          arg = self.arg()
          self.advance()
          tokens = lexer.lexer(arg).generate_tokens()
          interpreter(tokens).interpret()
          if self.tok is not None and self.tok.type != self.tok.type != token.TokenTypes.semi:
            raise Exception("Expected ; or EOL")
          if self.tok is not None:
            self.advance()
        else:
          raise Exception(f"Illegal function {self.tok.value}")
      elif self.tok.type == token.TokenTypes.underscore:
        self.advance()
        func_name = self.tok.value
        self.advance()
        args = []
        toks = []
        while self.tok.type != token.TokenTypes.semi:
          args.append(self.tok.value)
          self.advance()
        arg.add(func_name, args)
        self.advance()
        while self.tok is not None and self.tok.value != "end":
          if self.tok.value in ends:
            e = self.ends_in_func()
            for i in e:
              toks.append(i)
          else:
            toks.append(self.tok)
            self.advance()
        self.advance() if self.tok is not None and self.tok.value == "end" else print(end="")
        self.advance() if self.tok is not None and self.tok.value == "end" else print(end="")
        function.add(func_name, toks)
      elif self.tok.type in (token.TokenTypes.squote, token.TokenTypes.dquote):
        self.advance()
        self.advance()
        self.advance()
      else:
        raise Exception("Illegal token")
