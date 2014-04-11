import StringIO
import cStringIO
from my_parser import *
import sys

def main():
    
    if len(sys.argv)==2:
        filename=sys.argv[1];
        fileList=filename.split(".");
        outfile=fileList[0];
    """filename="C:\cse304\Homeworks\HW5\Sample.txt"
    outfile="Sample";"""
    parse(filename,outfile);


def parse(filename,outfile):
    infile=open(filename,"r");
    parser=MyParser();
    parser.build();

    """for line in infile.readlines():
        print line
        parser.parse(line);"""

    intext=infile.read();
    aList=parser.parse(intext);
    res=getVarList(aList);
    symDict=symTable(res);
    formatIns(aList,symDict);

    writeMips(aList,outfile);
    


#Return a list of temporaries used in the
#intermediate code
def getVarList(aList):
    varList=[];
    for quad in aList.values():
        for i in xrange(1,len(quad)):

            lcheck=0;
            if  isinstance (quad[i],str):
                if "Label" in quad[i]:
                    lcheck=1;
            if quad[i-1]=="func" or quad[i-1]=="funcall" :
                continue;
                
            if not isinstance(quad[i],(int,long)) and quad[i]!="_" and lcheck==0:
                varList.append(quad[i]);


    varList=set(varList);
    varList=list(varList);
    return varList;



#Creating a mapping for the temporaries
# to MIPS registers
def symTable(varList):
    symDict={};
    regs=["$t0","$t1","$t2","$t3","$t4","$t5","$t6","$t7","$t8","$t9","$a0","$a1","$a2","$a3",
          "$s0","$s1","$s2","$s3","$s4","$s5","$s6","$s7"];

    if len(varList)>len(regs):
        print "Error: Spilling has occured"
        exit(1);

    else:
        for i in xrange(0,len(varList)):
            tempDict={varList[i]:regs.pop(0)}
            symDict.update(tempDict);

    return symDict;


#This method will then replace all temporaries 
# in intermediate code in aList to mapped registers
def formatIns(aList,symTable):
    for quad in aList.values():
        for i in xrange(1,len(quad)):
            if symTable.has_key(quad[i]):
                reg=symTable.get(quad[i]);
                quad[i]=reg;


def writeMips(aList,outfile):
    
    outfile=outfile+".asm";
    ofile=open(outfile,"w+");
    string=".text\n";
    string+="jal main \n";
    string+=mipsExit();
    for key,quad in aList.iteritems():
        if quad[0]=="=":
            string+=mipsAs(quad,key);
        elif quad[0]=="+":
            string+=mipsAdd(quad,key);
        elif quad[0]=="*":
            string+=mipsMul(quad,key);
        elif quad[0]=="/":
            string+=mipsDiv(quad,key);
        elif quad[0]=="-":
            string+=mipsSub(quad,key);
        elif quad[0]=="input":
            string+=mipsInput(quad,key);
        elif quad[0]=="print":
            string+=mipsPrint(quad,key);
        elif quad[0]=="==":
            string+=mipsIsEqual(quad,key);
        elif quad[0]=="!=":
            string+=mipsNotEqual(quad,key);
        elif quad[0]==">":
            string+=mipsGreaterThan(quad,key);
        elif quad[0]=="<":
            string+=mipsLessThan(quad,key);
        elif quad[0]==">=":
            string+=mipsGreaterEqual(quad,key);
        elif quad[0]=="<=":
            string+=mipsLessEqual(quad,key);
        elif quad[0]=="&&":
            string+=mipsAnd(quad,key);
        elif quad[0]=="||":
            string+=mipsOr(quad,key);
        elif quad[0]=="jfalse":
            string+=mipsJmpFalse(quad,key);
        elif quad[0]=="jmp":
            string+=mipsJmp(quad,key);
        elif quad[0]=="memgen":
            string+=mipsMemgen(quad,key);
        elif quad[0]=="memstore":
            string+=mipsMemstore(quad,key);
        elif quad[0]=="memload":
            string+=mipsMemload(quad,key);
        elif quad[0]=="func":
            string+=mipsFuncDef(quad,key);
        elif quad[0]=="funcall":
            string+=mipsFunCall(quad,key);
        elif quad[0]=="return":
            string+=mipsReturn(quad,key);
        """elif quad[0]=="EXIT":
            string +=mipsExit(quad,key);"""   
       
    ofile.write(string)
    
    ofile.close();
    

def mipsAs(quad,key):
    string="Label"+str(key)+ " : ";
    if(quad[3]==1):
        string+="sw "+quad[2]+" 0("+quad[1]+")\n"
    elif isinstance(quad[2],(int,long)):
        string+="li "+quad[1]+", "+str(quad[2])+"\n";
    else:
        string+="move "+quad[1]+", "+quad[2]+"\n";
    return string;


def mipsAdd(quad,key):
    string="Label"+str(key)+ " : ";
    string+="add "+quad[1]+", "+quad[2]+", "+quad[3]+"\n";
    return string;

def mipsSub(quad,key):
    string="Label"+str(key)+ " : ";
    string+="sub "+quad[1]+", "+quad[2]+", "+quad[3]+"\n";
    return string;

def mipsMul(quad,key):
    string="Label"+str(key)+ " : ";
    if isinstance (quad[3],int):
        quad[3]=str(quad[3]);
    string+="mult "+quad[2]+", "+quad[3]+"\n";
    string1="mflo " +quad[1]+"\n";
    string+=string1;
    return string;

def mipsDiv(quad,key):
    string="Label"+str(key)+ " : ";
    string+="div "+quad[2]+", "+quad[3]+"\n";
    string1="mflo "+quad[1]+"\n";
    string+=string1;
    return string;
    
