i=0;
iCode={};
dictIndex=0;

def newtemp():
    global i;
    i=i+1;
    return "$"+str(i);

def addCode(temp):
    global iCode;
    global dictIndex;
    dictIndex=dictIndex+1;
    tempdict={dictIndex:temp};
    iCode.update(tempdict);

def getCode():
    global iCode;
    #print iCode;
    return iCode;

def getDictIndex():
    global dictIndex;
    return dictIndex;

class AST:
   pass;

class VAR(AST):

    stype="";
    def __init__(self,x):
        self.var=x;
        self.welformed=False;

    def __str__(self):
        return self.var;

    def __defined__(self):
        return self.var;

    def __setWelformed__(self,value):
        self.welformed=value;

    def __isWelformed__(self,temp):
        if self.var in temp:
            return True;
        else:
            return False;

    def __gencode__(self):
        self.tvalue=self.var
        return self.tvalue;

    def __setType__(self,stype):
        self.stype=stype;

    def __getType__(self):
        return self.stype;

class NUM(AST):

    stype="";
    def __init__(self,n):
        self.num=n;
        
        
    def __str__(self):
        return str(self.num);
    

    def __isWelformed__(self,temp):
        return True;

    def __setType__(self,stype):
        self.stype=stype;

    def __getType__(self):
        return self.stype;

    def __gencode__(self):
        temp=newtemp();
        addCode(["=",temp,int(self.num),"_"]);
        self.tvalue=temp;
        return self.tvalue;

class TRUE(AST):

    stype="bool";
    
    def __init__(self):
        self.num=1;
       
    def __str__(self):
        return "True";
    

    def __isWelformed__(self,temp):
        return True;

    def __setType__(self,stype):
        self.stype=stype;

    def __getType__(self):
        return self.stype;

    def __gencode__(self):
        temp=newtemp();
        addCode(["=",temp,int(self.num),"_"]);
        self.tvalue=temp;
        return self.tvalue;  


class FALSE(AST):
    stype="bool";
    
    def __init__(self):
        self.num=0;
        

    def __str__(self):
        return "False";
    

    def __isWelformed__(self,temp):
        return True;

    def __setType__(self,stype):
        self.stype=stype;

    def __getType__(self):
        return self.stype;

    def __gencode__(self):
        temp=newtemp();
        addCode(["=",temp,int(self.num),"_"]);
        self.tvalue=temp;
        return self.tvalue;
        
class NEG(AST):

    stype="";
    def __init__(self,val):
        self.lchild=val;
        

    def __str__(self):
        return "-" + str(self.lchild);

    def __isWelformed__(self,temp):
        return self.lchild.__isWelformed__(temp);

    def __typeCheck__(self):
        if(self.lchild.__getType__()=="int"):
            self.stype="int";
        else:
            print "Negation not well typed";
            exit(1);


    def __getType__(self):
        return self.stype;

    def __setType__(self,stype):
        self.stype=stype;

    def __gencode__(self):
        
        temp=newtemp();
        addCode(["*",temp,NUM(-1).__gencode__(),self.lchild.__gencode__()]);
        self.tvalue=temp;
        return self.tvalue;


class ASSIGN(AST):

    def __init__(self,c1,c2):
            self.lchild=c1;
            self.rchild=c2;
            self.check=0;

    def __str__(self):
        return str(self.lchild) + "=" + str(self.rchild);

    def __defined__(self):
        return self.lchild.__defined__();

    def __toAssignArray__(self,p):
        self.check=p

    def __getType__(self):
        return self.type;

    def __setType__(self,stype):
        self.type=stype;


    def __isWelformed__(self,temp):
        if isinstance(self.rchild,INPUT) or isinstance(self.rchild,(NUM,TRUE,FALSE)):
            if not isinstance(self.lchild,(ARRAYGET,OBJACC)):
                self.lchild.__setWelformed__(True);
                temp.append(str(self.lchild));
            return True;
        else:
            if self.rchild.__isWelformed__(temp)==True:
                temp.append(str(self.lchild));
                return True;
            else:
                return False;

    def __typeCheck__(self):
        if  not isinstance(self.rchild,INPUT):
            if(self.lchild.__getType__()==self.rchild.__getType__()):
                self.__setType__(self.lchild.__getType__());

            else:
                self.__setType__("error");
                print "Type Error"
                exit(1);

    def __gencode__(self):

        self.__typeCheck__();
        
        if(self.check==1):
           addCode(["=",self.lchild.__gencode__(),self.rchild.__gencode__(),1]);
        else:
            addCode(["=",self.lchild.__gencode__(),self.rchild.__gencode__(),"_"]);
        return self.lchild.tvalue ;


    def __isReturned__(self):
        return False;

