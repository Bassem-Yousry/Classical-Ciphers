import numpy as np


def input_file(name):
    rf = open(name, 'r')
    line = rf.read()
    lines = line.splitlines()
    rf.close()
    return lines


def output_file(name, content):
    with open(name, 'w') as wf:
        for l in content:
            wf.write(l)
            wf.write('\n')
    wf.close()


def HillCipher2_2(text, key):
    PList = list()
    PList[:0] = text.upper().replace(" ", "")
    if len(PList) % 2 == 1:
        PList.append('X')
    KeyMatrix = np.array([[key[0], key[1]], [key[2], key[3]]])
    i = 0
    Encr = []
    while i < len(PList):
        TextMatrix = np.array([[ord(PList[i]) - 65], [ord(PList[i + 1]) - 65]])
        Result = np.dot(KeyMatrix, TextMatrix)
        Result %= 26
        Result = Result.flatten().tolist()
        Encr.append(chr(65 + int(Result[0])))
        Encr.append(chr(65 + int(Result[1])))
        i += 2
    return "".join(Encr)


def HillCipher3_3(text, key):
    # KeyMatrix=[[1,2,3],[4,5,6],[7,8,9]]
    PList = list()
    PList[:0] = text.upper().replace(" ", "")
    while len(PList) % 3 != 0:
        PList.append('X')
    key = np.reshape(key, (-1, 3))
    KeyMatrix = np.array(key)
    i = 0
    Encr = []
    while i < len(PList):
        TextMatrix = np.array([[ord(PList[i]) - 65], [ord(PList[i + 1]) - 65], [ord(PList[i + 2]) - 65]])
        Result = np.dot(KeyMatrix, TextMatrix)
        Result %= 26
        Result = Result.flatten().tolist()
        Encr.append(chr(65 + int(Result[0])))
        Encr.append(chr(65 + int(Result[1])))
        Encr.append(chr(65 + int(Result[2])))
        i += 3
    return "".join(Encr)


def CaesarCipher(text, key):
    EncText = str()
    for l in text:
        if l >= 'a' and l <= 'z':
            EncText += chr(((ord(l) - ord('a') + key) % 26) + ord('a'))
        elif l >= 'A' and l <= 'Z':
            EncText += chr(((ord(l) - ord('A') + key) % 26) + ord('A'))
    return EncText


def VigenereCipher(text, key, mode):
    text = text.upper().replace(" ", "")
    key = key.upper().replace(" ", "")
    # 0        ---> repeating mode
    # else     ---> auto mode
    if not mode:
        if len(key) < len(text):
            Repeat = int(len(text) / len(key))
            key *= Repeat
            if len(key) < len(text):
                key += key[0:len(text) - len(key)]
    else:
        if len(key) < len(text):
            key += text[0:len(text) - len(key)]
    Encr = str()
    for i, L in enumerate(text):
        Encr += CaesarCipher(L, ord(key[i]) - 65)
    return Encr


def PlayFairCipher(text, key):
    KeyList = [[1, 2, 3, 4, 5],  # 5*5 KeyList
               [6, 7, 8, 9, 10],
               [11, 12, 13, 14, 15],
               [16, 17, 18, 19, 20],
               [21, 22, 23, 24, 25]]

    KList = []
    KList[:0] = key.upper().replace("J", "I").replace(" ", "")
    KList = list(dict.fromkeys(KList))  # remove redundancy
    row = 0
    column = 0
    for l in KList:  # add key's letters in keylist
        KeyList[row][column] = l
        column += 1
        if column == 5:
            column = 0
            row += 1
    Char = 'A'
    while row < 5:  # fill the keylist
        while Char in KList or Char == 'J':
            Char = chr(ord(Char) + 1)

        KeyList[row][column] = Char
        KList.append(Char)
        column += 1
        if column == 5:
            column = 0
            row += 1
    plainText = list()
    plainText[:0] = text.replace(" ", "").upper().replace('J', 'I')
    i = 0
    while i + 1 < len(plainText):  # If a pair is a repeated letter, insert ‘X’ as filler between the two characters
        if plainText[i] == plainText[i + 1]:
            plainText.insert(i + 1, 'X')
        i += 2
    if len(plainText) % 2 == 1:  # If there is a single trialing letter, attach ‘X’ to the end
        plainText.append('X')

    def GetCharIndex(Char, List):
        Row = 0
        Column = 0
        while Row < 5:
            if Char == List[Row][Column]:
                return Row, Column
            Column += 1
            if Column == 5:
                Column = 0
                Row += 1
        return 5, 5

    i = 0
    Encr = []
    while i < len(plainText):
        Index1 = GetCharIndex(plainText[i], KeyList)
        Index2 = GetCharIndex(plainText[i + 1], KeyList)
        if Index1[0] == Index2[0]:  # If both letters fall in the same row, replace each with letter to right
            Char1 = KeyList[Index1[0]][(Index1[1] + 1) % 5]
            Char2 = KeyList[Index2[0]][(Index2[1] + 1) % 5]
        elif Index1[1] == Index2[1]:  # If both letters fall in the same column, replace each with the letter below it
            Char1 = KeyList[(Index1[0] + 1) % 5][Index1[1]]
            Char2 = KeyList[(Index2[0] + 1) % 5][Index2[1]]
        else:  # Otherwise, each letter is replaced by the letter in the same row and in the column of the other letter of the pair.
            Xo = Index1[1]
            while Xo != Index2[1]:
                Xo = (Xo + 1) % 5
            Char1 = KeyList[Index1[0]][Xo]
            Xo = Index2[1]
            while Xo != Index1[1]:
                Xo = (Xo + 1) % 5
            Char2 = KeyList[Index2[0]][Xo]
        Encr.append(Char1)
        Encr.append(Char2)
        i += 2
    return "".join(Encr)


