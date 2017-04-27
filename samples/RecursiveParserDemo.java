
// Recursive descent parser for the language of all strings of the form a^n b^n, where n > 0
// Usage:  java RecursiveParserDemo <input-string>

// Initial grammar:  S -> aSb | ab
// Equivalent LL(1) grammar:   S -> aA , A -> aAb | b

public class RecursiveParserDemo
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
		if ( token == '.' && !errFlag )
			System.out.println( "string accepted" );
		else
			System.out.printf( "string not accepted (error on or before position %d)\n", position );
	}
	
	// production: S -> aA
	public static void S()
	{
		if ( token == 'a' )
		{
			getNextToken();
			A();
		}
		else
			error( "S" );
	}

	// productions: A -> aAb | b
	public static void A()
	{
		if ( token == 'a' )
		{
			getNextToken();
			A();
			if ( token == 'b' )
				getNextToken();
			else
			    error( "A1" );
		}
		else if (token == 'b')
		{
			getNextToken();
		}
		else
		   error( "A2" );
	}
	
	public static void error( String from )
	{
		System.out.printf( "Parse error %s %d\n", from, position );
		errFlag = true;
	}
	
}