class AE(AST):
    def __init__(self,c1,op,c2):
        self.lchild=c1;
        self.op=op;
        self.rchild=c2;

    def __str__(self):
        return "(" + str(self.lchild)+" " + self.op + " "+str(self.rchild)+")";


    def __isWelformed__(self,temp):
        return self.rchild.__isWelformed__(temp) and self.lchild.__isWelformed__(temp);

    def __gencode__(self):
        temp=newtemp();
        addCode([self.op,temp,self.lchild.__gencode__(),self.rchild.__gencode__()]);
        self.tvalue=temp;
        return self.tvalue;


    def __getType__(self):
        if (str(self.op)=="!"):
            if(self.lchild.__getType__()=="bool"):
                return "bool";
            else:
                return "error";
        if(str(self.op)=="!=" or str(self.op)=="=="):
            if(self.lchild.__getType__()=="bool" and self.rchild.__getType__()=="bool") or(self.lchild.__getType__()=="int" and self.rchild.__getType__()=="int"):
                return "bool";
            else:
                return "error";

        if(str(self.op)=="<" or str(self.op)==">" or str(self.op)=="<=" or str(self.op)==">="):
            if(self.lchild.__getType__()=="int" and self.rchild.__getType__()=="int"):
                return "bool";
            else:
                return "error";

        if(str(self.op)=="&&" or str(self.op)=="||"):
            if(self.lchild.__getType__()=="bool" and self.rchild.__getType__()=="bool"):
                return "bool";
            else:
                return "error";
            
        if(str(self.op)=="+" or str(self.op)=="-" or str(self.op)=="*" or str(self.op)=="/" or str(self.op)=="%"):
            if(self.lchild.__getType__()=="int" and self.rchild.__getType__()=="int"):
                return "int"
            else:
                return "error";
            
                
                   
class ARRAY(AST):
    stype="";
    def __init__(self,varname):
        self.name=varname;
        self.lchild="";
        
    def __str__(self):
        return str(self.name)+"=["+str(self.lchild)+"]";

    def __isWelformed__(self,temp):
         if self.lchild.__isWelformed__(temp)==True:
             temp.append(str(self.name));
             return True;

         else:
             return False;

    def __setSize__(self,size):
        self.lchild=size;

    def __setType__(self,typ):
        self.stype=typ;

    def __getType__(self):
        return self.stype;

    def __isReturned__(self):
        return False;

    def __gencode__(self):
        #Need to create an array
        temp=newtemp();
        addCode(["memgen",temp,self.lchild.__gencode__(),self.name.__gencode__()]);
        return temp;
       

class ARRAYGET(AST):
    def __init__(self,varname,index):
        self.lchild=varname;
        self.rchild=index;
        #A variable check if an array index is to be loaded or stored at
        self.load=1;

    def __str__(self):
        if(self.load==0):
            return str(self.lchild.name)+"["+str(self.rchild)+"]= "+str(self.value);
        else:
            return str(self.lchild.name)+"["+str(self.rchild)+"]";

    def __isWelformed__(self,temp):
        return self.rchild.__isWelformed__(temp);
            
    def __toLoad__(self,temp):
        self.load=temp;

    def __setToValue__(self,value):
        self.value=value;

    def __getType__(self):
        x=self.lchild.__getType__();
        return x[1];

    def __TypeCheck__(self):
        if self.rchild.__getType__()=="int":
           return;
        else:
            print "Array Index not an integer"
            exit(1);

    def __gencode__(self):
        self.__TypeCheck__();
        if self.load==0:
            temp=newtemp();
            self.tvalue=temp;
            addCode(["memstore",temp,str(self.lchild.name),self.rchild.__gencode__()]);
            return self.tvalue;
        else:
            temp=newtemp();
            self.tvalue=temp;
            addCode(["memload",temp,str(self.lchild.name),self.rchild.__gencode__()]);
            return self.tvalue;


class INPUT(AST):
    def __init__(self):
        pass;

    def __str__(self):
        return "input()";

    def __gencode__(self):
        temp=newtemp();
        addCode(["input",temp,"_","_"]);
        self.tvalue=temp
        return self.tvalue;
        

