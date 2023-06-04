def compBinary(s1,s2):
    count = 0
    pos = 0
    for i in range(len(s1)):
        if s1[i] != s2[i]:
            count+=1
            pos = i
    if count == 1:
        return True, pos
    else:
        return False, None
def compBinarySame(term,number):
    for i in range(len(term)):
        if term[i] != '-':
            if term[i] != number[i]:
                return False

    return True
def combinePairs(group, unchecked):
    l = len(group) -1
    check_list = []
    next_group = [[] for x in range(l)]
    for i in range(l):
        for elem1 in group[i]:
            for elem2 in group[i+1]:
                b, pos = compBinary(elem1, elem2)
                if b == True:
                    check_list.append(elem1)
                    check_list.append(elem2)
                    new_elem = list(elem1)
                    new_elem[pos] = '-'
                    new_elem = "".join(new_elem)
                    next_group[i].append(new_elem)
    for i in group:
        for j in i:
            if j not in check_list:
                unchecked.append(j)

    return next_group, unchecked
def remove_redundant(group):
    new_group = []
    for j in group:
        new=[]
        for i in j:
            if i not in new:
                new.append(i)
        new_group.append(new)
    return new_group
def remove_redundant_list(list):
    new_list = []
    for i in list:
        if i not in new_list:
            new_list.append(i)
    return new_list
def check_empty(group):

    if len(group) == 0:
        return True

    else:
        count = 0
        for i in group:
            if i:
                count+=1
        if count == 0:
            return True
    return False
def find_prime(Chart):
    prime = []
    for col in range(len(Chart[0])):
        count = 0
        pos = 0
        for row in range(len(Chart)):
            if Chart[row][col] == 1:
                count += 1
                pos = row

        if count == 1:
            prime.append(pos)

    return prime

def check_all_zero(Chart):
    for i in Chart:
        for j in i:
            if j != 0:
                return False
    return True
def find_max(l):
    max = -1
    index = 0
    for i in range(len(l)):
        if l[i] > max:
            max = l[i]
            index = i
    return index

class groupby:
    #def init(self, iterable, key=None):
    def __init__(self, iterable):
        #if key is None:
        #    key = lambda x: x
        #self.keyfunc = key
        self.it = iter(iterable)
        self.tgtkey = self.currkey = self.currvalue = object()
    def __iter__(self):
        return self
    def __next__(self):
        self.id = object()
        while self.currkey == self.tgtkey:
            self.currvalue = next(self.it)
            #self.currkey = self.keyfunc(self.currvalue)
            self.currkey = self.currvalue
        self.tgtkey = self.currkey
        return (self.currkey, self._grouper(self.tgtkey, self.id))
    def _grouper(self, tgtkey, id):
        while self.id is id and self.currkey == tgtkey:
            yield self.currvalue
            try:
                self.currvalue = next(self.it)
            except StopIteration:
                return
            #self.currkey = self.keyfunc(self.currvalue)
            self.currkey = self.currvalue

def multiplication(list1, list2):
    list_result = []
    if len(list1) == 0 and len(list2)== 0:
        return list_result
    elif len(list1)==0:
        return list2
    elif len(list2)==0:
        return list1
    else:
        for i in list1:
            for j in list2:
                if i == j:
                    list_result.append(i)
                else:
                    list_result.append(list(set(i+j)))
        list_result.sort()
        return list(list_result for list_result,_ in groupby(list_result))
def petrick_method(Chart):
    P = []
    for col in range(len(Chart[0])):
        p =[]
        for row in range(len(Chart)):
            if Chart[row][col] == 1:
                p.append([row])
        P.append(p)
    for l in range(len(P)-1):
        P[l+1] = multiplication(P[l],P[l+1])
    P = sorted(P[len(P)-1],key=len)
    final = []
    min=len(P[0])
    for i in P:
        if len(i) == min:
            final.append(i)
        else:
            break
    return final
