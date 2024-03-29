"""
**CFG**
S -> IF(COND) E; | IF(COND) S; | PRINT(STRING); | IDENT = E;
COND -> E REL E 
REL -> '<' | '>' | '<=' | '>=' | '==' | '!='

E -> E + EA | E - EA | EA 
EA -> EA * EB | EA / EB | EB
EB -> -EC | EC
EC -> EC * * ED | ED
ED -> NUMBER | IDENT | ( E ) | SQRT(E)

**LL1**
S -> IF(COND) E SEMICOL | IF(COND) S SEMICOL | PRINT(STRING) SEMICOL | PRINT(E) | IDENT = E SEMICOL

COND -> E REL E 
REL -> '<' | '>' | '<=' | '>=' | '==' | '!='

E -> EA E' 
E' -> + EA E' | - EA E' | epsilon
EA -> EB EA' 
EA' -> * EB EA' | / EB EA' | epsilon
EB -> -EC | EC
EC -> ED EC' 
EC' -> * * ED EC' | ED | epsilon
ED -> NUMBER | IDENT | ( E ) | SQRT(E)
"""

class SynAnalyzer:
    def __init__(self, lex_pairs=None):
        self.lex_pairs = lex_pairs
        self.position = -1;
        self.token = ""
        self.lexeme = ""
        self.variables = {}
        
        self.err_flag = False
        
        self.conds = ["GREATER", "LESSER", "EQUALS", "NOT"]
        self.E_ident = ["NUMBER", "IDENT", "LPAREN", "RPAREN", "SQRT"]
    

    def set_next_pair(self):
        """Similar to get_next_token in Lex"""
        if self.token == "EOF":
            print("End reached.")
        else:
            self.position = self.position + 1
            self.token = self.lex_pairs[self.position][0]
            self.lexeme = self.lex_pairs[self.position][1]
            
    def get_variable_value(self, var):
        """ Gets value from dictionary of variables declared in program"""
        dict_var = dict(self.variables)
        if var in dict_var.keys():
            try:
                return float(dict_var[var])
            except Exception as e:
                return dict_var[var]
        return 0

    def get_curr_lexeme(self):
        """ If token is identifier, it's a variable. If token is just number, return as is"""
        if self.token == "IDENT":
            return self.get_variable_value(self.lexeme)
        elif self.token == "NUMBER":
            return float(self.lexeme)
        error(1, "COND:Value neither variable nor number")
        
    def error(self, error_type, class_src):
        """ Classes of errors """ 
        errors = {1: "Unexpected token", 2: "Inappropriate argument", 3: "Invalid assignment", 
        4: "Undeclared variable"}
        print("[{}] Error: {}; Token: {}; Lexeme: {}; Position: {}".format(class_src, errors[error_type], 
                                                               self.token, self.lexeme, self.position))
        self.err_flag = True
    
    def check_semicolon(self):
        if self.token != "SEMICOL":
            self.err_flag = True
            self.err_msg = "Missing semicolon"
            return False
        elif self.token == "SEMICOL" and self.token != "EOF":
            self.set_next_pair()
            self.S()
        return True
            
    # Production S -> IF(COND) E ; | IF(COND) S | PRINT(STRING) ; | PRINT(E) ; | IDENT = E ;
    def S(self): 
        res = -1
        ans = None

        if self.token == "IF" and not self.err_flag:
            self.set_next_pair()
            if self.token == "LPAREN":
                self.set_next_pair()
                if self.token in self.E_ident:
                    # Get condition result
                    cond_res = self.COND() 
                    self.set_next_pair()
                    if self.token == "RPAREN":
                        self.set_next_pair()
                        if cond_res:
                            print("Condition met.", end=" ")
                            # Handling expression
                            if self.token in ["NUMBER", "LPAREN", "RPAREN", "SQRT"]:
                                ans = self.E()
                                print("Computation performed", ends=" ") 
                                self.set_next_pair()
                                if not self.check_semicolon():
                                    self.error(1, "S:IF:Missing semicolon")
                                  
                            # Recurse to S
                            elif self.token in ["IF", "PRINT", "IDENT"]: # S identifiers
                                self.S()
                        else:
                            print("Condition not met.")
                            #CONTINUE TO SEMICOLON
                            while self.token != "SEMICOL":
                                self.set_next_pair()
                            self.set_next_pair()
                            self.S()
                    else:
                        self.error(1, "S:IF:Missing right parenthesis")
                else:
                    self.error(1, "S:IF")
            else:
                self.error(1, "S:IF:Missing left parenthesis")
                
            return ans

        elif self.token == "PRINT" and not self.err_flag:
            msg = ""
            self.set_next_pair()
            
            # check format (STRING) or (IDENT)
            if self.token == "LPAREN":
                self.set_next_pair()
                if self.token == "STRING":
                    msg = self.lexeme
                    print("Output: ({})".format(msg))
                    self.set_next_pair()

                elif self.token in self.E_ident:
                    msg = self.E()
                    print("Output: ({})".format(msg))
                    if msg is None:
                        self.error(1, "S:PRINT:No string to print")

                else:
                    self.error(2, "S")
    
                if self.token == "RPAREN":
                    self.set_next_pair()
                    if not self.check_semicolon():
                        self.error(2, "S:PRINT:Missing semicolon")
                        
                else:
                    self.error(1, "S:PRINT:Missing right parenthesis")
            else:
                self.error(1, "S:PRINT:Missing left parenthesis")
                
            return True
            
        elif self.token == "IDENT" and not self.err_flag:
            var_name = self.lexeme
            self.set_next_pair()
            
            # Assignment procedure
            if self.token == 'EQUALS':  
                self.set_next_pair()
                if self.token in self.E_ident:
                    val = self.E()
                    self.variables[var_name] = val
                    print("Computation performed ({} = {})".format(var_name, val))
                    if not self.check_semicolon():
                        self.error(1, "S:IDENT:Missing semicolon")
                else:
                    self.error(1, "S:IDENT")
            else:
                self.error(1, "S:IDENT")
                            
            return True
        
    # Compares two variables and returns true or false
    def COND(self):
        var1_val = self.E()
        var2_val = None
        cond1 = None
        cond2 = None

        # self.set_next_pair()

        if self.token in self.conds:
            cond1 = self.token
            self.set_next_pair()

            if cond1 == "NOT":
                if self.token == "EQUALS":
                    cond2 = self.token
                    self.set_next_pair()
                    var2_val = self.get_curr_lexeme()
                else:
                    error(1, "COND:NOT:Not a condition")
            else:
                if self.token in self.conds:
                    cond2 = self.token
                    self.set_next_pair()
                    var2_val = self.get_curr_lexeme()
                elif self.token in ["NUMBER", "IDENT"]:
                    var2_val = self.get_curr_lexeme()

            if cond1 == "GREATER":
                if cond2 == "EQUALS":
                    return var1_val >= var2_val
                return var1_val > var2_val
            elif cond1 == "LESSER":
                if cond2 == "EQUALS":
                    return var1_val <= var2_val
                return var1_val < var2_val
            elif cond1 == "EQUALS":
                if cond2 == "EQUALS":
                    return var1_val == var2_val
                self.error(3, "COND")
            elif cond1 == "NOT":
                if cond2 == "EQUALS":
                    return var1_val != var2_val
                self.error(3, "COND")
            else:
                self.error(1, "COND")

        self.error(1, "COND")

    # Production E -> EA E'
    def E(self):
        # print("In E: Lexeme: {}".format(self.lexeme))
        x = self.EA()
        y = self.E_prime()
        # print("In E: {}, {}".format(x,y))
        return x + y

    # Production E' -> + EA E' | - EA E' | epsilon
    def E_prime(self):
        # print("In E_PRIME: Lexeme: {}".format(self.lexeme))
        if self.token == "PLUS":
            self.set_next_pair()
            x = self.EA()
            y = self.E_prime()
            # print("In E_PRIME: {} + {}".format(x,y))
            return x + y
        elif self.token == "MINUS":
            self.set_next_pair()
            x = self.EA()
            y = self.E_prime()
            # print("In E_PRIME: {} - {}".format(x,y))
            return -x + y
        else:
            return 0

    # Production EA -> EB EA' 
    def EA(self):
        x = self.EB()
        y = self.EA_prime()
        # print("In EA: {}, {}".format(x,y))
        return x * y
    
    # Production EA' -> * EB EA' | / EB EA' | epsilon
    def EA_prime(self):
        if self.token == "MULT":
            self.set_next_pair()
            x = self.EB()
            y = self.EA_prime()
            return x * y
        elif self.token == "DIVIDE":
            self.set_next_pair()
            x = self.EB()
            y = self.EA_prime()
            return 1/(x * y)
        else:
            return 1

    # Production EB -> -EC | EC
    def EB(self):
        # print(self.token)
        if self.token == "MINUS":
            self.set_next_pair()
            return -1*self.EC()
        else:returns true or false
            return self.EC()
    
    # Production EC -> ED EC'
    def EC(self):
        x = self.ED()
        y = self.EC_prime()
        # print("In EC: {}, {}".format(x,y))
        return x ** y

    # Production EC' -> * * ED EC' | epsilon
    def EC_prime(self):
        if self.token == "EXP":
            self.set_next_pair()
            x = self.ED()
            y = self.EC_prime()
            # print("{}, {}".format(x,y))
            return x * y
        else:
            return 1


    # Production ED -> NUMBER | IDENT | (E) | SQRT(E)
    def ED(self):
        if self.token == "NUMBER":
            val = float(self.lexeme)
            self.set_next_pair()
            return val
        elif self.token == "IDENT":
            val = self.get_variable_value(self.lexeme)
            self.set_next_pair()
            return val
        elif self.token == "LPAREN":
            self.set_next_pair()
            val = self.E()
            if self.token == "RPAREN":
                self.set_next_pair()
                return val
            else:
                self.error(1, "ED:Missing right parenthesis")
        elif self.token == "SQRT":
            self.set_next_pair()
            if self.token == "LPAREN":
                self.set_next_pair()
                val = self.E()
                if self.token == "RPAREN":
                    self.set_next_pair()
                    return val ** (0.5)
                else:
                    self.error(1, "ED:Missing right parenthesis")
            else:
                self.error(1, "ED:Missing left parenthesis")
        else:
            self.error(1, "ED")
        return False