class PRINT(AST):
    def __init__(self,value):
        self.lchild=value;

    def __str__(self):
        return "Print (" +str(self.lchild)+")";

    def __isWelformed__(self,temp):
        return self.lchild.__isWelformed__(temp);

    def __TypeCheck__(self):
        if(self.lchild.__getType__()=="int"):
            return
        else:
            print "Type error in print"
            exit(1);


    def __gencode__(self):
        addCode(["print","_",self.lchild.__gencode__(),"_"]);
        return;

    def __isReturned__(self):
        return False;

class BLOCK(AST):
    def __init__(self,stmtseq):
        self.lchild=stmtseq;

    def __str__(self):
        return "{" + str(self.lchild) + "}";

    def __isWelformed__(self,temp):
        block_temp=temp[:];
        return self.lchild.__isWelformed__(block_temp)
    #NEEDS CHANGE?
    def __gencode__(self):
        self.lchild.__gencode__();
        return;

    def __isReturned__(self):
        return self.lchild.__isReturned__();

class IF(AST):
        
    def __init__(self,cond,then):
        self.cond=cond;
        self.lchild=then;
        self.reg=0;

    
    def __str__(self):
        return "If " + str(self.cond)+" Then \n" +str(self.lchild)


    def __isWelformed__(self,temp):
        #if_local_temp=temp[:];
        return self.cond.__isWelformed__(temp) and self.lchild.__isWelformed__(temp);


    def __typeCheck__(self):
        print str(self.cond.__getType__());
        if(self.cond.__getType__()=="bool"):
            return ;
        else:
            print "If statement not well typed";
            exit(1);
    

    def __gencode__(self):

        self.__typeCheck__();
        
        tempreg=self.cond.__gencode__();

        #Store this instruction in dict temporarily
        addCode(["jfalse",tempreg,"Label"+str(self.reg),"_"]) 

        tempIndex=getDictIndex(); #Get the pointer for prev instruction

        #Generate the intermediate code for then statement
        self.lchild.__gencode__(); 

        tempDict=getCode(); #Get the dictionary

        self.reg=getDictIndex()+1; #Get the right jump label
        
        #Now change the jfalse instruction with the right address label
        tempDict[tempIndex]=["jfalse",tempreg,"Label"+str(self.reg),"_"];
       
        return;


    def __isReturned__(self):
        return False;


class IF_ELSE(AST):

    def __init__(self,cond,then,elstmt):
        self.cond=cond;
        self.lchild=then;
        self.rchild=elstmt;
        self.reg=0;
        self.reg1=0;

    def __str__(self):
        return "If " + str(self.cond)+" Then \n" +str(self.lchild)+ "\nElse\n" + str(self.rchild)

    def __isWelformed__(self,temp):
        #if_else_local_temp=temp[:];
        return (self.cond.__isWelformed__(temp)
                and self.lchild.__isWelformed__(temp)
                and self.rchild.__isWelformed__(temp));


    def __typeCheck__(self):
        print str(self.cond.__getType__());
        if(self.cond.__getType__()=="bool"):
            return ;
        else:
            print "If statement not well typed";
            exit(1);



    def __gencode__(self):

        self.__typeCheck__();
        
        tempreg=self.cond.__gencode__();

        #Store this instruction in dict temporarily
        addCode(["jfalse",tempreg,"Label"+str(self.reg),"_"]) 

        tempIndex=getDictIndex(); #Get the pointer for prev instruction

        #Generate the intermediate code for 'then' statement
        self.lchild.__gencode__(); 

        

        #if the 'if' statement finished excuting skip the else
        addCode(["jmp","Label"+str(self.reg1),"_","_"])

        #Get the index for the prev instruction
        tempIndex2=getDictIndex();

        self.reg=getDictIndex()+1; #Get the right jump label

        #Get the intermediate code for the 'else' statement
        self.rchild.__gencode__();

        self.reg1=getDictIndex()+1;
        
        
        #Now change the jfalse and jmp instruction with the right address label
        tempDict=getCode();
        tempDict[tempIndex]=["jfalse",tempreg,"Label"+str(self.reg),"_"];
        tempDict[tempIndex2]=["jmp","_","Label"+str(self.reg1),"_"]
       
        return;

    def __isReturned__(self):
      return self.lchild.__isReturned__() and self.rchild.__isReturned__();


