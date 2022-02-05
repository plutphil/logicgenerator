truthtable = {
    "inputs":2,
    "outputs":1
}
trainingdata=[
    [[0,0],[0]],
    [[0,1],[1]],
    [[1,0],[1]],
    [[1,1],[0]]
]
class Node:
    def __init__(s,a,b):
        s.a=a
        s.b=b
        s.n=False
    def get(s):
        return (s.a.get()|s.b.get())^s.n
    def str(s):
        return ("!"if s.n else "")+"("+s.a.str()+"|"+s.b.str()+")"
class InputNode(Node):
    def __init__(s,name=""):
        s.val=False
        s.name=name
        pass
    def get(s):
        return s.val
    def str(s):
        return str(s.name)
def createnet(cin,cout):
    layers=[]
    layer=[]
    inputnodes=[]
    outputnodes=[]
    for i in range(cin):
        inputnodes.append(InputNode("i"+str(i)))
    while(len(layer)!=cout):
        for i in range(cin-1):
            layer.append(Node(inputnodes[i],inputnodes[i+1]))
    outputnodes=layer
    return {"layers":layers,"inputs":inputnodes,"outputs":outputnodes}
def createnet2(cin,cout,nonce):
    layers=[]
    layer=[]
    inputnodes=[]
    outputnodes=[]
    for i in range(cin):
        inputnodes.append(InputNode("i"+str(i)))
    currentnode=None
    for i in range(int(nonce/len(inputnodes))):
        if currentnode==None:
            currentnode=inputnodes[(i+nonce)%len(inputnodes)]
        else:
            currentnode=Node(currentnode,inputnodes[(i+nonce)%len(inputnodes)])
            layer.append(currentnode)
    layers.append(layer)
    return {"layers":layers,"inputs":inputnodes,"outputs":[currentnode]}
    
def testnet(net):
    testi=0
    failedtests=0
    for i in trainingdata:
        line = "test "+str(testi)+" "
        testi+=1
        for x in range(len(i[0])):
            net["inputs"][x].val=i[0][x]
            line += ("1"if i[0][x]else"0")
        failed = False
        line+=" "
        for x in range(len(i[1])):
            line+= ("1"if i[1][x]==1 else"0")
        line+=" "
        for x in range(len(i[1])):
            line+= ("1"if net["outputs"][x].get()else"0")
            if net["outputs"][x].get()==1 != i[1][x]:
                failed=True
        if failed:
            failedtests+=1
        line+=" failed"if failed else ""
        print(line)
    return failedtests
#net = createnet(2,1)  
net=createnet2(2,1,6)

def tryallcombinations(net):
    allnodes = []
    for layer in net["layers"]:
        for n in layer:
            allnodes.append(n)
    for n in net["outputs"]:
        allnodes.append(n)
    for i in range(2**len(allnodes)):
        for x in range(len(allnodes)):
            allnodes[x].n=(i>>x)&1
        print("iteration "+str(i))
        if testnet(net)==0:
            print("successful iteration!!!")
            for n in net["outputs"]:
                print(n.str())
            #exit(0)
tryallcombinations(net)

print(net)