def find_minimum_cost(Chart, unchecked, n_var, varname):
    P_final = []
    essential_prime = find_prime(Chart)
    essential_prime = remove_redundant_list(essential_prime)
    if len(essential_prime)>0:
        s = "\nEssential Prime Implicants :\n"
        for i in range(len(unchecked)):
            for j in essential_prime:
                if j == i:
                    s= s+binary_to_letter(unchecked[i], n_var, varname)+' , '
        #print(s[:(len(s)-3)])
    for i in range(len(essential_prime)):
        for col in range(len(Chart[0])):
            if Chart[essential_prime[i]][col] == 1:
                for row in range(len(Chart)):
                    Chart[row][col] = 0
    if check_all_zero(Chart) == True:
        P_final = [essential_prime]
    else:
        P = petrick_method(Chart)
        P_cost = []
        for prime in P:
            count = 0
            for i in range(len(unchecked)):
                for j in prime:
                    if j == i:
                        count = count+ cal_efficient(unchecked[i])
            P_cost.append(count)
        for i in range(len(P_cost)):
            if P_cost[i] == min(P_cost):
                P_final.append(P[i])
        for i in P_final:
            for j in essential_prime:
                if j not in i:
                    i.append(j)
    return P_final
def cal_efficient(s):
    count = 0
    for i in range(len(s)):
        if s[i] != '-':
            count+=1
    return count
'''
def binary_to_letter(s):
    out = ''
    c = 'a'
    more = False
    n = 0
    for i in range(len(s)):
        if more == False:
            if s[i] == '1':
                out = out + c
            elif s[i] == '0':
                out = out + c + '\''
        if more == True:
            if s[i] == '1':
                out = out + c + str(n)
            elif s[i] == '0':
                out = out + c + str(n) + '\''
            n+=1
        if c=='z' and more == False:
            c = 'A'
        elif c=='Z':
            c = 'a'
            more = True

        elif more == False:
            c = chr(ord(c)+1)
    return out
'''
def binary_to_letter(s, varcount, varname='x'):
    out = ''
    counter = varcount - 1
    varname = chr(ord(varname) - 32)#varname.capitalize()
    c = varname + str(counter)
    more = False
    n = 0
    for i in range(len(s)):
        if more == False:
            if s[i] == '1':
                out = out + ('*' if len(out) > 0 else '') + c
            elif s[i] == '0':
                out = out + ('*' if len(out) > 0 else '') + c + '\''
        if more == True:
            if s[i] == '1':
                out = out + ('*' if len(out) > 0 else '') + c + str(n)
            elif s[i] == '0':
                out = out + ('*' if len(out) > 0 else '') + c + str(n) + '\''

            n+=1
        if c=='z' and more == False:
            c = 'A'
        elif c=='Z':
            c = 'a'
            more = True

        elif more == False:
            counter = counter - 1
            c = varname + str(counter) #chr(ord(c)+1)
    return out
def getPot(x):
    i = 1
    for u in range(x):
        i = i * 2
    return i

def getKVMap(size):
    field = []

    if size == 64:
        field = [0,1,5,4,24,25,21,20,2,3,7,6,26,27,23,22,12,13,17,16,36,37,33,32,10,11,15,14,34,35,31,30,50,51,55,54,74,75,71,70,52,53,57,56,76,77,73,72,42,43,47,46,66,67,63,62,40,41,45,44,64,65,61,60]
    elif size == 32:
        field = [0,1,5,4,24,25,21,20,2,3,7,6,26,27,23,22,12,13,17,16,36,37,33,32,10,11,15,14,34,35,31,30]
    elif size == 16:
        field = [0,1,5,4,2,3,7,6,12,13,17,16,10,11,15,14]
    elif size == 8:
        field = [0,1,5,4,2,3,7,6]
    elif size == 4:
        field = [0,1,2,3]
    return field

def getKVSize(fieldSize):
    for i in range(fieldSize):
        for j in range(fieldSize):
            if i * j == fieldSize and (i == j * 2 or i * j == i * i):
                return i, j

def freeName(varname, offset):
    n = chr(ord('A')+offset)
    if n == varname:
        return chr(ord(n)+1)
    return n