class WHILE(AST):

    def __init__(self,cond,do):
        self.cond=cond;
        self.lchild=do;
        self.reg=0;
        self.reg1=0;

    def __str__(self):
        return "While " +str(self.cond) +"\ndo : " + str(self.lchild);


    def __isWelformed__(self,temp):
        #while_local_temp=temp[:];
        return self.cond.__isWelformed__(temp) and self.lchild.__isWelformed__(temp);

    
    def __TypeCheck__(self):
        if(self.cond.__getType__()=="bool"):
            return;
        else:
            print "While statement not well typed"
            exit(1);


    def __gencode__(self):

        self.__TypeCheck__();
        
        tempreg=self.cond.__gencode__();

        #To get the label of the 'condition'statement
        self.reg1=getDictIndex();
    
        #Store this instruction in dict temporarily
        addCode(["jfalse","Label"+str(self.reg1),"_","_"])

        tempIndex=getDictIndex();

        #Intermediate code for the 'do' statement
        self.lchild.__gencode__()

        addCode(["jmp","_","Label"+str(self.reg1),"_"])

        #Getting the right label
        self.reg=getDictIndex()+1;
        
        #Now change the jfalse instruction with the right address label
        tempDict=getCode();
        tempDict[tempIndex]=["jfalse",tempreg,"Label"+str(self.reg),"_"];

    def __isReturned__(self):
        return self.lchild.__isReturned__();


class DO_WHILE(AST):

    def __init__(self,do_stmt,cond):
        self.lchild=do_stmt;
        self.cond=cond;
        self.reg=0;
        self.reg1=0;

    def __str__(self):
        return "do " + str(self.lchild) + "\nwhile" + str(self.cond);

    def __isWelformed__(self,temp):
        #doWhile_local_temp=temp[:];
        return self.cond.__isWelformed__(temp) and self.lchild.__isWelformed__(temp);


    def __TypeCheck__(self):
        if(self.cond.__getType__()=="bool"):
            return;
        else:
            print "While statement not well typed"
            exit(1);

    def __gencode__(self):
        self.__TypeCheck__();
        
        # To get the lable of the do statment 
        self.reg1=getDictIndex()+1;
        self.lchild.__gencode__();
        
        tempreg=self.cond.__gencode__();

        #Storing the jfalse instruction temporarily 
        addCode(["jfalse",tempreg,"Label"+str(self.reg1),"_"]);
        tempIndex=getDictIndex();

        addCode(["jmp","_","Label"+str(self.reg1),"_"]);

        #Getting the label number after 'jmp' instruction
        self.reg=getDictIndex()+1;

        #Now change the jfalse instruction with the right address label
        tempDict=getCode();
        tempDict[tempIndex]=["jfalse",tempreg,"Label"+str(self.reg),"_"];

    def __isReturned__(self):
        return self.lchild.__isReturned__();


class FOR(AST):

    def __init__(self,SEopt1,AEopt,SEopt2,stmt):
        self.lchild=stmt;
        self.ae=AEopt;
        self.s1=SEopt1;
        self.s2=SEopt2;

    def __str__(self):
        string="for( ";
        if (self.s1!=None):
            string+= str(self.s1);
  
        string+=";";

        if(self.ae!=None):
            string+=str(self.ae);

        string+=";";

        if(self.s2!=None):
            string+=str(self.s2);

        string+=")\n"
        string+=str(self.lchild);
        return string;

    def __isWelformed__(self,temp):
        check=True;

        if(self.s1!=None):
            check=self.s1.__isWelformed__(temp);
        if(self.ae!=None):
            check=self.ae.__isWelformed__(temp);
        if(self.s2!=None):
            check=self.s2.__isWelformed__(temp);

        check=self.lchild.__isWelformed__(temp);
        return check;


    def __gencode__(self):
        tempreg="";
        label1=0;
        label2=0;
        tempIndex=0;
        if(self.s1 != None):
            self.s1.__gencode__();

        if(self.ae !=None):
            tempreg=self.ae.__gencode__();
            label1=getDictIndex();
            #storing the 'jfalse' instruction temporarily
            addCode(["jfalse",tempreg,"Label"+str(label1),"_"]);
            tempIndex=getDictIndex();

        self.lchild.__gencode__();

        #Getting the label number of the statement
        label2=getDictIndex();

        if(self.s2 != None):
            self.s2.__gencode__();

        if(self.ae!=None):
            addCode(["jmp","_","Label"+str(label1),"_"])
            label1=getDictIndex()+1;
            tempDict=getCode();
            tempDict[tempIndex]=["jfalse",tempreg,"Label"+str(label1),"_"]

        if(self.ae==None):
            addCode(["jmp","_","Label"+str(label2),"_"])
            

    def __isReturned__(self):
        return self.lchild.__isReturned__();


