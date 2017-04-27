import argparse
import os

letters = ["A", "B", "C", "D", "E", "F",
   "G", "H", "I", "J", "K", "L",
   "M", "N", "O", "P", "Q", "R", 
   "S", "T", "U", "V", "W", "X", 
   "Y", "Z"] 

digits = ["0", "1", "2", "3", "4", 
  "5", "6", "7", "8", "9"]

tf = {0: {"letter": 1, "space": 0, "e": 1, "quotation": 3, "equals": 5, "plus": 6, 
          "minus": 7, "mult":8, "slash":11, "modulo": 12, "lparen": 13, 
          "rparen": 14, "comma": 15, "semicolon": 16, "eof": 17, "dot": 26,
          "other": 0, "nl":0, "digit": 18},
      # Identifier
      1: {"letter": 1, "e": 1, "digit": 1, "space": 2, "equals": 2, "nl":2, 
          "lparen": 2, "rparen": 2, "semicolon": 2, "eof": 2, "dot": 2,
          "slash": 2, "modulo": 2, "mult": 2, "plus": 2, "minus": 2, "comma":2,
          "error": 2},
      # String
      3: {"letter": 3, "e": 3, "digit": 3, "space": 3, "nl":3, 
          "dot": 3, "lparen": 3, "rparen": 3, "slash": 3, "modulo": 3, 
          "plus": 3, "minus": 3, "equal": 3, "comma": 3,
          "semicolon": 3, "mult": 3, "other":3, "quotation": 4,
          "error": 3}, 
      # Multiply
      8: {"letter": 9, "e": 9, "digit": 9, "space": 9, "lparen": 9, "rparen": 9, 
          "mult": 10, "error": 2},      
      # Slash
      11: {"letter": 23, "e": 23, "digit": 23, "space": 23, "lparen": 23, 
           "rparen": 23, "slash": 24, "error": 2},
      # Comment
      24: {"letter": 24, "e": 24, "digit": 24, "other": 24, "eof": 24,
          "dot": 24, "lparen": 24, "rparen": 24, "modulo": 24, "space": 24,
          "plus": 24, "minus": 24, "equal": 24, "quotation": 24, "comma": 24,
          "semicolon": 24, "eof": 24, "mult": 24, "slash": 24, "nl":25},
      # Digit
      18: {"digit": 18, "dot": 26, "e": 20, "space": 22, "nl":22, "lparen": 22, 
           "rparen": 22, "slash": 22, "modulo": 22, "plus": 22, "mult": 22,
           "minus": 22, "equal": 22, "comma": 22, "semicolon": 22, 
           "eof": 22, "error": 1},
      # Digit with no dot after
      19: {"digit": 19, "e": 20, "space":22, "nl":22, "lparen": 22, "rparen": 22, 
           "slash": 22, "modulo": 22, "mult": 22, "plus": 22, "minus": 22, 
           "equals": 22, "comma": 22, "semicolon": 22, "eof": 22, "error": 1},
      # Exponent
      20: {"plus": 21, "minus": 21, "digit": 21, "error": 1}, 
      # Digit after exponent
      21: {"digit": 21, "e": 22, "space":22, "nl":22, "lparen": 22, "rparen": 22, 
           "slash": 22, "modulo": 22, "plus": 22, "minus": 22, 
           "equal": 22, "quotation": 22, "comma": 22,
           "semicolon": 22, "eof": 22, "mult": 22, "error": 1},
      26: {"digit": 19, "error":1}
     }

accept_states = {2: "IDENT", 4: "STRING", 5: "EQUALS", 6: "PLUS", 7: "MINUS", 9: "MULT", 
                 10: "EXP", 23:"DIVIDE", 12: "MODULO", 13: "LPAREN", 14: "RPAREN", 15: "COMMA",
                 16: "SEMICOLON", 17: "EOF", 22: "DIGIT", 25: "COMMENT"}

errors = {1: "Badly-formed number", 2: "Illegal Character", 3: "Unterminated String"}

class LexAnalyzer:
    def __init__(self, text=None, fn=None):
        if fn != None:
            self.input = open(fn).read()
        else:
            self.input = text
        self.position = 0
        self.token = self.input[self.position]
        
        self.err_flag = False
        self.start_state = 0
        self.current_state = 0

    def setState(self, state):
        self.current_state = state   
        
    def getNextToken(self):
        if self.position == len(self.input) -1:
            self.token = '$' # end of string marker
        else:
            self.position += 1
            self.token = self.input[self.position]
        
    def check_token_type(self, token):
        token_type_dict = {'"': "quotation", "=": "equals", "+": "plus", "-": "minus",
                           "*": "mult", "/": "slash", "%": "modulo", "(": "lparen",
                           ")": "rparen", ",": "comma", ";": "semicolon", "$": "eof", ".": "dot", 
                           " ": "space", "\n": "nl"}
        
        if token == "E":
            return "e"
        elif token in letters:
            return "letter"
        elif token in digits:
            return "digit"
        elif token in token_type_dict.keys():
            return token_type_dict[token]
        else:
            return "other"
        
def main():

    parser = argparse.ArgumentParser(description="Lexical Analysis for an input file.")
    parser.add_argument("filename", metavar='fn', type=str, help="Input filename to analyze.")

    args = parser.parse_args()
    
    if args.filename is not None:
      la = LexAnalyzer(fn=args.filename)
    else:
      print("Please input either filename or text to analyze. Enter 'python proj1.py -h' for help")

    lexeme = ""
    
    print("=====================================")
    print("INPUT")
    print("=====================================")
    print("{}\n\nLength: {}\n".format(la.input, len(la.input)))

    print("=====================================")
    print("TOKEN | LEXEME")
    print("=====================================")
    
    while True:
        # Check token type
        token_type = la.check_token_type(la.token)
        
        # Match to tf, update state  
        
        if token_type in tf[la.current_state].keys():
            la.setState(tf[la.current_state][token_type])
        else:
            print("Current State: {}. Token not recognized: {}".format(la.current_state, token_type))
            print("ERROR: {}".format(errors[tf[la.current_state]["error"]]))
            break
        
        # When state not start state, start saving lexeme
        if la.current_state != la.start_state:
            lexeme += la.token
        
        # If state in accept state, print TOKEN and saved LEXEME, then clear lexeme var and return to start state
        if la.current_state in accept_states.keys():
            if la.current_state in [2, 9, 22, 23, 25]: # those with other required before accepting state
                print("{}: {}".format(accept_states[la.current_state], lexeme[:-1]))
                la.position -= 1
            else:
                print("{}: {}".format(accept_states[la.current_state], lexeme))
            
            lexeme = ""
            la.setState(la.start_state)
            
        # Break loop if eof detected, else get next token and continue
        if la.token == "$":
            break
        else: 
            la.getNextToken()  
         
main()