def createDiagram(inputCount, minterms, minimizedTerms, dcMinterms, shouldCNF, varname='x'):
    if inputCount < 2:
        return

    fieldSize = 4
    for i in range(inputCount - 2):
        fieldSize = fieldSize * 2

    if fieldSize > 64:
        return

    varname = chr(ord(varname) - 32)

    kvmap = getKVMap(fieldSize)

    #########DEFAULT###########
    field = []

    for i in range(fieldSize):
        field.append(0)

    mintermsNormalized = []
    for i in range(len(minterms)):
        mintermsNormalized.append(int(minterms[i], 2))

    for i in range(len(kvmap)):
        if int(str(kvmap[i]), 8) in mintermsNormalized:
            field[i] = 1 

    #print('###')
    #print(mintermsNormalized)
    #print('###')
    #print(field)
    #########FOR DON'T CARES###########
    dcField = []

    for i in range(fieldSize):
        dcField.append(0)

    dcMintermsNormalized = []
    for i in range(len(dcMinterms)):
        dcMintermsNormalized.append(int(dcMinterms[i], 2))

    for i in range(len(kvmap)):
        if int(str(kvmap[i]), 8) in dcMintermsNormalized:
            dcField[i] = 1

    #print('###')
    #print(dcMintermsNormalized)
    #print('###')
    #print(dcField)

    #print(minterms)
    #print(mintermsNormalized)
    #print(kvmap)
    #print(field)

    fieldBackup = field.copy()

    width, height = getKVSize(fieldSize)
    
    X0 = [False, True, True, False] # left to right
    X1 = [False, True, True, False] # up to down
    X2 = [False, False, True, True, True, True, False, False] # left to right
    X3 = [False, False, True, True, True, True, False, False] # up to down
    X4 = [False, False, False, False, True, True, True, True] # left to right
    X5 = [False, False, False, False, True, True, True, True] # up to down
    minimizedTermsAsList = minimizedTerms.split(' + ')

    stackingLetters = []
    for i in range(fieldSize):
        stackingLetters.append([])
    alphlet = []

    cnf = []
    for w in range(width):
        for h in range(height):
            slotX = [X0[w % len(X0)], X1[h % len(X1)], X2[w % len(X2)], X3[h % len(X3)], X4[w % len(X4)], X5[h % len(X5)]]
            
            if field[h * width + w] == 1:
                for term in minimizedTermsAsList:
                    slots = term.split('*')
                    countTarget = len(slots)
                    counts = 0

                    for slot in slots:
                        for i in range(len(slotX)):
                            if varname + str(i) in slot and "'" in slot and not slotX[i] or varname + str(i) in slot and not "'" in slot and slotX[i]:
                                counts = counts + 1
                                break

                    if counts >= countTarget:
                        name = freeName(varname, minimizedTermsAsList.index(term))
                        field[h * width + w] = name if field[h * width + w] == 1 else '#'
                        stackingLetters[h * width + w].append(name)
                    elif not minimizedTerms:
                        field[h * width + w] = '&'

                if len(dcMinterms) > 0:
                    #print(dcField[h * width + w])
                    #print(field[h * width + w])
                    if dcField[h * width + w] == 1 and field[h * width + w] != '#':

                        if field[h * width + w] != 1:
                            alphlet.append(field[h * width + w])

                        field[h * width + w] = 'X' #TODO: I did not check if this letter is used regulary!
                        fieldBackup[h * width + w] = 'X'
                    
            else:
                s = ''
                s = s + '('
                for i in range(inputCount):
                    s = s + varname + str(i) + ("'" if slotX[i] else '') + ('+' if i < inputCount - 1 else '')
                s = s + ')*'
                cnf.append(s)

    for l in alphlet:
        for i in range(len(stackingLetters)):
            for u in range(len(stackingLetters[i])):
                if stackingLetters[i][u] == l:
                    stackingLetters[i][u] = 'X'

    formattedStackingLetters = []
    for w in range(width):
        for h in range(height):
            if len(stackingLetters[h * width + w]) > 1:
                formattedStackingLetters.append(str(h+1) + ',' + str(w+1) + ': ' + str(stackingLetters[h * width + w]))


    if shouldCNF:
        lastvar = cnf[len(cnf) - 1]
        cnf[len(cnf) - 1] = lastvar[:len(lastvar)-1]

        print('\n-- Long CNF Answers --')
        if len(cnf) > 0:
            lastvar = cnf[len(cnf) - 1]
            cnf[len(cnf) - 1] = lastvar[:len(lastvar)-1]
            printTermList(cnf)
        else:
            print('1')

    print('\n-- KV --')
    printField(makeDisplayField(fieldBackup, fieldSize))

    print('\n-- Marked KV --')
    #for term in minimizedTermsAsList:
    #    print(freeName(varname, minimizedTermsAsList.index(term)) + ': ' + term)
    printField(makeDisplayField(field, fieldSize))
    printTermList(formattedStackingLetters)

