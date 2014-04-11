import ply.yacc as yacc
from my_lexer import *
from ast_classes import *


class MyParser:
    lex=MyLexer();
    lex.build();
    tokens=lex.tokens
    
    precedence=(('nonassoc','GREATERTHAN','LESSTHAN','ISEQUAL','NOTEQUAL','LESSOREQUAL','GREATEROREQUAL'),
                ('left','PLUS','MINUS'),
                ('left','MULT','DIVIDE','MOD'),
                ('right','UMINUS'),
                ('right','NOT'));

    decList={};    
    scopeList={};
    fscope=0;
    scope=0;
    var_type="";
    isArray=False;
    f_ret="";
    dList=[];
    
    def p_error(self,p):
        print('Syntax error %s' %p);
        exit(1);

    def p_pgm_start(self,p):
        'pgm : DeclSeq'
        p[0]= p[1];


    def p_declSeq(self,p):
        'DeclSeq : Decl DeclSeq'
        if p[2]==None and p[1]!=None:
            p[0]=DECL(p[1]);
        elif p[2]!=None and p[1]!=None:
            p[0]=DECLSEQ(p[1],p[2]);
        elif p[1]==None and p[2]!=None:
            p[0]=DECL(p[2]);

    def p_declSeq_empty(self,p):
        'DeclSeq : empty'
        p[0]=None;

    def p_empty(self,p):
        'empty : '
        pass;

    def p_decl_vardecl(self,p):
        'Decl : VarDecl'
        p[0]=p[1];

    def p_ext_vardecl(self,p):
        'Extension : VarDecl'
        p[0]=p[1];

    def p_ext_vardecl_seq(self,p):
        'Extension : VarDecl Extension'
        if p[2]==None:
            p[0]=p[1];
        else:
            p[0]=STMTSEQ(p[1],p[2]);
            
    def p_ext_stmt(self,p):
        'Extension : stmtSeq'
        p[0]=p[1];

    def p_decl_func(self,p):
        'Decl : FunDecl'
        p[0]=p[1];

    def p_decl_obj(self,p):
        'Decl : ClassDecl'
        p[0]=p[1];

    def p_vardecl(self,p):
        'VarDecl : Type VarList SCOLON'
        p[0]=p[2];

    def p_stmt_seq(self,p):
        'stmtSeq : stmt stmtSeq'
        if (p[2]!=None):
            p[0]=STMTSEQ(p[1],p[2]);

        else:
            p[0]=STMT(p[1]);

    def p_stmt_seq_empty(self,p):
        'stmtSeq : empty'
        pass


    def p_type_int(self,p):
        'Type : INT'
        self.var_type=p[1];
        p[0]=p[1];


    def p_type_bool(self,p):
        'Type : BOOL'
        self.var_type=p[1];
        p[0]=p[1];


    def p_type_id(self,p):
        'Type : ID'
        if self.decList.has_key(p[1]):
            x=self.decList[p[1]];
            if isinstance(x,OBJECTDECL):
                self.var_type=p[1];
                p[0]=p[1];
            else:
                print "Object not recognised"
                exit(1);
        else:
            print "Object not defined"
            exit(1);
    
    """def p_type_array(self,p):
        'Type : Type LBRACKET RBRACKET'
        self.var_type=("array",p[1]);
        p[0]=("array",p[1]);
        self.isArray=True;"""


    def p_type_void(self,p):
        'Type : VOID'
        self.var_type=p[1];
        p[0]=p[1];
        

    def p_varlist(self,p):
        'VarList : Var COMMA VarList'
        p[0]=VARLISTSQ(p[1],p[3]);

    def p_varlist_var(self,p):
        'VarList : Var'
        p[0]=VARLIST(p[1]);
        print p[1];

    def p_var(self,p):
        'Var : ID DimStar'
        x=None;
        if(p[2]==None):
            if(self.scope==1):
                x=self.var_helper(p[1],x);

            else:
                x=VAR(p[1]);
                x.__setType__(str(self.var_type));
                self.decList.update({p[1]:x});

        elif (p[2]!=None):
            print "its an array";
            x=ARRAY(VAR(p[1]));
            x.__setType__(("array",self.var_type));
            self.decList.update({p[1]:x});
            
        p[0]=x;
        

    def p_dimstar(self,p):
        'DimStar : LBRACKET RBRACKET'
        pass;

    def var_helper(self,p,x):
       
        if self.decList.has_key(p)==True:
            
            if self.scopeList.has_key(p)==False:
                self.scopeList.update({p:[1]});
                x=VAR(p+"1");
                x.__setType__(str(self.var_type));
                self.decList.update({str(x):x});
                return x;
            else:
                aList=self.scopeList[p];
                num=aList[len(aList)-1];
                num=num+1;
                x=VAR(p+str(num));
                x.__setType__(str(self.var_type));
                aList.append(num);
                self.decList.update({str(x):x});
                return x;
                
        else:
            x=VAR(p);
            x.__setType__(str(self.var_type));
            self.decList.update({p:x});
            return x;
    

    def p_func(self,p):
        'FunDecl : Type ID LPAREN fseen FormalOpt RPAREN stmt'
        x=FUNCTION(p[2],p[5],p[1],p[7]);
        "Add the function to the symbol table"
        self.decList.update({p[2]:x});
        p[0]=x;
        self.fscope=0;
        

    def p_fseen(self,p):
        'fseen : empty'
        self.fscope=1;
        self.f_ret=self.var_type;
        pass;
    
    def p_formal_opt(self,p):
        'FormalOpt : Type ID'
        x=None;
        self.scopeList.update({p[2]:[1]});
        x=VAR(p[2]+"1");
        x.__setType__(str(self.var_type));
        self.decList.update({str(x):x});
        p[0]=FORMAL(p[1],x);


    def p_formal_opt_empty(self,p):
        'FormalOpt : empty'
        p[0]=None;


    def p_functioncall(self,p):
        'FunctionCall : ID LPAREN Args RPAREN'
        try:
            x=self.decList[p[1]];
            y=FUNCALL(p[1],p[3]);
            y.__setType__(x.__getType__());
            y.__setInType__(x.__getInType__());
            p[0]=y;

        except LookupError:
            print("Undefined function name '%s'" %p[1])
            exit(1); 

    def p_func_argsopt(self,p):
        'Args : AE'
        p[0]=p[1];

    def p_func_argsempty(self,p):
        'Args : empty'
        p[0]=None;


    def p_classdecl(self,p):
        'ClassDecl : CLASS ID LBRACE Extension RBRACE'
        x=OBJECTDECL(p[4],VAR(p[2]));
        self.decList.update({p[2]:x});
        p[0]=x;

    def p_dimstar_empty(self,p):
         'DimStar : empty'
         p[0]=None;

    def p_dimstar_dim(self,p):
        'DimStar : LBRACKET RBRACKET DimStar'
        p[0]=p[1];
    
    
    def p_stmt_matchedstmt(self,p):
        '''stmt : matchedstmt'''
        p[0]=p[1];
        

    def p_stmt_openstmt(self,p):
        'stmt : openstmt'
        p[0]=p[1];


    #Changing the grammar for assign
    def p_stmt_assign(self,p):
        '''matchedstmt : SE SCOLON'''
        p[0]=p[1];


    def p_stmt_print(self,p):
        'matchedstmt : Print'
        p[0]=p[1];


    def p_stmt_while(self,p):
        'matchedstmt : While'
        p[0]=p[1];

    def p_stmt_block(self,p):
        'matchedstmt : Block'
        p[0]=p[1];

    def p_stmt_do_while(self,p):
        'matchedstmt : doWhile'
        p[0]=p[1];

    def p_stmt_for(self,p):
        'matchedstmt : for'
        p[0]=p[1];

    def p_stmt_ret(self,p):
        'matchedstmt : ReturnOpt SCOLON'
        p[0]=p[1];

    def p_ret_ae(self,p):
        'ReturnOpt : RETURN AE'
        p[0]=RETURN(p[2],self.f_ret);

    def p_ret_void(self,p):
        'ReturnOpt : RETURN VOID'
        p[0]=RETURN(p[2],p[2]);

    #Grammar rules for handling dangling if else stmts
    def p_openstmt_then(self,p):
        '''openstmt : IF AE THEN stmt''' 
        p[0]=IF(p[2],p[4]);
       

    def p_openstmt_then_else(self,p):
        'openstmt : IF AE THEN matchedstmt ELSE openstmt'
        p[0]=IF_ELSE(p[2],p[4],p[6]);


    def p_matchedstmt(self,p):
        'matchedstmt : IF AE THEN matchedstmt ELSE matchedstmt'
        p[0]=IF_ELSE(p[2],p[4],p[6]);

    
               
    def p_assign(self,p):
        '''SE : LHS EQUALS AE'''
        if(isinstance(p[1],ARRAY)):
            if p[1].__getType__()==p[3].__getType__():
                p[1].__setSize__(p[3]);
                p[0]=p[1];
            else:
                print "Wrong Array Assignment"
                exit(1);

        if(isinstance(p[1],ARRAYGET)):
            p[1].__setToValue__(p[3]);
            p[1].__toLoad__(0);
            p[0]=ASSIGN(p[1],p[3]);
            p[0].__toAssignArray__(1);

        if(isinstance(p[3],ARRAYGET)):
            p[3].__toLoad__(1);
            p[0]=ASSIGN(p[1],p[3]);

        if(isinstance(p[3],OBJECT)):
            print p[1].__getType__();
            print p[3].__getType__();
            if p[1].__getType__()==p[3].__getType__():
                print "Right type of objects"
                p[3].__setName__(p[1]);
                self.decList[str(p[1])]=p[3];
                p[0]=p[3];
            else:
                print "Wrong object assignment"
                exit(1);
                
        if(isinstance(p[1],OBJACC)):
            print "Right object field assignment"
            p[1].__setValue__(p[3]);
            p[1].__toLoad__(0);
            p[0]=ASSIGN(p[1],p[3]);
            p[0].__toAssignArray__(1);
            
            

        if not isinstance(p[1],(OBJACC,ARRAY,ARRAYGET,OBJECT)) and not isinstance(p[3],(OBJECT,ARRAYGET,ARRAY)):
            p[0]=ASSIGN(p[1],p[3]);
        


    def p_lhs_id(self,p):
        'LHS : FieldAccess'
        p[0]=p[1];  

    def p_lhs_array(self,p):
        'LHS : ArrayAccess'
        p[0]=p[1];

    def p_fieldaccess_id(self,p):
        'FieldAccess : ID'
        x=None;
        try:
            if(self.scope==1 or self.fscope==1):
                print ("We are in a scope")
                if self.scopeList.has_key(p[1])==True:
                    
                  
                    aList=self.scopeList.get(p[1]);
                    num=aList[len(aList)-1];
                    
                    x=self.decList[p[1]+str(num)];
                else:
                   
                    x=self.decList[p[1]];
            else:        
                x=self.decList[p[1]];
            p[0]=x;

        except LookupError:
            print("Undefined or undeclared name '%s'" %p[1])
            exit(1);

        

    def p_fieldaccess_obj(self,p):
        'FieldAccess : Primary DOT ID'
        x=p[1];    
        if isinstance(x,OBJECT):
            i= x.__hasVar__(p[3])
            if i!=None :
                y=OBJACC(p[1],NUM(i),p[3]);
                p[0]=y;
                     
            else:
                print "Object field not accessible"
                exit(1);
        else:
            print "Trying to access something that is not an object"
            exit(1);


    
    def p_se_inc(self,p):
        'SE : INCREMENT LHS'
        p[0]=ASSIGN(p[2],AE(p[2],"+",NUM(1)));

    def p_se_dec(self,p):
        'SE : DECREMENT LHS'
        p[0]=ASSIGN(p[2],AE(p[2],"-",NUM(1)));


    def p_print(self,p):
        'Print : PRINT LPAREN AE RPAREN SCOLON'
        if(isinstance(p[3],ARRAYGET)):
            p[3].__toLoad__(1);
           
        p[0]=PRINT(p[3]);

    def p_while(self,p):
        'While : WHILE AE DO matchedstmt'
        p[0]=WHILE(p[2],p[4]);


    def p_do_while(self,p):
        'doWhile : DO matchedstmt WHILE AE SCOLON'
        p[0]=DO_WHILE(p[2],p[4]);


    def p_for(self,p):
        'for : FOR LPAREN SEopt SCOLON AEopt SCOLON SEopt RPAREN matchedstmt'
        p[0]=FOR(p[3],p[5],p[7],p[9]);


    def p_seopt(self,p):
        'SEopt : SE'
        p[0]=p[1];

    def p_seopt_empty(self,p):
        'SEopt : empty'
        p[0]=None;

    def p_aeopt(self,p):
        'AEopt : AE'
        p[0]=p[1];

    def p_aeopt_empty(self,p):
        'AEopt : empty'
        p[0]=None;

    def p_ae_se(self,p):
        'AE : SE'
        p[0]=p[1];

    def p_ae_lhs(self,p):
        'AE : Primary'
        p[0]=p[1];

    def p_primary_fieldacc(self,p):
        'Primary : FieldAccess'
        p[0]=p[1];
        
    def p_primary_funcall(self,p):
        'Primary : FunctionCall'
        p[0]=p[1];

    def p_ae_input(self,p):
        'Primary : INPUT LPAREN RPAREN'
        p[0]=INPUT();

    def p_ae_true(self,p):
        'Primary : TRUE'
        x=TRUE();
        x.__setType__("bool");
        p[0]=x;

    def p_ae_false(self,p):
        'Primary : FALSE'
        x=FALSE();
        x.__setType__("bool");
        p[0]=x;
            
    def p_ae_paren(self,p):
        'Primary : LPAREN AE RPAREN'
        p[0]=p[2];

    def p_ae_number(self,p):
        'Primary : NUMBER'
        x=NUM(p[1]);
        x.__setType__("int");
        p[0]=x;

    def p_plus(self,p):
        """AE : AE PLUS AE"""
        p[0]=AE(p[1],'+',p[3]);


    def p_minus(self,p):
        'AE : AE MINUS AE'
        p[0]=AE(p[1],"-",p[3]);

    def p_mult(self,p):
        'AE : AE MULT AE'
        p[0]=AE(p[1],"*",p[3]);

    def p_div(self,p):
        'AE : AE DIVIDE AE'
        p[0]=AE(p[1],"/",p[3]);

    def p_mod(self,p):
        'AE : AE MOD AE'
        p[0]=AE(p[1],"%",p[3]);


    def p_uminus(self,p):
        'AE : MINUS AE %prec UMINUS'
        x=NEG(p[2]);
        x.__setType__(p[2].__getType__());
        p[0]=x;
    

    def p_greater(self,p):
        'AE : AE GREATERTHAN AE'
        p[0]=AE(p[1],'>',p[3]);

    def p_greaterEqual(self,p):
        'AE : AE GREATEROREQUAL AE'
        p[0]=AE(p[1],'>=',p[3]);

    def p_less(self,p):
        'AE : AE LESSTHAN AE'
        p[0]=AE(p[1],'<',p[3]);

    
    def p_lessEqual(self,p):
        'AE : AE LESSOREQUAL AE'
        p[0]=AE(p[1],'<=',p[3]);


    def p_isequal(self,p):
        'AE : AE ISEQUAL AE'
        p[0]=AE(p[1],"==",p[3]);

    def p_notequal(self,p):
        'AE : AE NOTEQUAL AE'
        p[0]=AE(p[1],"!=",p[3]);

    def p_and(self,p):
        'AE : AE AND AE'
        p[0]=AE(p[1],"&&",p[3]);

    def p_or(self,p):
        'AE : AE OR AE'
        p[0]=AE(p[1],"||",p[3]);

    def p_not(self,p):
        'AE : NOT AE %prec NOT'
        print str(p[2].__getType__());
        p[0]= AE(p[2],"!",NUM(1));

    def p_prim_array_access(self,p):
        'Primary : ArrayAccess'
        p[0]=p[1];


    def p_primary_newobj(self,p):
        'Primary : NEW ID LPAREN RPAREN'
        x=self.decList[p[2]];
        p[0]=OBJECT(x);

    def p_ae_dimexpr(self,p):
        'AE : NEW Type DimExpr DimStar'
        x= p[3];
        x.__setType__(("array",p[2]));
        p[0]=x;

    def p_arrray_access(self,p):
        'ArrayAccess : Primary LBRACKET AE RBRACKET'
        
        p[0]=ARRAYGET(p[1],p[3]);

    def p_dimexpr(self,p):
        'DimExpr : LBRACKET AE RBRACKET'
        p[0]=p[2];

    def p_block(self,p):
        'Block : LBRACE seen Extension RBRACE'
        p[0]=BLOCK(p[3]);
        self.scope=0;

    def p_seen(self,p):
        'seen :'
        self.scope=1;
        
    


    def build(self):
        self.parser=yacc.yacc(module=self)


    def parse(self,data):
        self.lex.test(data);
        result=self.parser.parse(data);
        print result;
        if result.__isWelformed__(self.dList):
            pass;

        else:
            print "error in semantics"
            exit(1);
            
        result.__gencode__();
        t=getCode();
        """index=getDictIndex()+1;
        tempDict={index : ["EXIT","_","_","_"]};
        t.update(tempDict);"""
        for value in t.items():
            print value;


        return t;
    
