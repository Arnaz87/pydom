import re

class Parser():
  def __init__(self, inp = ""):
    self.pos = 0
    self.input = inp

  def char(self):
    return self.input[self.pos]

  def next_char(self):
    return self.input[self.pos + 1]

  def consume_char(self):
    self.pos += 1
    return self.input[self.pos-1]

  def starts_with(self, query):
    return self.input.startswith(query, self.pos)

  def eof(self):
    return self.pos >= len(self.input)

  def consume_while(self, test):
    result = ""
    while not self.eof() and test(self.char()):
      result += self.consume_char()
    return result

  def consume_space(self):
    return self.consume_while(lambda c: c in (" ", "\n", "\t", "\r"))

  def consume_pattern(self, pattern):
    return self.consume_while(lambda c: bool(re.match(pattern, c)))
