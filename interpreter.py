from tokens import token
import lexer
import check
from copy import deepcopy, copy
import os
import time
import re
import socket
import threading
import requests
import string
import sys
import random

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
  def __init__(self, name, args):
    self.name_ = name
    self.args = args
    self.funcs = dictionary()
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
static_vars = dictionary()
function = dictionary()
arg = dictionary()
argvars = dictionary()
limited_funcs = dictionary()
class_funcs = dictionary()
debug = False
using = {"os": False, "regex": False, "server": False,"client": False}
constructors = dictionary()
# All reserved keywords that use "end"
ends = ["for", "while", "if", "try"]
EOF = -1

class interpreter:
  def __init__(self, toks, func=False, class_=False, classname="", return_val=False):
    global debug
    self.toks = iter(toks)
    self.func = func
    self.class_ = class_
    self.classname = classname
    self.section = 0
    self.classyieldresult = []
    self.classglobals = dictionary()
    self.classlocals = dictionary()
    self.classfuncs = dictionary()
    self.return_val = return_val
    self.tok = token.Result(token.TokenTypes.eof)
    self.advance()

  def advance(self):
    try:
      print("Before: ", self.tok) if debug else print(end="")
      self.tok = next(self.toks)
      print("After: ", self.tok) if debug else print(end="")
    except StopIteration:
      self.section = EOF
      self.tok = None

  def arg(self, ret_list=False):
    global local_vars
    value = ""
    if self.tok.type in (token.TokenTypes.dquote, token.TokenTypes.squote):
      self.advance()
      value = self.tok.value
      self.advance()
      self.advance()
    elif self.tok.type in (token.TokenTypes.integer, token.TokenTypes.floating):
      value = self.tok.value
      self.advance()
    elif self.tok.value in self.classglobals:
      name = self.tok.value
      self.advance()
      if self.tok is not None and self.tok.type == token.TokenTypes.lbrack:
        self.advance()
        index = self.arg()
        if self.tok.type != token.TokenTypes.rbrack:
          raise Exception("Expected [index]")
        self.advance()
        value = self.classglobals[name][index]
      else:
        value = self.classglobals[name]
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
    elif self.tok.value in self.classlocals:
      name = self.tok.value
      self.advance()
      if self.tok is not None and self.tok.type == token.TokenTypes.lbrack:
        self.advance()
        index = self.arg()
        if self.tok.type != token.TokenTypes.rbrack:
          raise Exception("Expected [index]")
        self.advance()
        value = self.classlocals[name][index]
      else:
        value = self.classlocals[name]
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
    elif self.tok.value in local_vars:
      name = self.tok.value
      self.advance()
      if self.tok is not None and self.tok.type == token.TokenTypes.lbrack:
        self.advance()
        index = self.arg()
        if self.tok.type != token.TokenTypes.rbrack:
          raise Exception("Expected [index]")
        self.advance()
        value = local_vars[name][index]
      else:
        value = local_vars[name]
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
    elif self.tok.value in static_vars:
      name = self.tok.value
      self.advance()
      if self.tok is not None and self.tok.type == token.TokenTypes.lbrack:
        self.advance()
        index = self.arg()
        if self.tok.type != token.TokenTypes.rbrack:
          raise Exception("Expected [index]")
        self.advance()
        value = static_vars[name][index]
      else:
        value = static_vars[name]
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
    elif self.tok is not None and self.tok.type != token.TokenTypes.semi and type(value) == object:
      class_name = value.name_
      args = dictionary()
      temp_vars = copy(local_vars)
      local_vars = dictionary()
      local_vars = temp_vars
      if self.tok is not None and self.tok.type != token.TokenTypes.semi:
        if self.tok.value is not None and self.tok.value in  value.global_:
          value = value.global_[self.tok.value]
          self.advance()
        elif self.tok.value in class_funcs[class_name]:
          funcname = self.tok.value
          self.advance()
          for i in arg[funcname]:
            value = ""
            if i == "mulargs":
              value = []
              while self.tok.type != token.TokenTypes.semi:
                value.append(self.arg(ret_list=True))
            else:
              value = self.arg(ret_list=True)
            local_vars.add(i, value)
          try:
            a = interpreter(class_funcs[class_name][funcname,  True], return_val=True, class_=True, classname=class_name)
            a.classglobals = value.global_
            a.classlocals = value.local
            a.interpret()
            value.global_ = a.classglobals
            value.local = a.classlocals
          except FunctionReturn as f:
            value = f.args[0]
        else:
          raise Exception(f"Illegal attribute of {class_name}")
    elif self.tok.value == "True":
      value = 1
      self.advance()
    elif self.tok.value == "False":
      value = 0
      self.advance()
    elif self.tok.value == "None":
      value = None
      self.advance()
    elif self.tok.value == "argv":
      value = sys.argv
      self.advance()
    elif self.tok.value == "argc":
      value = len(sys.argv)
      self.advance()
    elif self.tok.value == "time":
      value = time.time()
      self.advance()
    elif self.tok.value == "input":
      self.advance()
      value = input(self.arg())
    elif self.tok.value == "py_eval":
      self.advance()
      value = eval(self.arg())
    elif self.tok.value == "int":
      self.advance()
      value = int(self.arg())
    elif self.tok.value == "str":
      self.advance()
      value = str(self.arg())
    elif self.tok.value == "list":
      self.advance()
      value = list(self.arg(True))
    elif self.tok.value == "float":
      self.advance()
      value = float(self.arg())
    elif self.tok.value == "bool":
      self.advance()
      value = bool(self.arg())
    elif self.tok.value == "tuple":
      self.advance()
      value = tuple(self.arg(True))
    elif self.tok.value == "rand":
      self.advance()
      value = random.random()
    elif self.tok.value == "randint":
      self.advance()
      value = random.randint(int(f"-{sys.maxsize}"), sys.maxsize)
    elif self.tok.value == "try":
      self.advance()
      tokens = []
      while self.tok is not None and self.tok.type != token.TokenTypes.or_:
        tokens.append(self.tok)
        self.advance()
      self.advance()
      try:
        interpreter(tokens).interpret()
        value = 0
      except:
        value = 1
      self.advance()
    elif self.tok.value is not None and self.tok.value in constructors:
      class_name = self.tok.value
      args = dictionary()
      temp_vars = copy(local_vars)
      local_vars = dictionary()
      self.advance()
      for i in arg[class_name]:
        if i == "mulargs":
          a = []
          while self.tok.type != token.TokenTypes.semi:
            a.append(self.arg())
          self.advance()
        else:
          a = self.arg()
        local_vars.add(i, a)
      value = object(class_name, args)
      a = interpreter(constructors[class_name], class_=True, classname=class_name)
      global_ = a.classglobals
      local = a.classlocals
      a.interpret()
      local_vars = temp_vars
      value.global_ = global_
      value.local = local
      if self.tok is not None and self.tok.type != token.TokenTypes.semi:
        if self.tok.value is not None and self.tok.value in value.global_:
          value = value.global_[self.tok.value]
          self.advance()
        elif self.tok.value in class_funcs[class_name]:
          funcname = self.tok.value
          self.advance()
          for i in arg[funcname]:
            value = ""
            if i == "mulargs":
              value = []
              while self.tok.type != token.TokenTypes.semi:
                value.append(self.arg())
              self.advance()
            else:
              value = self.arg()
            local_vars.add(i, value)
          try:
            a = interpreter(class_funcs[class_name][funcname], True, return_val=True, class_=True, classname=class_name)
            a.classglobals = value.global_
            a.classlocals = value.local
            a.interpret()
            value.global_ = a.classglobals
            value.local = a.classlocals
          except FunctionReturn as f:
            value = f.args[0]
        else:
          raise Exception(f"Illegal attribute of {class_name}")
    elif self.tok.value in function:
      funcname = self.tok.value
      self.advance()
      temp_vars = copy(local_vars)
      local_vars = dictionary()
      for i in arg[funcname]:
        value = ""
        if i == "mulargs":
          value = []
          while self.tok.type != token.TokenTypes.semi:
            value.append(self.arg())
          self.advance()
        else:
          value = self.arg()
        local_vars.add(i, value)
      try:
        interpreter(function[funcname], True, return_val=True).interpret()
        value = None
      except FunctionReturn as f:
        value = f.args[0]
      local_vars = temp_vars
      try:
        times = int(funcname.split("_")[0][1:])
        if funcname.split("_")[0][0] != "U":
          raise Exception("")
        if funcname not in limited_funcs:
          limited_funcs.add(funcname, times - 1)
        else:
          limited_funcs[funcname] -= 1
        if not limited_funcs[funcname]:
          function.remove(funcname)
          argvars.remove(funcname)
      except:
        pass
      if self.tok is not None and self.tok.type != token.TokenTypes.semi:
        raise Exception("Expected ; or EOL")
      if self.tok is not None and self.tok.type == token.TokenTypes.semi:
        self.advance()
    elif self.tok.value is not None and self.tok.value.lower() == "math":
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
        elif self.tok.value in global_vars and type(global_vars[self.tok.value]) in (int, float, str):
          mathstr += str(global_vars[self.tok.value])
        elif self.tok.value in local_vars and type(local_vars[self.tok.value]) in (int, float, str):
          mathstr += str(local_vars[self.tok.value])
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
        a = self.arg(ret_list)
        value.append(a)
      self.advance() if self.tok.type != token.TokenTypes.semi else print(end="")
    elif self.tok.type == token.TokenTypes.and_:
      self.advance()
      value = id(self.arg(True))
    else:
      raise Exception("Illegal argument")
    if type(value) != str and str(value) == "True":
      value = 1
    elif type(value) != str and str(value) == "False":
      value = 0
    """elif type(value) == list and not ret_list:
      string = "["
      for i in value:
        if type(i) == str:
          string += f"'{i}' "
        else:
          string += f"{i} "
      value = string + "\b]"
    elif type(value) == tuple and not ret_list:
      string = "("
      for i in value:
        if type(i) == str:
          string += f"'{i}' "
        else:
          string += str(i)
      value = string + "\b)"""
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
    in_string = False
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
          temp = self.arg(True)
          temp.replace("\"", "\\\"").replace("\"", "\\'")
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
    global arg, local_vars
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
        elif self.tok.value.lower() == "global" and self.class_:
          self.advance()
          name = self.tok.value
          self.advance()
          if self.tok is None or self.tok.type == token.TokenTypes.semi:
            value = ""
          elif self.tok.type == token.TokenTypes.equal:
            self.advance()
            value = self.arg(True)
            self.advance() if self.tok is not None and self.tok.type in (token.TokenTypes.dquote, token.TokenTypes.squote) else print(end="")
          if self.tok is not None and self.tok.type != token.TokenTypes.semi:
            raise Exception("No ; or EOL")
          if self.tok is not None:
            self.advance()
          self.classglobals.add(name, value)
        elif self.tok.value.lower() == "local" and self.class_ is True:
          self.advance()
          name = self.tok.value
          self.advance()
          if self.tok is None or self.tok.type == token.TokenTypes.semi:
            value = ""
          elif self.tok.type == token.TokenTypes.equal:
            self.advance()
            value = self.arg(True)
            self.advance() if self.tok.type in (token.TokenTypes.dquote, token.TokenTypes.squote) else print(end="")
          if self.tok is not None and self.tok.type != token.TokenTypes.semi:
            raise Exception("No ; or EOL")
          if self.tok is not None:
            self.advance()
          self.classlocals.add(name, value)
        elif self.tok.value.lower() == "global":
          self.advance()
          name = self.tok.value
          self.advance()
          if self.tok is None or self.tok.type == token.TokenTypes.semi:
            value = ""
          elif self.tok.type == token.TokenTypes.equal:
            self.advance()
            value = self.arg(True)
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
            value = self.arg(True)
            self.advance() if self.tok.type in (token.TokenTypes.dquote, token.TokenTypes.squote) else print(end="")
          if self.tok is not None and self.tok.type != token.TokenTypes.semi:
            raise Exception("No ; or EOL")
          if self.tok is not None:
            self.advance()
          local_vars.add(name, value)
        elif self.tok.value.lower() == "local":
          raise Exception("Local outside of function")
        elif self.tok.value.lower() == "static":
          self.advance()
          name = self.tok.value
          self.advance()
          if self.tok is None or self.tok.type == token.TokenTypes.semi:
            value = ""
          elif self.tok.type == token.TokenTypes.equal:
            self.advance()
            value = self.arg(True)
            self.advance() if self.tok is not None and self.tok.type in (token.TokenTypes.dquote, token.TokenTypes.squote) else print(end="")
          if self.tok is not None and self.tok.type != token.TokenTypes.semi:
            raise Exception("No ; or EOL")
          if self.tok is not None:
            self.advance()
          static_vars.add(name, value)
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
              except AttributeError:
                try:
                  global_vars[name] = "".join(list(global_vars[name]).insert(index, a))
                except IndexError:
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
          elif self.tok.type == token.TokenTypes.plus:
            self.advance()
            if self.tok.type == token.TokenTypes.equal:
              self.advance()
              local_vars[name] += self.arg()
            else:
              raise Exception("After + expected =")
          elif self.tok.type == token.TokenTypes.minus:
            self.advance()
            if self.tok.type == token.TokenTypes.equal:
              self.advance()
              local_vars[name] -= self.arg()
            else:
              raise Exception("After - expected =")
          elif self.tok.type == token.TokenTypes.multiply:
            self.advance()
            if self.tok.type == token.TokenTypes.equal:
              self.advance()
              local_vars[name] *= self.arg()
            else:
              raise Exception("After * expected =")
          elif self.tok.type == token.TokenTypes.divide:
            self.advance()
            if self.tok.type == token.TokenTypes.equal:
              self.advance()
              local_vars[name] /= self.arg()
            else:
              raise Exception("After / expected =")
          elif self.tok.type == token.TokenTypes.and_:
            self.advance()
            if self.tok.type == token.TokenTypes.equal:
              self.advance()
              local_vars[name] &= self.arg()
            else:
              raise Exception("After & expected =")
          elif self.tok.type == token.TokenTypes.or_:
            self.advance()
            if self.tok.type == token.TokenTypes.equal:
              self.advance()
              local_vars[name] |= self.arg()
            else:
              raise Exception("After | expected =")
          elif self.tok.type == token.TokenTypes.xor:
            self.advance()
            if self.tok.type == token.TokenTypes.equal:
              self.advance()
              local_vars[name] ^= self.arg()
            else:
              raise Exception("After ^ expected =")
          if self.tok is not None and self.tok.type != token.TokenTypes.semi:
            raise Exception("Expected EOL")
          if self.tok is not None:
            self.advance()
        elif self.tok.value == "integer":
          self.advance()
          name = self.tok.value
          self.advance()
          if self.tok.type != token.TokenTypes.equal:
            raise Exception("Expected = in integer decleration")
          self.advance()
          tempvalue = self.arg()
          if type(tempvalue) != int:
            raise Exception("Non-integer value assigned to int!")
          global_vars.add(name, tempvalue)
          if self.tok is not None and self.tok.type != token.TokenTypes.semi:
            raise Exception("Expected EOL")
          if self.tok is not None:
            self.advance()
        elif self.tok.value == "string":
          self.advance()
          name = self.tok.value
          self.advance()
          if self.tok.type != token.TokenTypes.equal:
            raise Exception("Expected = in string decleration")
          self.advance()
          tempvalue = self.arg()
          if type(tempvalue) != str:
            raise Exception("Non-string value assigned to str!")
          global_vars.add(name, tempvalue)
          if self.tok is not None and self.tok.type != token.TokenTypes.semi:
            raise Exception("Expected EOL")
          if self.tok is not None:
            self.advance()
        elif self.tok.value == "float":
          self.advance()
          name = self.tok.value
          self.advance()
          if self.tok.type != token.TokenTypes.equal:
            raise Exception("Expected = in float decleration")
          self.advance()
          tempvalue = self.arg()
          if type(tempvalue) != float:
            raise Exception("Non-float value assigned to float!")
          global_vars.add(name, tempvalue)
          if self.tok is not None and self.tok.type != token.TokenTypes.semi:
            raise Exception("Expected EOL")
          if self.tok is not None:
            self.advance()
        elif self.tok.value == "list":
          self.advance()
          name = self.tok.value
          self.advance()
          if self.tok.type != token.TokenTypes.equal:
            raise Exception("Expected = in integer decleration")
          self.advance()
          tempvalue = self.arg(True)
          if type(tempvalue) != list:
            raise Exception("Non-list value assigned to list!")
          global_vars.add(name, tempvalue)
          if self.tok is not None and self.tok.type != token.TokenTypes.semi:
            raise Exception("Expected EOL")
          if self.tok is not None:
            self.advance()
        elif self.tok.value in self.classglobals:
          name = self.tok.value
          self.advance()
          if self.tok.type == token.TokenTypes.equal:
            self.advance()
            self.classglobals[name] = self.arg()
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
              self.classglobals[name][index] = a
            except:
              try:
                self.classglobals[name].insert(index, a)
              except AttributeError:
                try:
                  self.classglobals[name] = "".join(list(self.classglobals[name]).insert(index, a))
                except IndexError:
                  self.classglobals[name] += str(a)
          elif self.tok.type == token.TokenTypes.plus:
            self.advance()
            if self.tok.type == token.TokenTypes.equal:
              self.advance()
              self.classglobals[name] += self.arg()
            else:
              raise Exception("After + expected =")
          elif self.tok.type == token.TokenTypes.minus:
            self.advance()
            if self.tok.type == token.TokenTypes.equal:
              self.advance()
              self.classglobals[name] -= self.arg()
            else:
              raise Exception("After - expected =")
          elif self.tok.type == token.TokenTypes.multiply:
            self.advance()
            if self.tok.type == token.TokenTypes.equal:
              self.advance()
              self.classglobals[name] *= self.arg()
            else:
              raise Exception("After * expected =")
          elif self.tok.type == token.TokenTypes.divide:
            self.advance()
            if self.tok.type == token.TokenTypes.equal:
              self.advance()
              self.classglobals[name] /= self.arg()
            else:
              raise Exception("After / expected =")
          elif self.tok.type == token.TokenTypes.and_:
            self.advance()
            if self.tok.type == token.TokenTypes.equal:
              self.advance()
              self.classglobals[name] &= self.arg()
            else:
              raise Exception("After & expected =")
          elif self.tok.type == token.TokenTypes.or_:
            self.advance()
            if self.tok.type == token.TokenTypes.equal:
              self.advance()
              self.classglobals[name] |= self.arg()
            else:
              raise Exception("After | expected =")
          elif self.tok.type == token.TokenTypes.xor:
            self.advance()
            if self.tok.type == token.TokenTypes.equal:
              self.advance()
              self.classglobals[name] ^= self.arg()
            else:
              raise Exception("After ^ expected =")
          if self.tok is not None and self.tok.type != token.TokenTypes.semi:
            raise Exception("Expected EOL")
          if self.tok is not None:
            self.advance()
        elif self.tok.value in self.classlocals:
          name = self.tok.value
          self.advance()
          if self.tok.type == token.TokenTypes.equal:
            self.advance()
            self.classlocals[name] = self.arg()
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
              self.classlocals[name][index] = a
            except:
              try:
                self.classlocals[name].insert(index, a)
              except AttributeError:
                try:
                  self.classlocals[name] = "".join(list(self.classlocals[name]).insert(index, a))
                except IndexError:
                  self.classlocals[name] += str(a)
          elif self.tok.type == token.TokenTypes.plus:
            self.advance()
            if self.tok.type == token.TokenTypes.equal:
              self.advance()
              self.classlocals[name] += self.arg()
            else:
              raise Exception("After + expected =")
          elif self.tok.type == token.TokenTypes.minus:
            self.advance()
            if self.tok.type == token.TokenTypes.equal:
              self.advance()
              self.classlocals[name] -= self.arg()
            else:
              raise Exception("After - expected =")
          elif self.tok.type == token.TokenTypes.multiply:
            self.advance()
            if self.tok.type == token.TokenTypes.equal:
              self.advance()
              self.classlocals[name] *= self.arg()
            else:
              raise Exception("After * expected =")
          elif self.tok.type == token.TokenTypes.divide:
            self.advance()
            if self.tok.type == token.TokenTypes.equal:
              self.advance()
              self.classlocals[name] /= self.arg()
            else:
              raise Exception("After / expected =")
          elif self.tok.type == token.TokenTypes.and_:
            self.advance()
            if self.tok.type == token.TokenTypes.equal:
              self.advance()
              self.classlocals[name] &= self.arg()
            else:
              raise Exception("After & expected =")
          elif self.tok.type == token.TokenTypes.or_:
            self.advance()
            if self.tok.type == token.TokenTypes.equal:
              self.advance()
              self.classlocals[name] |= self.arg()
            else:
              raise Exception("After | expected =")
          elif self.tok.type == token.TokenTypes.xor:
            self.advance()
            if self.tok.type == token.TokenTypes.equal:
              self.advance()
              self.classlocals[name] ^= self.arg()
            else:
              raise Exception("After ^ expected =")
          if self.tok is not None and self.tok.type != token.TokenTypes.semi:
            raise Exception("Expected EOL")
          if self.tok is not None:
            self.advance()
        elif self.tok.value == "alias":
          self.advance()
          if self.tok.value != None and self.tok.value == "function":
            self.advance()
            new_name = self.tok.value
            self.advance()
            try:
              function.add(new_name, function[self.tok.value])
              arg.add(new_name, arg[self.tok.value])
            except KeyError:
              raise Exception("Tried to alias a non-existant function")
            self.advance()
          elif self.tok.value != None and self.tok.value == "global":
            self.advance()
            new_name = self.tok.value
            self.advance()
            try:
              global_vars[new_name] = global_vars[self.tok.value]
            except KeyError:
              raise Exception("Tried to alias a non-existant global variable")
            self.advance()
          elif self.tok.value != None and self.tok.value == "local":
            self.advance()
            new_name = self.tok.value
            self.advance()
            try:
              local_vars[new_name] = local_vars[self.tok.value]
            except KeyError:
              raise Exception("Tried to alias a non-existant local variable")
            self.advance()
          else:
            raise Exception("Unexpected specifier to alias")
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
            try:
              interpreter(toks).interpret()
            except IllegalBreak:
              break
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
            if self.tok.value in ends:
              e = self.ends_in_func()
              for i in e:
                toks.append(i)
            else:
              toks.append(self.tok)
              self.advance()
          self.advance()
          while not a:
            try:
              interpreter(toks).interpret()
            except IllegalBreak:
              break
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
          temp_vars = copy(local_vars)
          local_vars = dictionary()
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
              if i == "mulargs":
                value = []
                while self.tok.type != token.TokenTypes.semi:
                  value.append(self.arg())
                self.advance()
              else:
                value = self.arg()
            local_vars.add(i, value)
          try:
            interpreter(function[funcname], True).interpret()
          except FunctionReturn:
            pass
          local_vars = temp_vars
          try:
            times = int(funcname.split("_")[0][1:])
            if funcname.split("_")[0][0] != "U":
              raise Exception("")
            if funcname not in limited_funcs:
              limited_funcs.add(funcname, times - 1)
            else:
              limited_funcs[funcname] -= 1
            if not limited_funcs[funcname]:
              function.remove(funcname)
              argvars.remove(funcname)
          except:
            pass
          if self.tok is not None and self.tok.type != token.TokenTypes.semi:
            raise Exception("Expected ; or EOL")
          if self.tok is not None and self.tok.type == token.TokenTypes.semi:
            self.advance()
        elif self.class_ and self.tok.value in class_funcs[self.classname]:
          funcname = self.tok.value
          self.advance()
          for i in arg[funcname]:
            value = ""
            if i == "mulargs":
              value = []
              while self.tok.type != token.TokenTypes.semi:
                value.append(self.arg(ret_list=True))
            else:
              value = self.arg(ret_list=True)
            local_vars.add(i, value)
          try:
            a = interpreter(class_funcs[self.classname][funcname], return_val=True, class_=True, classname=self.classname)
            a.classglobals = self.classglobals
            a.classlocals = self.classlocals
            a.interpret()
            self.classglobals = a.classglobals
            self.classlocals = a.classlocals
          except FunctionReturn as f:
            value = f.args[0]
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
        elif self.tok.value == "seed":
          self.advance()
          value = random.seed(self.arg())
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
          iterobj = self.arg(True)
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
          if self.return_val:
            return_ = self.arg()
            if self.tok is not None and self.tok.type !=  self.tok.type != token.TokenTypes.semi:
              raise Exception("Expected ; or EOL")
            if self.tok is not None:
              self.advance()
            raise FunctionReturn(return_)
          else:
            name = self.tok.value
            globalv = True if argvars[name][0] == "global" else   False
            name = argvars[name][1]
            self.advance()
            val = self.arg()
            if not globalv:
              local_vars[name] = val
            else:
              global_vars[name] = val
            self.advance()
            if self.tok is not None and self.tok.type !=  self.tok.type != token.TokenTypes.semi:
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
          exec(x)
          if self.tok is not None and self.tok.type != self.tok.type != token.TokenTypes.semi:
            raise Exception("Expected ; or EOL")
          if self.tok is not None:
            self.advance()
        elif self.tok.value == "qstr":
          self.advance()
          arg = self.arg()
          tokens = lexer.lexer(arg).generate_tokens()
          interpreter(tokens).interpret()
          if self.tok is not None and self.tok.type != self.tok.type != token.TokenTypes.semi:
            raise Exception("Expected ; or EOL")
          if self.tok is not None:
            self.advance()
        else:
          if debug:
            print(self.classname)
            print(class_funcs[self.classname])
          raise Exception(f"Illegal function {self.tok.value}")
      elif self.tok.type == token.TokenTypes.underscore:
        self.advance()
        func_name = self.tok.value
        self.advance()
        if func_name.split(":")[0] in constructors:
          classname = func_name.split(":")[0]
          try:
            func_name = func_name.split(":")[1]
          except IndexError:
            raise Exception("Function name cannot share class name")
          args = []
          toks = []
          while self.tok.type != token.TokenTypes.semi:
            args.append(self.tok.value)
            self.advance()
          arg.add(func_name, args)
          self.advance()
          while self.tok is not None and self.tok.value !=  "end":
            if self.tok.value in ends:
              e = self.ends_in_func()
              for i in e:
                toks.append(i)
            else:
              toks.append(self.tok)
              self.advance()
          self.advance() if self.tok is not None and  self.tok.value == "end" else print(end="")
          self.advance() if self.tok is not None and  self.tok.value == "end" else print(end="")
          try:
            class_funcs[classname].add(func_name, toks)
          except KeyError:
            class_funcs[classname] = dictionary()
            class_funcs[classname].add(func_name, toks)
        else:
          args = []
          toks = []
          while self.tok.type != token.TokenTypes.semi:
            args.append(self.tok.value)
            self.advance()
          arg.add(func_name, args)
          self.advance()
          while self.tok is not None and self.tok.value !=  "end":
            if self.tok.value in ends:
              e = self.ends_in_func()
              for i in e:
                toks.append(i)
            else:
              toks.append(self.tok)
              self.advance()
          self.advance() if self.tok is not None and  self.tok.value == "end" else print(end="")
          self.advance() if self.tok is not None and  self.tok.value == "end" else print(end="")
          function.add(func_name, toks)
      elif self.tok.type == token.TokenTypes.multiply:
        self.advance()
        class_name = self.tok.value
        self.advance()
        args = []
        toks = []
        while self.tok.type != token.TokenTypes.semi:
          args.append(self.tok.value)
          self.advance()
        self.advance()
        while self.tok is not None and self.tok.value != "end":
          if self.tok.value in ends:
            e = self.ends_in_func()
            for i in e:
              toks.append(i)
          else:
            toks.append(self.tok)
            self.advance()
        self.advance()
        self.advance() if self.tok is not None and self.tok.value == "end" else print(end="")
        constructors.add(class_name, toks)
        arg.add(class_name, args)
      elif self.tok.type in (token.TokenTypes.squote, token.TokenTypes.dquote):
        self.advance()
        self.advance()
        self.advance()
      else:
        if debug:
          print(self.tok)
        raise Exception("Illegal token")