def printTermList(array):
    for term in array:
        print(term) 
    #print() 
    

def makeDisplayField(field, fieldSize):
    width, height = getKVSize(fieldSize)
    displayArray = []

    line = '  '
    for i in range(width):
        line = line + str(i+1) + ' '
        
    displayArray.append(line)

    for i in range(height):
        line = str(i + 1) + " "
        for j in range(width):
            line = line + str(field[i * width + j]) + "|"
        displayArray.append(line)
    return displayArray

def printField(field):
    for i in range(len(field)):
        print(field[i])
    #print()

def dckv(dcList, varname):
    a = dcList
    arr = []
    for i in range(len(a)):
        arr.append("")
    n_var = len(bin(len(a) - 1)[2:])
    counter = 0
    rev = False
    for u in range(n_var):
        counter = 0
        rev = False
        for i in range(len(a)):
            if counter < getPot(u) and not rev:
                if a[i] != "0":
                    arr[i] = "0" + arr[i]
                counter = counter + 1

            if counter > 0 and rev:
                if a[i] != "0":
                    arr[i] = "1" + arr[i]
                counter = counter - 1

            if counter >= getPot(u) and not rev:
                rev = True

            if counter == 0 and rev:
                rev = False
    a = []

    #dcList = []
    #for i in range(len(arr)):
    #    if arr[i].count('x') > 0:
    #        arr[i][len(arr[i])-1] = '1'

    for i in range(len(arr)):
        if arr[i]:
            a.append(arr[i])
    #for i in range(len(a)):
    #    print(a[i])
    for i in range(len(a)):
        a[i] = int(a[i], 2)
    a = map(int, a)
    group = [[] for x in range(n_var+1)]
    a = list(a)
    for i in range(len(a)):
        a[i] = bin(a[i])[2:]
        if len(a[i]) < n_var:
            for j in range(n_var - len(a[i])):
                a[i] = '0'+ a[i]
        elif len(a[i]) > n_var:
            print('\nError : Choose the correct number of variables(bits)\n')
            return
        index = a[i].count('1')
        group[index].append(a[i])
    all_group=[]
    unchecked = []
    while check_empty(group) == False:
        all_group.append(group)
        next_group, unchecked = combinePairs(group,unchecked)
        group = remove_redundant(next_group)

    s = "\nPrime Implicants :\n"
    for i in unchecked:
        s= s + binary_to_letter(i, n_var, varname) + " , "
    #print(s[:(len(s)-3)])
    Chart = [[0 for x in range(len(a))] for x in range(len(unchecked))]

    for i in range(len(a)):
        for j in range (len(unchecked)):
            if compBinarySame(unchecked[j], a[i]):
               Chart[j][i] = 1
    primes = find_minimum_cost(Chart, unchecked, n_var, varname)
    primes = remove_redundant(primes)
    s=''
    k=''
    for prime in primes:
        s=''
        k=''
        for i in range(len(unchecked)):
            for j in prime:
                if j == i:
                    s = s + binary_to_letter(unchecked[i], n_var, varname) + ' + '
                    k = k + binary_to_letter(unchecked[i], n_var, varname) + ' + \n'
        #print(s[:(len(s)-3)])
    #createDiagram(n_var, a, s[:(len(s)-3)], varname)
    if len(k[:(len(k)-3)].replace(' ', '')) < 1:
        return '1'

    return k[:(len(k)-3)]

