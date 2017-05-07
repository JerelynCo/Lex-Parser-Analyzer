
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
		int answer = S();
		System.out.println(answer);
	}
	
	// production: S -> E.
	public static int S()
	{
        int ans = E();
		if ( token == '.' && !errFlag )
			System.out.println( "string accepted" );
		else
			System.out.printf( "string not accepted (error on or before position %d)\n", position );
	    return ans;
	}

	// production: E->TA
	public static int E()
	{
			int x = T();
            int y = A();
			return x + y;
   }


	// productions: A->+TA|eps
	public static int A()
	{
		if ( token == '+' )
		{
			getNextToken();
			int x = T();
            int y = A();
			return x + y;
		}
		else
            return 0; // do nothing (eps)
	}

	// production: T->FB
	public static int T()
	{
 			int x = F();
            int y = B();
			return x*y;
	}

	// productions: B->*FB|eps
	public static int B()
	{
		if ( token == '*' )
		{
			getNextToken();
			int x = F();
            int y = B();
			return x*y;
		}
		else
            return 1; // do nothing (eps)
	}

	// productions: F->-X|X
	public static int F()
	{
		if ( token == '-' )
		{
			getNextToken();
			return -X();
		}
		else
            return X();
	}

	// productions: X->1|(E)
	public static int X()
	{
		int ans = 0;
		if ( token >= '0' && token <= '9')            
		{
			ans = token-'0';
			getNextToken();
            // that's it.
		}
		else if ( token == '(' )
                {        
                        getNextToken();    
                        ans = E();
                        if ( token == ')' )
                           getNextToken();
                        else
                           error( "X2" );
                        
                }
                else
                        error( "X1" );
		return ans;
	}
	
	public static void error( String from )
	{
		System.out.printf( "Parse error %s %d\n", from, position );
		errFlag = true;
	}
	
}