def VernamCipher(text, key):
    if len(text) == len(key):
        return VigenereCipher(text, key, 1)
    else:
        return "Error Key Length not equal to Text"


# --------------------------------------Caesar-------------------------------------------------
try:
    Lines = input_file('caesar_plain.txt')
    CaesarKeys = [3, 6, 12]
    CaesarOutput = []
    for n in CaesarKeys:
        CaesarOutput.append('Key=' + str(n) + '\n')
        for l in Lines:
            CaesarOutput.append(CaesarCipher(l, n))
        CaesarOutput.append('-----------------------------')

    output_file('caesar_cipher.txt', CaesarOutput)
except:
    print('caesar_plain.txt is not found')
# --------------------------------------PlayFair-------------------------------------------------
try:
    Lines = input_file('playfair_plain.txt')
    CaesarKeys = ["rats", "archangel"]
    CaesarOutput = []
    for n in CaesarKeys:
        CaesarOutput.append('Key=' + str(n) + '\n')
        for l in Lines:
            CaesarOutput.append(PlayFairCipher(l, n))
        CaesarOutput.append('-----------------------------')

    output_file('playfair_cipher.txt', CaesarOutput)
except:
    print('playfair_plain.txt is not found')
# --------------------------------------HillCipher 2*2-------------------------------------------------
try:
    Lines = input_file('hill_plain_2x2.txt')
    CaesarOutput = []
    for l in Lines:
        CaesarOutput.append(HillCipher2_2(l, [5, 17, 8, 3]))

    output_file('hill_cipher_2x2.txt', CaesarOutput)
except:
    print('hill_cipher_2x2.txt is not found')

# --------------------------------------HillCipher 3*3-------------------------------------------------
try:
    Lines = input_file('hill_plain_3x3.txt')
    CaesarOutput = []
    for l in Lines:
        CaesarOutput.append(HillCipher3_3(l, [2, 4, 12, 9, 1, 6, 7, 5, 3]))
    output_file('hill_cipher_3x3.txt', CaesarOutput)
except:
    print('hill_cipher_3x3.txt is not found')
# --------------------------------------VigenereCipher-------------------------------------------------
try:
    Lines = input_file('vigenere_plain.txt')
    CaesarOutput = []
    CaesarOutput.append("Key=PIE   &   Mode=Repeating\n")
    for l in Lines:
        CaesarOutput.append(VigenereCipher(l, 'PIE', 0))
    CaesarOutput.append('-----------------------------')
    CaesarOutput.append("\nKey=AETHER   &   Mode=Auto\n")
    for l in Lines:
        CaesarOutput.append(VigenereCipher(l, 'aether', 1))
    output_file('vigenere_cipher.txt', CaesarOutput)
except:
    print('vigenere_plain.txt is not found')
# --------------------------------------VernamCipher-------------------------------------------------
try:
    Lines = input_file('vernam_plain.txt')
    CaesarOutput = []
    for l in Lines:
        CaesarOutput.append(VernamCipher(l, 'SPARTANS'))
    output_file('vernam_cipher.txt', CaesarOutput)
except:
    print('vernam_plain.txt is not found')

try:
    while True:
        PlainText = (input('\ntype the plain text:'))
        CaesarKey = int(input('Enter Caesar Key:'))
        PF_Key = (input('Enter PlayFair Key:'))
        Hill2_2 = (input('Enter HillCipher_2x2 array of int separated by space : '))
        Hill2_2 = Hill2_2.split()
        Hill2_2=list(map(int, Hill2_2))
        Hill3_3 = (input('Enter HillCipher_3x3 array of int separated by space : '))
        Hill3_3 = Hill3_3.split()
        Hill3_3=list(map(int, Hill3_3))
        VigenereKM = (input('Enter Vigenere Key and mode separated by space : '))
        VigenereKM = VigenereKM.split()
        VigenereKey = VigenereKM[0]
        VigenereMode = int(VigenereKM[1])
        VernamKey = (input('Enter Vernam Key : '))
        print("\nCaesarCipher = "+str(CaesarCipher(PlainText,CaesarKey)))
        print("PlayFair = "+str(PlayFairCipher(PlainText,PF_Key)))
        print("HillCipher2x2 = "+str(HillCipher2_2(PlainText,Hill2_2)))
        print("HillCipher3x3 = "+str(HillCipher3_3(PlainText,Hill3_3)))
        print("VigenereCipher = "+str(VigenereCipher(PlainText,VigenereKey,VigenereMode)))
        print("VernamOneTime = "+str(VernamCipher(PlainText,VernamKey)))
        print('\n')
except:
    print("invalid input")
