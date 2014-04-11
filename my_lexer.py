import ply.lex as lex

class MyLexer:

    reserved={'print':'PRINT','if':'IF', 'then':'THEN','else':'ELSE','while':'WHILE','do':'DO','input':'INPUT','new':'NEW','for':'FOR',
              'true':'TRUE','false':'FALSE','new':'NEW','int':'INT','bool':'BOOL','void':'VOID','return':'RETURN','class':'CLASS'};

    tokens=['EQUALS',
            'ID',
            'NUMBER',
            'PLUS',
            'MINUS',
            'MULT',
            'DIVIDE',
            'MOD',
            'AND',
            'OR',
            'ISEQUAL',
            'NOTEQUAL',
            'LESSTHAN',
            'LESSOREQUAL',
            'GREATERTHAN',
            'GREATEROREQUAL',
            'NOT',
            'LPAREN',
            'RPAREN',
            'LBRACE',
            'RBRACE',
            'SCOLON',
            'INCREMENT',
            'DECREMENT',
            'LBRACKET',
            'RBRACKET',
            'COMMA',
            'DOT']+list(reserved.values());

    #Regular Expressions rules
    t_PLUS=r'\+';
    t_MINUS=r'-';
    t_MULT=r'\*';
    t_DIVIDE=r'/';
    t_MOD=r'%';
    t_AND=r'&&';
    t_OR=r'\|\|';
    #Error with OR ?
    t_ISEQUAL=r'==';
    t_NOTEQUAL=r'!=';
    t_LESSTHAN=r'<';
    t_LESSOREQUAL=r'<=';
    t_GREATERTHAN=r'>';
    t_GREATEROREQUAL=r'>=';
    t_NOT=r'!';
    t_LPAREN=r'\(';
    t_RPAREN=r'\)';
    t_LBRACE=r'{';
    t_RBRACE=r'}';
    t_EQUALS=r'=';
    t_SCOLON=r'\;';
    t_INCREMENT=r'\+\+';
    t_DECREMENT=r'--';
    t_LBRACKET=r'\[';
    t_RBRACKET=r'\]';
    t_COMMA=r'\,';
    t_DOT=r'\.';

    t_ignore=" \t";

    def t_comment(self,t):
        r'//.*'
        t.lexer.lineno += t.value.count('\n')

    def t_ID(self,t):
        r'[a-zA-Z_][a-zA-Z0-9_]*';
        t.type=self.reserved.get(t.value,'ID');
        return t;
    
    def t_NUMBER(self,t):
        r'\d+';
        try:
            t.value=int(t.value);
        except ValueError:
            print("Integer value too large %d",t.value);
            t.value=0;
        return t;


    def t_newline(self,t):
        r'\n+';
        t.lexer.lineno += len(t.value);
        #t.type='NEWLINE'
        #return t

    def t_error(self,t):
        print ("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1);

    def build(self):
        self.lexer=lex.lex(module=self);

    def test(self,data):
        self.lexer.input(data)
        while True:
            tok=self.lexer.token()
            if not tok: break
            print tok

            
