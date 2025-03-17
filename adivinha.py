from random import randint

print("####  Iniciando o Jogo de Adivinhar  ###")

objetivo = randint(0,100)
chances = 5
tentativa = 0 

while tentativa != objetivo:
    tentativa = input("Chute um numero entre 0 e 100: ")
    if tentativa.isnumeric() :
        tentativa = int(tentativa)
        chances = chances - 1 
        if tentativa == objetivo:
            print("")
            print("Parabéns, você venceu! o número era {} e você tinha {} chances." . format(objetivo, chances))
            print("")
            break;
        else:
            print("")
            if tentativa > objetivo:
                print("Você errou, Dica é um numero menor. ")
            else:
                print("Você errou, Dica é um numero maior.")
            print("Você ainda possui {} chances".format(chances))
            print("")
        if chances == 0 :
            print("")
            print("Suas chances acabaram, você perdeu! ")
            print("") 
            break;   

print("#### Fim do Jogo  ####")





        
