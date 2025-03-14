executar = True
while executar :
    escolhas = '''
        [1] ou [+] para somar 
        [2] ou [-] para subtrair
        [3] ou [/] para dividir
        [4] ou [*] para multiplicar
        [5] para sair
        '''
    print(escolhas)
    operador = input("Qual sua opção?: ") 
    valor01 = input("Qual o primeiro valor? ")
    valor02 = input("Qual o segundo valor? ")

    valor01 = int(valor01)
    valor02 = int(valor02)

    texto_sair = '''
        [1] Não, desejo sair!
        [2] Sim, desejo realizar outro calculo   
    '''
    #Soma
    if operador == "1" or operador == "+" or operador == "Somar" :
        resultado = valor01 + valor02
        print("Resultado da soma: " + str(resultado))
        print(texto_sair)
        operador = input("Deseja realizar outro calculo? ")
        if operador == "1" :
           executar = False


    #Subtração
    if operador == "2" or operador == "Subtrair" or operador =="-":
        resultado = valor01 - valor02
        print("Resultado da subtração: " + str(resultado))
        print (texto_sair)
        operador = input("Deseja realizar outro calculo? ")
        if operador == "1" :
            executar = False

    #Divisão
    if operador =="3" or operador == "Divisão" or operador =="/":
        resultado = valor01 / valor02
        print("Resultado da divisão: " + str(resultado))
        print(texto_sair)
        operador = input("Deseja realizar outro calculo? ")
        if operador == "1":
            executar = False


    #Multiplicação
    if operador =="4" or operador == "Multiplicação" or operador =="*":
        resultado = valor01 / valor02
        print("Resultado da multiplicação: " + str(resultado))
        print(texto_sair)
        operador = input("Deseja realizar outro calculo? ")
        if operador == "1":
            executar = False

    
    #Sair
    if operador == "5" or operador == "Sair":
        print("obrigado!")
        executar = False
 





