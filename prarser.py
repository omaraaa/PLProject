#hello



def getTests():
  found=True;
  i=1;
  while found:
    try:
      f = open(str(i)+".txt");
    except FileNotFoundError:
      return;
    yield f;
    i+=1;

t = getTests();

for f in t:
  s = f.read();
  print(s);