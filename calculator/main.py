from calculator.lexer import Lexer
from calculator.parser_ import Parser
from calculator.interpreter import Interpreter

#while True:
    #try:
        #text = input("calc > ")
        #lexer = Lexer(text)
        #tokens = lexer.generate_tokens()
        #parser = Parser(tokens)
        #tree = parser.parse()
        #if not tree: continue
        #interpreter = Interpreter()
        #value = interpreter.visit(tree)
        #print(value)
    #except Exception as e:
        #print(e)

def calculate_(calculator_input):
  text = calculator_input
  lexer = Lexer(text)
  tokens = lexer.generate_tokens()
  parser = Parser(tokens)
  tree = parser.parse()
  if not tree: 
    return "incorrect"
  interpreter = Interpreter()
  value = interpreter.visit(tree)
  return value
