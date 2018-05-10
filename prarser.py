#hello

import string;

def getTests():
  found=True;
  i=1;
  while found:
    try:
      f = open(str(i)+".txt");
    except FileNotFoundError:
      return;
    yield (f, str(i)+".txt");
    i+=1;


t = getTests();
st= {};
line=1
col=1
errors = []
buff = "";
def lex(f):
  global st, errors, line, col;
  st = f
  errors = []
  line=1
  col=1
  buff = "";
  def n():
    global st;
    if not n:
      return False;
  def serr(e):
    global errors, line, col, buff;
    errors = errors + ["Error: {} \"{}\" at line:{} col:{}".format(e, buff, line, col)];
    buff = "";
  def nextchar(*t):
    global st, line, col;
    
    if not st:
      return False;

    while(st[0] == ' ' or st[0] == '\n'):
      col += 1
      if(st[0] == '\n'):
        line += 1
        col = 1
      st = st[1::]
      if not st:
        return False;
    #print(t, st[0:5]);
    for c in t:
      if not st:
        return False;
      if c == st[0]:
        col+=1
        st = st[1::]
        return True;

    return False;
  def gotochar(t):
    global st, line, col, buff;
    if not st:
      return False;
    while(st[0] != t):
      buff += st[0];
      col += 1
      if(st[0] == '\n'):
        line += 1
        col = 1
      st = st[1::]
      if not st:
        return False;

  def next(t):
    global st, line, col;
    if not st:
      return False;
    while(st[0] == ' ' or st[0] == '\n'):
      col += 1
      if(st[0] == '\n'):
        line += 1
        col = 1
      st = st[1::]
      if not st:
        return False;
    #print(t, st[0]);
    i = 0;
    while(i < len(t)):
      if not st:
        return False;
      #print(t[i], st[i]);
      if t[i] != st[i]:
          return False;
      i+=1;
    col += i
    st = st[i::];
    return True;

  def special():
    return nextchar("+", "-", "*", "/", "\\", "^", "~", ":", ".", "?", " ", "#", "$", "&");
  def character():
    if alphanum():
      return 1;
    if special():
      return 1;
    return False;
  def strng():
    if character():
      strng();
    else:
      return False;
    
    return 1;
  def digit():
    return nextchar(*[str(i) for i in range(0, 10)]);
  def numeral():
    if digit():
      numeral();
    else:
      return False;
    
    return 1;
  def uppercase():
    return nextchar(*(string.ascii_uppercase+"_"));
  def lowercase():
    return nextchar(*string.ascii_lowercase);

  def alphanum():
    if lowercase():
      return True;
    if uppercase():
      return True;
    if digit():
      return True;
    return False;

  def charlist():
    if alphanum():
      charlist();

  def variable():
    if uppercase():
      charlist();
      return 1;

  def small_atom():
    if lowercase():
      charlist();
      return True;

    return False;


  def atom():
    if small_atom():
      return True;
    if nextchar('\'') and strng() and nextchar('\''):
      return True;

    return False;

  def structure():
    if nextchar("(") and term_list() and nextchar(")"):
      return 1;
    return False;

  def term():
    if atom():
      structure()
      return 1;
    if variable():
      return 1;
    if numeral():
      return 1;
    return False;

  def term_list():
    if term():
      if(nextchar(',')):
        term_list();
      return True;
    return False;    

  def predicate():
    if atom():
      if nextchar("("):
        term_list();
        if not nextchar(")"):
          gotochar(")");
          serr("invalid term")
          nextchar(")");
      return 1;
    return False;
      

    

  def predicate_list():
    if not predicate():
      gotochar(",");
      serr("invalid predicate");

    if(nextchar(",")):
      predicate_list();

  def query():
    if(next("?- ")):
      predicate_list()
    else:
      serr("no query found")

    if not nextchar("."):
      serr("Query must end with .")

  def clause():
    if(not predicate()):
      return False;

    if(next(":-")):
      predicate_list();

    nextchar(".");
    return True;


  def clause_list():
    
    if(clause()):
      clause_list();

  def program():
    clause_list();
    query();

  program();
  if not errors:
    print("Correct");
  else:
    print("Syntax Error:",*errors, sep='\n')



####
for f, fn in t:
  s = f.read();
  print(fn)
  lex(s)
  print("");
####