def mipsMod(quad,key):
    string="Label"+str(key)+ " : ";
    string+="div "+quad[2]+", "+quad[3]+"\n";
    string1="mfhi "+quad[1]+"\n";
    string+=string1;
    return string;

def mipsInput(quad,key):
    string="Label"+str(key)+ " : ";
    string+="li $v0 5 \n";
    string+="syscall\n";
    string+="move, "+quad[1]+", $v0"+"\n";
    return string;

def mipsPrint(quad,key):
    string="Label"+str(key)+ " : ";
    string+="li $v0 1\n"
    string+="move $a0, "+quad[2]+"\n";
    string+="syscall\n"
    return string;


def mipsIsEqual(quad,key):
    string="Label"+str(key)+ " : ";
    string += "xor " + quad[1]+" "+quad[2]+" "+quad[3]+"\n";
    string += "slti " + quad[1]+ " " +quad[1]+" 1 \n";
    return string


def mipsNotEqual(quad,key):
    string="Label"+str(key)+ " : ";
    string += "xor " + quad[1]+" "+quad[2]+" "+quad[3]+"\n";
    #string += "slt " + quad[1]+" "+quad[1]+" $zero\n";
    return string

def mipsNot(quad,key):
    string="Label"+str(key)+ " : ";
    string += "xor " + quad[1]+" "+quad[2]+" "+quad[3]+"\n";
    return string


def mipsGreaterThan(quad,key):
    string="Label"+str(key)+ " : ";
    string += "slt " + quad[1]+" "+quad[3]+" "+quad[2]+"\n";
    return string;

def mipsLessThan(quad,key):
    string="Label"+str(key)+ " : ";
    string += "slt " + quad[1]+" "+quad[2]+" "+quad[3]+"\n";
    return string;

def mipsJmpFalse(quad,key):
    string="Label"+str(key)+ " : ";
    string += "beq $zero "+quad[1] +" "+quad[2]+"\n";
    return string;

def mipsJmp(quad,key):
    string="Label"+str(key)+ " : ";
    string+="j "+quad[2]+"\n";
    return string;

def mipsGreaterEqual(quad,key):
    string="Label"+str(key)+ " : ";
    string += "xor " + quad[1]+" "+quad[2]+" "+quad[3]+"\n";
    string += "slti " + quad[1]+ " " +quad[1]+" 1 \n";
    string += "slt $v0 " +quad[3] + " "+quad[2]+"\n";
    string +="OR " + quad[1]+" $v0 "+quad[1]+"\n";
    return string;


def mipsLessEqual(quad,key):
    string="Label"+str(key)+ " : ";
    string += "xor " + quad[1]+" "+quad[2]+" "+quad[3]+"\n";
    string += "slti " + quad[1]+ " " +quad[1]+" 1 \n";
    string +="slt $v0 " + quad[2]+" "+ quad[3]+"\n";
    string +="OR " + quad[1]+" $v0 "+quad[1]+"\n";
    return string;
    

def mipsAnd(quad,key):
    string="Label"+str(key)+ " : ";
    string+="AND " + quad[1]+" "+quad[2]+" "+quad[3]+"\n";
    return string;

def mipsOr(quad,key):
    string="Label"+str(key)+ " : ";
    string+="OR " + quad[1]+" "+quad[2]+" "+quad[3]+"\n";
    return string;


def mipsMemgen(quad,key):
    string="Label"+str(key)+ " : ";
    string+="li "+quad[1]+" 4\n";
    string+="mult "+quad[1]+" "+quad[2]+"\n";
    string+="mflo "+quad[1]+"\n";
    string+="move $a0, "+quad[1]+"\n";
    string+="li $v0, 9\n";
    string+="Syscall\n"
    string+="move "+quad[3]+", $v0\n";
    return string;


def mipsMemstore(quad,key):
    string="Label"+str(key)+ " : ";
    string+="add "+quad[3]+","+quad[3]+","+quad[3]+"\n";
    string+="add "+quad[3]+","+quad[3]+","+quad[3]+"\n";
    string+="add "+quad[1]+", "+quad[3]+" "+quad[2]+" \n";
    return string;


def mipsMemload(quad,key):
    string="Label"+str(key)+ " : ";
    string+="add "+quad[3]+","+quad[3]+","+quad[3]+"\n";
    string+="add "+quad[3]+","+quad[3]+","+quad[3]+"\n";
    string+="add $v1, "+quad[3]+" "+quad[2]+" \n";
    string+="lw " +quad[1]+ " 0($v1)\n";
    return string;


def mipsFuncDef(quad,key):
    string=str(quad[1])+":\n";
    if(quad[2]!="_"):
        string+="lw "+quad[2]+",($sp)\n";
        string+="addu $sp,$sp,4\n";
    string+="subu $sp,$sp,4\n";
    string+="sw $ra 0($sp)\n";
    return string;


def mipsFunCall(quad,key):
    string="Label"+str(key)+" : ";
    if(quad[2]!="_"):
        string+="subu $sp,$sp,4\n";
        string+="sw "+quad[2]+",0($sp)\n";
    string+="jal "+quad[1]+"\n";
    string+="lw "+quad[3]+",($sp)\n";
    string+="addu $sp,$sp,4\n";
    return string;


def mipsReturn(quad,key):
    string="Label"+str(key)+" : ";
    if(quad[1]!="_"):
        string+="lw $ra 0($sp)\n";
        string+="addu $sp,$sp,4\n";
        string+="subu $sp,$sp,4\n";
        string+="sw "+quad[1]+",0($sp)\n";
    else:
        string+="lw $ra 0($sp)\n";
        string+="addu $sp,$sp,4\n";
    string+="jr $ra\n"
    return string;


def mipsExit():
    string="li $v0 10\n"
    string+="syscall\n"
    return string;
    



if __name__== '__main__':
    main();