def kv(minterms, shouldCNF, varname):
    a = list(minterms)
    arr = []
    
    ##############
    dcm = []
    #print(minterms)
    hasDC = False
    
    for i in a:
        if i != 'X':
            dcm.append('0')
        else:
            hasDC = True
            dcm.append('1')
    
    dnfIntersection = ''
    if hasDC == True:
        #print(dcm)
        #print(len(dcm) > 0)
        dnfIntersection = dckv(dcm, varname)

    #print(dcm)
    #print(len(dcm) > 0)
    #print(dnfIntersection)
    ##############

    for i in range(len(a)):
        arr.append("")
    n_var = len(bin(len(a) - 1)[2:])
    print("INPUTS: " + str(n_var))
    counter = 0
    rev = False
    for u in range(n_var):
        counter = 0
        rev = False
        for i in range(len(a)):
            if counter < getPot(u) and not rev:
                if a[i] != "0":
                    arr[i] = "0" + arr[i]
                counter = counter + 1

            if counter > 0 and rev:
                if a[i] != "0":
                    arr[i] = "1" + arr[i]
                counter = counter - 1

            if counter >= getPot(u) and not rev:
                rev = True

            if counter == 0 and rev:
                rev = False
    a = []

    for i in range(len(arr)):
        if arr[i]:
            a.append(arr[i])

    dcMinterms = []
    #print(a)
    minList = list(minterms)
    for i in a:
        ival = int(i, 2)
        if minList[ival].count('X') > 0:
            dcMinterms.append(i)
    #print(dcMinterms)

    '''
    for i in range(len(a)):
        eee = a[i]
        print(eee[len(eee)-1])
        if a[i][len(a[i])-1] == 'x':
            dcMinterms.append(a[i][:len(a[i])-1] + '1')
            a[i] = a[i][:len(a[i])-1] + '1'
        else:
            dcMinterms.append(a[i][:len(a[i])-1] + '0')
    '''

    #for i in range(len(a)):
    #    print(a[i])
    for i in range(len(a)):
        a[i] = int(a[i], 2)
    a = map(int, a)
    group = [[] for x in range(n_var+1)]
    a = list(a)
    for i in range(len(a)):
        a[i] = bin(a[i])[2:]
        if len(a[i]) < n_var:
            for j in range(n_var - len(a[i])):
                a[i] = '0'+ a[i]
        elif len(a[i]) > n_var:
            print('\nError : Choose the correct number of variables(bits)\n')
            return
        index = a[i].count('1')
        group[index].append(a[i])
    all_group=[]
    unchecked = []
    while check_empty(group) == False:
        all_group.append(group)
        next_group, unchecked = combinePairs(group,unchecked)
        group = remove_redundant(next_group)

    s = "\nPrime Implicants :\n"
    for i in unchecked:
        s= s + binary_to_letter(i, n_var, varname) + " , "
    #print(s[:(len(s)-3)])
    Chart = [[0 for x in range(len(a))] for x in range(len(unchecked))]

    for i in range(len(a)):
        for j in range (len(unchecked)):
            if compBinarySame(unchecked[j], a[i]):
               Chart[j][i] = 1
    primes = find_minimum_cost(Chart, unchecked, n_var, varname)
    primes = remove_redundant(primes)
    s=''
    k=''
    for prime in primes:
        s=''
        k=''
        for i in range(len(unchecked)):
            for j in prime:
                if j == i:
                    s = s + binary_to_letter(unchecked[i], n_var, varname) + ' + '
                    k = k + binary_to_letter(unchecked[i], n_var, varname) + ' + \n'
        #print(s[:(len(s)-3)])

    createDiagram(n_var, a, s[:(len(s)-3)], dcMinterms, shouldCNF, varname)
    print("\n-- Min DNF Answers --")

    res = k[:(len(k)-3)]

    if hasDC == True:
        res = res.replace(dnfIntersection, '')

    if len(res.replace(' ', '')) < 1:
        print('1')
    else:
        print(res)

def nextJK(before, after):
    if before == '0' and after == '0':
        return '0|X'
    if before == '0' and after == '1':
        return '1|X'
    if before == '1' and after == '0':
        return 'X|1'
    if before == '1' and after == '1':
        return 'X|0'
    print('Error in nextJK')
    exit()

def nextD(after):
    return after

def nextT(before, after):
    return str(int(before) ^ int(after))

def nextRSNor(before, after):
    if before == '0' and after == '0':
        return '1|0'
    if before == '0' and after == '1':
        return '0|X'
    if before == '1' and after == '0':
        return 'X|0'
    if before == '1' and after == '1':
        return '0|1'
    print('Error in nextRSNor')
    exit()

