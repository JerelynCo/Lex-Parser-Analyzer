from lex import LexAnalyzer
from syn import SynAnalyzer

def main():
    la = LexAnalyzer(fn="/home/fassster/Documents/cs242/proj1/samples/files/prog1.txt")
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
        
        # check out transition matrix
        la.transition_state()
        
        # print pair if available
        if la.output_ready:
            pair = (la.token_str, la.lexeme)
            pairs.append(pair)
            if debug_print:
                print("{}: {}".format(pair[0], pair[1]))
            
            la.output_ready = False
            la.lexeme = ""

        # move to next token
        la.get_next_token() 
        
        # print success if error-free termination
        if la.terminate:
            print("\n=> LEXICAL ANALYSIS: ", end="")
            if la.err_flag:
                print("UNSUCCESSFUL\n")
            else:
                print("SUCCESSFUL\n")
            break
         
    # continue to syntax analysis if no error in lexical analysis  
    if not la.err_flag:
        sa = SynAnalyzer(lex_pairs=pairs)
        sa.set_next_pair()
        sa.S()

        # print(sa.variables)

        # print success if error-free termination
        print("\n=> SYNTAX ANALYSIS: ", end="")
        if sa.err_flag:
            print("UNSUCCESSFUL\n")
        else:
            print("SUCCESSFUL\n")        
main()