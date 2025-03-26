from flask import Flask, jsonify, send_file
import pandas as pd
import io
import base64
import matplotlib.pyplot as plt

# Criar o app do Flask
app = Flask(__name__)

# carregar os dados do excel

arquivo = 'C:/Users/integral/Desktop/phelippe/01_base_vendas.xlsx'
df1 = pd.read_excel(arquivo, sheet_name='Relatório de Vendas')
df2 = pd.read_excel(arquivo, sheet_name='Relatório de Vendas1')

# Concatenar as duas tabelas
df_consolidado = pd.concat([df1, df2], ignore_index=True)

#remove as duplicatas do dataframe
df_consolidado = df_consolidado.drop_duplicates()

#adiciona uma coluna de status com base no plano vendido
df_consolidado['Status'] = df_consolidado['Plano Vendido'].apply(lambda x : 'Premium' if x == 'Enterprise' else 'Padrão')

# rota da pagina inicial ex: http://127.0.0.1:5000/
@app.route('/')
def pagina_inicial():
    conteudo = '''
    <style>
        a {
            display: inline-block;
            padding: 10px 20px;
            margin: 5px 0;
            text-decoration: none;
            color: white;
            border-radius: 5px;
            text-align: center;
            background-color: #4CAF50;
            transition: 0.3s;
            min-width: 200px;
            min-height: 20px;
            }
        </style>    
        <h1>API de análise de dados de Vendas</h1>
        <h2>Use as rotas para obter análises:</h2>
        <a href=''> -- Pagina Inicial -- </a><br/>
        <a href='/clientes_por_cidade'> -- Clientes por Cidade -- </a><br/>
        <a href='/vendas_por_plano'> -- Vendas por Planos -- </a><br/>
        <a href='/top_cidades'> -- Top 3 Cidades -- </a><br/>
        <a href='/dowload/excel'> -- Download em Excel -- </a><br/>
        <a href='/dowload/csv'> -- Download em CSV -- </a><br/>
        <a href='/grafico_pizza'> -- Grafico de Pizza -- </a><br/>
        <a href='/grafico_barras'> -- Grafico de Barras -- </a><br/>
        <br/>
        <a href='mailto:phelippe.moreira@hotmail.com'> E-mail de contato </a>
        '''
    return conteudo

@app.route('/clientes_por_cidade')
def clientes_por_cidade():
    clientes_por_cidade = df_consolidado.groupby('Cidade')['Cliente'].nunique().sort_values(ascending=False)
    return jsonify(clientes_por_cidade.to_dict())


@app.route('/vendas_por_plano')
def vendas_por_plano():
    vendas_por_plano = df_consolidado['Plano Vendido'].value_counts()
    return jsonify(vendas_por_plano.to_dict())


@app.route('/top_cidades')
def top_cidades():
    clientes_por_cidade = df_consolidado.groupby('Cidade')['Cliente'].nunique().sort_values(ascending=False)
    top_cidades = clientes_por_cidade.head(3)
    return jsonify(top_cidades.to_dict())


@app.route('/dowload/csv')
def dowload_csv():
    caminho_csv = 'C:/Users/integral/Desktop/phelippe/arquivo_csv.csv'
    df_consolidado.to_csv(caminho_csv,index=False)
    return jsonify({'message':"Download do arquivo CSV disponível","file_path":caminho_csv,
    "Autor": "Phelippe"
    })
    


@app.route('/dowload/excel')
def dowload_excel():
    caminho_excel = 'C:/Users/integral/Desktop/phelippe/arquivo_csv.xlsx'
    df_consolidado.to_excel(caminho_excel,index=False)
    return f"<a> href='{caminho_excel}'>Iniciar Download </a>"
    


# Grafico de barras! 

@app.route('/grafico_barras')
def grafico_barras():
    vendas_por_plano = df_consolidado['Plano Vendido'].value_counts()

    #Criar o Grafico de Barras
    fig, ax = plt.subplots() #cria um objeto de figura para os eixos do grafico
    vendas_por_plano.plot(kind='bar', ax=ax , color=['#66b3ff','#00f0f0'])
    ax.set_title('Grafico de vendas por plano')
    ax.set_xlabel('Plano')
    ax.set_ylabel('Numero de vendas')

    # Salvar o grafico em um objeto de memória
    img = io.BytesIO() #cria em buffer de memoria e armazena a imagem
    plt.savefig(img, format='png') #salva a imagem em formato png dentro do buffer
    img.seek(0) #move o ponteiro para o inicio do buffer

    #converte a imagem em uma string codificada em padrão correto base64    
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')

    # retornando a imagem como resposta
    return send_file(img, mimetype='image/png')

@app.route('/grafico_pizza')
def grafico_torta():
    #conta a quantidade de cada status
    status_dist = df_consolidado['Status'].value_counts()

    #Criar o grafico de torta
    fig, ax = plt.subplots()
    ax.pie(
        status_dist,
        labels=status_dist.index, 
        autopct='%1.1f%%', 
        startangle=90,
        colors=['#C1B8B8','#00F545'] 
        )
    ax.axis('equal')
    
    # Salvar o grafico em um objeto de memória
    img = io.BytesIO() #cria em buffer de memoria e armazena a imagem
    plt.savefig(img, format='png') #salva a imagem em formato png dentro do buffer
    img.seek(0) #move o ponteiro para o inicio do buffer

    #converte a imagem em uma string codificada em padrão correto base64    
    img_base64 = base64.b64encode(img.getvalue()).decode('utf-8')

    # retornando a imagem como resposta
    return send_file(img, mimetype='image/png')





# Rodar a aplicação Flask
if __name__ == '__main__':
    app.run(debug=True)
