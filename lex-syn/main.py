from lex import LexAnalyzer
from syn import SynAnalyzer

def main():
    la = LexAnalyzer(fn="/home/fassster/Documents/cs242/proj1/samples/files/prog3.txt")
    debug_print = True
    
    print("=====================================")
    print("INPUT (LENGTH: {})".format(len(la.input)))
    print("=====================================")
    print("{}\n".format(la.input))
    
    print("=====================================")
    print("RESULT")
    print("=====================================\n")
    
    if debug_print:
        print("TOKEN | LEXEME")
        print("---------------")
    
    # [(token, lexeme), (), ()]
    pairs = []
    while True:
        
        la.transitionState()
        
        if la.output_ready:
            pair = (la.token_str, la.lexeme)
            pairs.append(pair)
            if debug_print:
                print("{}: {}".format(pair[0], pair[1]))
            
            la.output_ready = False
            la.lexeme = ""
             
        la.getNextToken() 
        
        if la.terminate:
            if not la.err_flag:
                print("\n=> LEXICAL ANALYSIS: SUCCESSFUL\n")
            break
           
    if not la.err_flag:
        sa = SynAnalyzer(lex_pairs=pairs)
        sa.set_next_pair()
        sa.S()
        print(sa.variables)
        if not sa.err_flag:
            print("\n=> SYNTAX ANALYSIS: SUCCESSFUL\n")
        
main()