def nextRSNand(before, after):
    if before == '0' and after == '0':
        return '1|0'
    if before == '0' and after == '1':
        return 'X|1'
    if before == '1' and after == '0':
        return '1|X'
    if before == '1' and after == '1':
        return '0|1'
    print('Error in nextRSNor')
    exit()

def maw(prepInput, inputCount):
    print('USE INPUT FORMAT: 001122')
    print ('!!Just type number after number!!')
    uinput = input('0=D, 1=T, 2=JK, 3=NSNor, 4=NSNand\nDefine FF columns: ')
    #if not uinput:
    #    return
    ffoutList = list(uinput)
    ffCount = len(ffoutList)
    outputCount = len(prepInput) #int(input('output count: '))
    custom = input('custom list?: ')
    outputsN = []
    outputsN1 = prepInput

    #for i in outputsN1:
    #    print(i)

    if custom:
        for i in range(outputCount):
            outputsN.append(list(input('Enter Q' + str(outputCount - i - 1) + '(n): ')))

    #columnPart = int(len(outputsN1[0]) / pow(2, inputCount))

    if not custom:
        for i in range(len(bin(len(outputsN1[0])-1)[2:])):
            outputsN.append([])
        
        for u in range(len(outputsN)):
            for i in range(len(outputsN1[0])):
                val = bin(i)[2:]
                while len(val) < len(outputsN):
                    val = '0' + val
                outputsN[u].append(list(val)[u])
                
        '''
        while len(outputsN) < outputCount:
            outputsN.append([])

        for i in range(len(outputsN1[0])):
            val = bin(i % columnPart)[2:]
            #while len(val) < outputCount:
            #    val = '0' + val

            outputsN1Length = len(bin(len(outputsN1[0])-1)[2:])

            while len(val) < outputsN1Length:
                val = '0' + val

            for u in range(outputCount):
                #a = val[u]
                #outputsN[u].append(a)
                a = val[u]
                if outputCount < outputsN1Length:
                    a = val[outputsN1Length - outputCount + u]
                outputsN[u].append(a)
        '''

    table = []
    for i in range(len(outputsN[0])):
        line = '|'
        for u in range(ffCount):
            if ffoutList[u] == '0':
                line = line + outputsN1[u % outputCount][i]#nextD(outputsN[len(outputsN) - len(outputsN1) + u % outputCount][i])
            elif ffoutList[u] == '1':
                line = line + nextT(outputsN[len(outputsN) - len(outputsN1) + u % outputCount][i], outputsN1[u % outputCount][i])
            elif ffoutList[u] == '2':
                line = line + nextJK(outputsN[len(outputsN) - len(outputsN1) + u % outputCount][i], outputsN1[u % outputCount][i])
            elif ffoutList[u] == '3':
                line = line + nextRSNor(outputsN[len(outputsN) - len(outputsN1) + u % outputCount][i], outputsN1[u % outputCount][i])
            elif ffoutList[u] == '4':
                line = line + nextRSNand(outputsN[len(outputsN) - len(outputsN1) + u % outputCount][i], outputsN1[u % outputCount][i])
            line = line + '|'
        table.append(line)

    #for i in outputsN:
    #    print(i)

    #stateColumns = [] # or is it called rows? lol

    #at this point i am just lazy
    netRows = []
    netLines = []
    for i in range(len(outputsN[0])):
        line = ''
        for u in range(ffCount):
            if ffoutList[u] == '0':
                line = line + nextD(outputsN[len(outputsN) - len(outputsN1) + u % outputCount][i])
            elif ffoutList[u] == '1':
                line = line + nextT(outputsN[len(outputsN) - len(outputsN1) + u % outputCount][i], outputsN1[u % outputCount][i])
                #print(outputsN[u % outputCount][i])
            elif ffoutList[u] == '2':
                line = line + nextJK(outputsN[len(outputsN) - len(outputsN1) + u % outputCount][i], outputsN1[u % outputCount][i])
            elif ffoutList[u] == '3':
                line = line + nextRSNor(outputsN[len(outputsN) - len(outputsN1) + u % outputCount][i], outputsN1[u % outputCount][i])
            elif ffoutList[u] == '4':
                line = line + nextRSNand(outputsN[len(outputsN) - len(outputsN1) + u % outputCount][i], outputsN1[u % outputCount][i])
        netLines.append(line)

    for i in range(len(netLines[0])):
        netRows.append('')

    for i in range(len(netLines)):
        for u in range(len(netRows)):
            netRows[u] = netRows[u] + netLines[i][u]

    print('>>net state(n+1)<<')
    for i in range(len(table)):
        printStr = table[i] + ' '
        for u in range(len(outputsN1)):
            printStr = printStr + outputsN1[u][i] + '|'
        print(printStr[:len(printStr) - 1])

        #print(table[i] + '  ' + outputsN1[i])
    #for line in table:
    #    print(line)

    print('keep blanc for no skip')
    if input('skip kv?: '):
        return
    
    ## here logic and questions for kv input   
    print('Form: 1,12,24,...')
    kvColumnsIndexes = input('columns for kv:')
    while not kvColumnsIndexes:
        kvColumnsIndexes = input('columns for kv:')

    kvColumnsIndexes = list(map(int, kvColumnsIndexes.split(',')))

    shouldCNF = input('print cnfs?: ')
    if not shouldCNF:
        shouldCNF = False
    else:
        shouldCNF = True
    #kv(netRows + prepInput, shouldCNF)

    varname = input("kv input name?: ")
    if not varname:
        varname = 'q'

    allColumns = netRows + prepInput

    for el in allColumns:
        if el.count('|') > 0:
            allColumns.remove(el)

    #print(allColumns)
    for index in kvColumnsIndexes:
        kv(allColumns[index], shouldCNF, varname)