class FUNCTION(AST):
    def __init__(self,name,param,retype,stmt):
        self.param=param;
        self.retype=retype;
        self.stmt=stmt;
        self.name=name;
        

    def __str__(self):
        if self.param==None:
            string= str(self.retype)+" " +str(self.name)+"()"+self.stmt.__str__();

        else:
            string= str(self.retype)+" " +str(self.name)+"("+self.param.__str__()+")"+self.stmt.__str__();
        return string;

    def __getType__(self):
        return self.retype;

    def __getInType__(self):
        if self.param!=None:
            return self.param.__getType__();
        else:
            return None;

    def __isWelformed__(self,temp):
        if self.param==None:
            return self.stmt.__isWelformed__(temp) and self.stmt.__isReturned__();  
        else:
            return self.param.__isWelformed__(temp) and self.stmt.__isWelformed__(temp) and self.stmt.__isReturned__();

    def __gencode__(self):
        if self.param!=None:
            print "Param is  not none"
            addCode(["func",str(self.name),self.param.__gencode__(),"_"]);
            self.stmt.__gencode__();
            
        else:
            addCode(["func",str(self.name),"_","_"]);
            self.stmt.__gencode__();

        return;



class FUNCALL(AST):
    stype="";
    intype="";
    def __init__(self,name,arg):
        self.name=name;
        self.param=arg;

    def __str__(self):
        if self.param!=None:
            return str(self.name)+"("+self.param.__str__()+")";
        else:
            return str(self.name)+"()";

    def __setType__(self,p):
        self.stype=p;

    def __setInType__(self,p):
        self.intype=p;

    def __getType__(self):
        return self.stype;

    def __getInType__(self):
        return self.intype;

    def __TypeCheck__(self):
        if self.param!=None:
            if(self.intype==self.param.__getType__()):
                return;
            else:
                print "Error in function parameters"
                exit(1);
        if self.param==None and self.intype!=None:
            print "Function missing arguments"
            exit(1);

    def __isWelformed__(self,temp):
        if self.param!=None:
            return self.param.__isWelformed__(temp);
        else:
            return True;

    def __gencode__(self):
        self.__TypeCheck__();
        temp=newtemp();
        if self.param!=None:
            addCode(["funcall",str(self.name),self.param.__gencode__(),temp]);
        else:
            addCode(["funcall",str(self.name),"_",temp]);
        return temp;

    
class FORMAL(AST):
    def __init__(self,stype,name):
        self.stype=stype;
        self.name=name;

    def __str__(self):
        return str(self.stype)+" "+str(self.name); 

    def __getType__(self):
        return self.stype;

    def __isWelformed__(self,temp):
        temp.append(str(self.name));
        return True;

    def __getName__(self):
        return self.name;

    def __gencode__(self):
        return self.name.__gencode__();



class RETURN(AST):
    def __init__(self,p,typ):
        self.lchild=p;
        self.stype=typ;

    def __str__(self):
        if self.lchild!="void":
            return "return "+str(self.lchild);
        else:
            return "return void";

    def __isWelformed__(self,temp):
        temp.append("return");
        if self.lchild!="void":
            return self.lchild.__isWelformed__(temp);
        else:
            return True;

    def __TypeCheck__(self):
        if (self.lchild=="void" or self.lchild.__getType__()=="void")and self.stype=="void":
            return;
        elif(self.lchild!="void" and self.lchild.__getType__()==str(self.stype)):
            return;
        else:
            print "Return statement not well typed"
            exit(1);


    def __gencode__(self):
        self.__TypeCheck__();
        if self.lchild!="void":
            addCode(["return",self.lchild.__gencode__(),"_","_"]);
        else:
            addCode(["return","_","_","_"]);
        return;

    def __isReturned__(self):
        return True;


class STMT(AST):

    def __init__(self,stmt):
        self.lchild=stmt;


    def __str__(self):
        return str(self.lchild);

    def __isWelformed__(self,temp):
        return self.lchild.__isWelformed__(temp);


    def __gencode__(self):
        self.lchild.__gencode__();
        return;

    def __isReturned__(self):
        return self.lchild.__isReturned__();



class STMTSEQ(AST):

    def __init__(self,stmt,stmtsq):
        self.lchild=stmt;
        self.rchild=stmtsq;


    def __str__(self):
        return str(self.lchild) + "\n" + str(self.rchild); 
    

    def __isWelformed__(self,temp):
        return self.lchild.__isWelformed__(temp) and self.rchild.__isWelformed__(temp);

    def __gencode__(self):
        self.lchild.__gencode__();
        self.rchild.__gencode__();
        return;

    def __isReturned__(self):
        return  self.lchild.__isReturned__() or self.rchild.__isReturned__();

