import DustyDevilLexerGarcia

#while True:
    #text = input('DustyDevilLexerGarcia > ')
text = open("DustyDevil.in.txt", "r")
text = text.read()
result, error = DustyDevilLexerGarcia.run("DustyDevil.in.txt", text)


#Print to screen

if error: print(error.as_string())
else: print(result)

#Print to file

sourceFile = open("DustyDevil.out.txt", 'w')
if error: print(error.as_string(), file = sourceFile)
else: print(result, file = sourceFile)
sourceFile.close()