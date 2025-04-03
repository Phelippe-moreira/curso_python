# configurações do nosso sistema!

# configurações dos caminhos dos arquivos e do database
caminho_banco = "C:/Users/integral/Desktop/phelippe/consumo_alcool.db"
caminho_drinks_csv = "C:/Users/integral/Desktop/phelippe/drinks.csv"

# Configurações do Flask
server_config = {
    "DEBUG" : True, 
    "PORT" : 5000,
    "HOST": "0.0.0.0" # pode ser localhost se desejar

}
# No debug podemos usar as seguintes configs:
# Debug como true ou False para ligar ou desligar o modo,
# ou como DEV e PROD
# Dev é a mesma coisa que Debug True, ou seja ambientes de desenvolvimento
# Prod é a mesma coisa que False, ou seja, debug desligado e ambiente de produção


# Outras configurações gerais
semente_aleatoria = 42