class DECLSEQ(AST):
    def __init__(self,stmt,stmtsq):
        self.lchild=stmt;
        self.rchild=stmtsq;


    def __str__(self):
        return str(self.lchild) + "\n" + str(self.rchild); 
    

    def __isWelformed__(self,temp):
        return self.lchild.__isWelformed__(temp) and self.rchild.__isWelformed__(temp);

    def __gencode__(self):
        self.lchild.__gencode__();
        self.rchild.__gencode__();
        return;

class DECL(AST):
    
    def __init__(self,stmt):
        self.lchild=stmt;


    def __str__(self):
        return str(self.lchild);

    def __isWelformed__(self,temp):
        return self.lchild.__isWelformed__(temp);


    def __gencode__(self):
        self.lchild.__gencode__();
        return;


class VARLISTSQ(AST):
    def __init__(self,lch,rch):
        self.lchild=lch;
        self.rchild=rch;

    def __str__(self):
        return str(self.lchild)+"\n" +str(self.rchild);

    def __isWelformed__(self,temp):
        return True;

    def __isReturned__(self):
        return False;

    def __gencode__(self):
        return;

class VARLIST(AST):
    def __init__(self,lch):
        self.lchild=lch;
        self.rchild=None;

    def __str__(self):
        return str(self.lchild);

    def __isWelformed__(self,temp):
        return True;

    def __isReturned__(self):
        return False;

    def __gencode__(self):
        return;
    

class OBJECTDECL(AST):
    vList=[];
    def __init__(self,lch,typ):
        self.lchild=lch;
        self.stype=typ;
        self.__getVars__(self.lchild);

    def __str__(self):
        return "class " +str(self.stype)+"{"+ str(self.lchild)+"}";

    def __getVars__(self,lch):
        if isinstance(lch,VAR):
            self.vList.append(lch);
            return;
        if lch.lchild!=None:
            self.__getVars__(lch.lchild);
        if lch.rchild!=None:
            self.__getVars__(lch.rchild);
        
    def __isReturned__(self):
        return False;

    def __isWelformed__(self,temp):
        return self.lchild.__isWelformed__(temp);

    def __getType__(self):
        return self.stype;

    def __gencode__(self):
        """temp=newtemp();
        addCode(["memgen",temp,NUM(len(self.vList)).__gencode__(),self.name.__gencode__()]);
        return temp;"""
        return;


class OBJECT(AST):

    def __init__(self,lch):
        self.lchild=lch;
        
    def __setName__(self,name):
        self.name=name;

    def __getName__(self):
        return self.name;

    def __isWelformed__(self,temp):
        temp.append(str(self.name));
        return True;

    def __str__(self):
        return str(self.name)+" = "+"new " +self.__getType__()+"()"; 

    def __isReturned__(self):
        return False;

    def __getType__(self):
        return str(self.lchild.__getType__());

    def __hasVar__(self,p):
        for i in xrange(0,len(self.lchild.vList)):
            if str(self.lchild.vList[i])==p:
                return i;

    def __gencode__(self):
        temp=newtemp();
        addCode(["memgen",temp,NUM(len(self.lchild.vList)).__gencode__(),self.name.__gencode__()]);
        return temp;


class OBJACC(AST):

    def __init__(self,lch,index,var):
        self.lchild=lch;
        self.index=index;
        self.var=var;
        self.load=1;
        
    def __str__(self):
        return str (self.lchild.__getName__())+"."+str(self.var);

    def __setValue__(self,p):
        self.value=p;

    def __isWelformed__(self,temp):
        #temp.append(str(lch.__getName__())+"."+str(self.var));
        return True;

    def __getType__(self):
        x=self.lchild.lchild.vList[int(str(self.index))];
        return str(x.__getType__());

    def __toLoad__(self,v):
        self.load=v;

    def __gencode__(self):
        x=int(str(self.index));
        x=x+1;
        y=NUM(x);

        if self.load==0:
            temp=newtemp();
            self.tvalue=temp;
            addCode(["memstore",temp,str(self.lchild.__getName__()),y.__gencode__()]);
            return self.tvalue;
        else:
            temp=newtemp();
            self.tvalue=temp;
            addCode(["memload",temp,str(self.lchild.__getName__()),y.__gencode__()]);
            return self.tvalue;