def atable():
    shouldDescription = int(input('Description? (1 = yes, 0 = no): '))
    if (shouldDescription == 1):
        print('Description:')
        print('This script generates n+1 table, flip-flip table, kv net, cnf and minimal dnf from a transition table.')
        print('You can use this script either via python or micropython like in a fx-cg50 calculator.')
        print('This script is experimental and may contain bugs and errors, but you can help to improve it.')
        print('Use at your own risk!')

    shouldHelp = int(input('help? (1 = yes, 0 = no): '))
    if (shouldHelp == 1):
        print ('Usage help:')
        print ('After you draw the (moore/etc) automat you need to create the transition table.')
        print ('Use the column count of n+1 as output count.')
        print ('You will then be asked to input one column after another from right to left.')
        print ("Press enter 2x. I don't even know what those options are anymore, lol.")
        print ('IMPORTANT for the next step is that you should not use comma seperation.')
        print ('If you have to calc some flip flops, choose your options for each column in the order left to right.')
        print('')

    outCount = int(input('output count: '))
    tableInput = []
    for i in range(outCount):
        tstr = input('Enter Z' + str(outCount - i - 1) + ': ')
        tstr = tstr.split(',')
        tstr = list(map(int, tstr))
        tableInput.append(tstr)

    extraBitsForLater = len(bin(outCount - 1)[2:])
    
    inputCount = input('inputs?: ')
    if inputCount:
        extraBitsForLater = int(inputCount)
    else:
        print('extra bits: ' + str(extraBitsForLater))

    maxval = []
    for i in range(len(tableInput)):
        maxval.append(max(tableInput[i]))
    maxval = max(maxval)

    #print(tableInput)

    binTableInput = []
    for i in range(len(tableInput)):
        for u in range(len(tableInput[0])):
            binval = bin(tableInput[i][u])[2:]
            #maxval = max(tableInput[i])
            while len(binval) < len(bin(maxval)[2:]):
                binval = '0' + binval
            binTableInput.append(binval)

    #print(binTableInput)

    print('TABLE FOR N+1:')
    for i in range(len(binTableInput)):
        printStr = ''
        for u in range(len(binTableInput[0])):
            printStr = printStr + binTableInput[i][u] + '|'
        print(printStr[:len(printStr)-1])

    preparedMAWInput = []
    for i in range(len(binTableInput[0])):
        linestr = ''
        for u in range(len(binTableInput)):
            linestr = linestr + binTableInput[u][i]
        preparedMAWInput.append(linestr)

    #print(preparedMAWInput)

    print('keep blanc for no skip')
    if input('skip maw?:'):
        return

    maw(preparedMAWInput, extraBitsForLater)

atable()