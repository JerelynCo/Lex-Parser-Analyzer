
// Recursive descent parser for the language of
// single-digit arithmetic expressions whose operands
// are just 1's.  adddition, multiplication, negation
// and parentheses are supported
// Usage:  java PlayWithOnes <input-string>

// Initial grammar:  S->E.  E->E+T|T  T->T*F|F  F->-X|X  X->1|(E)
// Equivalent LL(1) grammar:
//   S->E.  E->TA  A->+TA|eps  T->FB  B->*FB|eps
//   F->-X|X  X->1|(E)  

public class PlayWithOnes
{
	private static String input;
	private static char token;
	private static int position = 0;
	private static boolean errFlag = false;
	
	public static void getNextToken()
	{
		if ( position == input.length() )
		   token = '.';  // end of string marker
		else
			token = input.charAt(position++); 
	}
	
	public static void main( String args[] ) 
	{
		input = args[0];
		getNextToken();
		S();
	}
	
	// production: S -> E.
	public static void S()
	{
                E();
		if ( token == '.' && !errFlag )
			System.out.println( "string accepted" );
		else
			System.out.printf( "string not accepted (error on or before position %d)\n", position );
	}

	// production: E->TA
	public static void E()
	{
                T();
                A();
    }


	// productions: A->+TA|eps
	public static void A()
	{
		if ( token == '+' )
		{
			getNextToken();
			T();
            A();
		}
		else
            ; // do nothing (eps)
	}

	// production: T->FB
	public static void T()
	{
        F();
        B();
    }

	// productions: B->*FB|eps
	public static void B()
	{
		if ( token == '*' )
		{
			getNextToken();
			F();
            B();
		}
		else
            ; // do nothing (eps)
	}

	// productions: F->-X|X
	public static void F()
	{
		if ( token == '-' )
		{
			getNextToken();
			X();
		}
		else
            X();
	}

	// productions: X->1|(E)
	public static void X()
	{
		if ( token == '1' )            
		{
			getNextToken();
            // that's it.
		}
		else if ( token == '(' )
                {        
                        getNextToken();    
                        E();
                        if ( token == ')' )
                           getNextToken();
                        else
                           error( "X2" );
                        
                }
                else
                        error( "X1" );
	}
	
	public static void error( String from )
	{
		System.out.printf( "Parse error %s %d\n", from, position );
		errFlag = true;
	}
	
}