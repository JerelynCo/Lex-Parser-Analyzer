class SynAnalyzer:
    def __init__(self, lex_pairs=None):
        self.lex_pairs = lex_pairs
        self.position = -1;
        self.token = ""
        self.lexeme = ""
        self.variables = {}
        
        self.err_flag = False
        
        self.rel = ['<', '>', '<=', '>=', '==', '!=']
        self.E_ident = ["NUMBER", "IDENT", "LPAREN", "RPAREN", "SQRT"]
    
    def set_next_pair(self):
        if self.token == "EOF":
            print("End reached.")
        else:
            self.position = self.position + 1
            self.token = self.lex_pairs[self.position][0]
            self.lexeme = self.lex_pairs[self.position][1]
            
    def get_variable_value(self, var):
        dict_var = dict(self.variables)
        if var in dict_var.keys():
            return dict_var[var]
        return None
        
    def error(self, error_type, class_src):
        errors = {1: "Unexpected token", 2: "Inappropriate argument"}
        print("[{}] Error: {}; Token: {}; Lexeme: {}; Position: {}".format(class_src, errors[error_type], 
                                                               self.token, self.lexeme, self.position))
        self.err_flag = True
    
    def check_semicolon(self):
        if self.token != "SEMICOL":
            self.err_flag = True
            self.err_msg = "Missing semicolon"
            return False
        elif self.token == "SEMICOL" and self.token != "EOF":
            print("Done statement.")
            self.set_next_pair()
            self.S()
        return True
            
    # Production S -> IF(COND) E ; | IF(COND) S | PRINT(STRING) ; | PRINT(IDENT) ; | IDENT = E ;
    def S(self): 
        res = -1
        ans = None
        
        if self.token == "IF":
            self.set_next_pair()
            if self.token == "LPAREN":
                self.set_next_pair()
                if self.token in self.E_ident:
                    cond_res = self.COND() 
                    self.set_next_pair()
                    if self.token == "RPAREN":
                        self.set_next_pair()
                        if cond_res:
                            print("Condition met.", end=" ")
                            
                            # Handling expression
                            if self.token in self.E_ident:
                                ans = self.E()
                                print("Computation performed", ends=" ") 
                                self.set_next_pair()
                                if not self.check_semicolon():
                                    self.error(1, "S")
                                  
                            # Recurse to S
                            elif self.token in ["IF", "PRINT", "IDENT"]: # S identifiers
                                self.S()
                        else:
                            print("Condition not met.")
                    else:
                        self.error(1, "S")
                else:
                    self.error(1, "S")
            else:
                self.error(1, "S")
                
            return ans

        elif self.token == "PRINT":
            msg = ""
            self.set_next_pair()
            
            # check format (STRING) or (IDENT)
            if self.token == "LPAREN":
                self.set_next_pair()
                if self.token == "STRING":
                    msg = self.lexeme
                    
                elif self.token == "IDENT":
                    msg = self.get_variable_value(self.lexeme)
                    if msg is None:
                        self.error("undeclared variable")
                else:
                    self.error(2, "S")
                            
                
                self.set_next_pair()
                if self.token == "RPAREN":
                    self.set_next_pair()
                    if self.check_semicolon():
                        print("Output: ({})".format(msg))
                else:
                    self.error(1, "S")
            else:
                self.error(1, "S")
                
            return True
            
        elif self.token == "IDENT":
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
                        self.error(1, "S")
                else:
                    self.error(1, "S")
            else:
                self.error(1, "S")
                            
            return True
        
    # should return true or false
    def COND(self):
        return 0

    # Production E -> EA E' 
    # should return value
    def E(self):
        print("In E: Lexeme: {}".format(self.lexeme))
        x = self.EA()
        y = self.E_prime()
        print("In E: {}, {}".format(x,y))
        return x + y

    # Production E' -> + EA E' | - EA E' | epsilon
    def E_prime(self):
        print("In E_PRIME: Lexeme: {}".format(self.lexeme))
        if self.token == "PLUS":
            self.set_next_pair()
            x = self.EA()
            y = self.E_prime()
            print("In E_PRIME: {} + {}".format(x,y))
            return x + y
        elif self.token == "MINUS":
            self.set_next_pair()
            x = self.EA()
            y = self.E_prime()
            print("In E_PRIME: {} - {}".format(x,y))
            return -x + y
        else:
            return 0

    # Production EA -> EB EA' 
    def EA(self):
        x = self.EB()
        y = self.EA_prime()
        print("In EA: {}, {}".format(x,y))
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
        print(self.token)
        if self.token == "MINUS":
            self.set_next_pair()
            return -1*self.EC()
        else:
            return self.EC()
    
    # Production EC -> ED EC' 
    def EC(self):
        x = self.ED()
        y = self.EC_prime()
        print("In EC: {}, {}".format(x,y))
        return x ** y


    # Production EC' -> * * ED EC' | epsilon
    def EC_prime(self):
        if self.token == "EXP":
            self.set_next_pair()
            x = self.ED()
            y = self.EC_prime()
            print("{}, {}".format(x,y))
            return x * y
        else:
            return 1


    # Production ED -> NUMBER | IDENT | (E) | SQRT(E)
    def ED(self):
        if self.token == "NUMBER":
            val = int(self.lexeme)
            self.set_next_pair()
            return val
        elif self.token == "IDENT":
            val = get_variable_value(self.lexeme)
            self.set_next_pair()
            return val
        elif self.token == "LPAREN":
            self.set_next_pair()
            val = self.E()
            self.set_next_pair()
            if self.token == "RPAREN":
                self.set_next_pair()
                return val
            else:
                self.error(1, "ED")
        elif self.token == "SQRT":
            self.set_next_pair()
            if self.token == "LPAREN":
                self.set_next_pair()
                val = self.E()
                self.set_next_pair()
                if self.token == "RPAREN":
                    self.set_next_pair()
                    return val ** (0.5)
                else:
                    self.error(1, "ED")
            else:
                self.error(1, "ED")
        else:
            self.error(1, "ED")
        return False
