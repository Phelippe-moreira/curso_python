from flask import Flask, request, render_template_string
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.io as pio
import random

#configura o plotly para abrir os arquivos no navegador por padrão
pio.renderers.default = "browser"

#carregar o drinks.csv
df = pd.read_csv("C:/Users/integral/Desktop/phelippe/drinks.csv")
#df_avengers = pd.read_csv("avengers.csv")

#cria o banco de dados em sql e popular com os dados do arquivo csv
conn = sqlite3.connect("C:/Users/integral/Desktop/phelippe/consumo_alcool.db")
df.to_sql("drinks", conn, if_exists="replace", index=False)
#df_avengers.to_sql("Vingadores", conn, if_exists="replace", index=False)
conn.commit()
conn.close()

#incia o flask
app = Flask(__name__)

html_template = '''
    <h1>Dashboard - Consumo de Alcool</h1>
    <h2> Parte 01 </h2>
        <ul>
            <li> <a href="/grafico1"> Top 10 paises com maior consumo de alcool </a> </li>
            <li> <a href="/grafico2"> Média de consumo por tipo de bebida </a> </li>
            <li> <a href="/grafico3"> Consumo total por região </a> </li>
            <li> <a href="/grafico4"> Comparativo entre os tipos de bebidas </a> </li>
            <li> <a href="/pais?nome=Brazil"> Insight por pais (ex: Brazil) </a> </li>
        </ul>
    <h2> Parte 02 </h2>
        <ul>
            <li><a href="/comparar"> Comparar </a></li>
            <li><a href="/upload_avengers"> Upload do CSV </a></li>
            <li><a href="/apagar_avengers"> Apagar Tabela Avengers </a></li>
            <li><a href="/atribuir_paises_avengers"> Atribuir Paises </a></li>
            <li><a href="/ver_avengers"> Ver tabela Avengers </a></li>
            <li><a href="/consultar_avengers"> Consultar detalhes do Vingador </a></li>
            <li><a href="/avengers_vs_drinks"> V.A.A (Vingadores Alcolicos Anonimos) </a></li>
        </ul>

    '''

# rota inicial com o links para os graficos
@app.route('/')
def index():
    return render_template_string(html_template)

@app.route('/grafico1')
def grafico1():
    conn = sqlite3.connect("C:/Users/integral/Desktop/phelippe/consumo_alcool.db")
    df = pd.read_sql_query("""
    SELECT country, total_litres_of_pure_alcohol
    FROM drinks
    ORDER BY total_litres_of_pure_alcohol DESC
    LIMIT 10
    """, conn)
    conn.close()
    fig = px.bar(
        df,
        x="country",
        y="total_litres_of_pure_alcohol",
        title="Top 10 paises com maior consumo de Alcool"
    )
    return fig.to_html()

# media do consumo por tipo global
@app.route('/grafico2')
def grafico2():
    conn = sqlite3.connect("C:/Users/integral/Desktop/phelippe/consumo_alcool.db")
    df = pd.read_sql_query("SELECT AVG(beer_servings) AS cerveja, AVG(spirit_servings) AS destilados, AVG(wine_servings) AS vinhos FROM drinks", conn)
    conn.close()
    df_melted = df.melt(var_name="Bebidas", value_name="Média de Porções")
    fig = px.bar(df_melted, x="Bebidas", y="Média de Porções", title="Media de consumo global por tipo")
    return fig.to_html()

@app.route('/grafico3')
def grafico3():
    # Define grupos de paises por região (simulando)
    regioes = {
        "Europa": ["France", "Germany", "Italy", "Spain", "Portugal", "UK"],
        "Asia":  ["China","Japan","India","Thailand"],
        "Africa":  ["Angola","Nigeri a","Egypt","Algeria"],
        "Americas":  ["USA","Brazil","Canada","Argentina","Mexico"]
    }
    dados = []
    conn = sqlite3.connect("C:/Users/integral/Desktop/phelippe/consumo_alcool.db")
    for regiao, paises in regioes.items():
        placeholders = ",".join([f"'{p}'" for p in paises])
        query =  f"""
            SELECT SUM(total_litres_of_pure_alcohol) as total FROM drinks WHERE country IN ({placeholders})
        """
        total = pd.read_sql_query(query, conn)[0] or 0
        dados.append({"Região": regiao, "Consumo Total":total})
    conn.close()
    df_regioes = pd.DataFrame(dados)
    fig = px.pie(df_regioes, names="Região", values="Consumo Total", title="Consumo total por região do mundo")
    return fig.to_html() +"<br/><a href='/'>Voltar ao Inicio</a>"

@app.route('/grafico4')
def grafico4():
    conn = sqlite3.connect("C:/Users/integral/Desktop/phelippe/consumo_alcool.db")
    df = pd.read_sql_query ('SELECT beer_servings, spirit_servings, wine_servings FROM drinks', conn)
    conn.close()
    medias = df.mean().resert_index()
    medias.columns = ["Tipo", "Média"]
    fig = px.pie(medias, names="Tipo", values="Média", title="Proporção média entre tipos de bebidas")
    return fig.to_html() + '<br><a href="/">Voltar ao inicio</a>'

@app.route('/comparar', methods=['GET','POST'])
def comparar():
    opcoes=['beer_servings','spirit_servings','wine_servings','total_litres_of_pure_alcohol']

    if request.method == 'POST':
        eixo_x = request.form.get('eixo_x')
        eixo_y = request.form.get('eixo_y')
        
        if eixo_x == eixo_y: 
            return "<h3> Selecione Variáveis Diferentes!.</h3>"

        conn = sqlite3.connect("C:/Users/integral/Desktop/phelippe/consumo_alcool.db") 
        df = pd.read_sql_query('SELECT country, {}, {} FROM drinks'.format(eixo_x,eixo_y), conn)
        conn.close()

        fig = px.scatter(df, x=eixo_x, y= eixo_y, title=f'Comparação entre {eixo_x} e {eixo_y}')
        fig.update_traces(textposition='top center') 
        return fig.to_html() + "<br><a href='/'>Voltar ao Inicio</a>" 


    return render_template_string('''
    <h2>Comparar Campos</h2>
    <form method='POST'> 
        <label for='eixo_x'> Eixo X: </label> 
        <select name='eixo_x'> 
            {% for col in opcoes %}                 
                <option value='{{ col }}'> {{ col }} </option>                  
            {% endfor %} 
         </select><br><br>


    <label for='eixo_y'> Eixo Y: </label> 
        <select name='eixo_y'> 
            {% for col in opcoes %}                 
               <option value='{{ col }}'> {{ col }} </option>                  
            {% endfor %} 
         </select><br><br>

         <input type='submit' value='--Comparar--'> 
                           
    </form>                           
''', opcoes=opcoes)


@app.route('/upload_avengers', methods=['GET','POST'])
def upload_avenger():
    if request.method == 'POST':
        file = request.files['file']
        if not file:
            return "<h3>Nenhum arquivo enviado</h3><br><a href='/upload_avengers'>Voltar ao Inicio</a>"
        df_avengers = pd.read_csv(file,encoding='latin1')
        conn = sqlite3.connect("C:/Users/integral/Desktop/phelippe/consumo_alcool.db") 
        df_avengers.to_sql('avengers', conn, if_exists='replace', index=False)
        conn.commit()
        conn.close()
        return "<h3>Arquivo inserido com sucesso!</h3><a href='/'>Voltar</a>"
    return '''
    <h2>Upload do arquivo Avengers</h2>
    <form method='POST' enctype='multipart/form-data'>
        <input type='file' name='file' accept=".csv"><br>
        <input type='submit' value="-- Enviar --">
    </form>
'''
        
         
@app.route('/apagar_avengers')  
def apagar_avengers():
    conn = sqlite3.connect("C:/Users/integral/Desktop/phelippe/consumo_alcool.db")   
    cursor = conn.cursor()

    try:
      cursor.execute("DROP TABLE IF EXISTS avengers") 
      conn.commit()
      mensagem = "<h3>Tabela 'avengers' apagada com sucesso! </h3>"


    except Exception as errinho:    
      mensagem = f"<h3>Erro ao apagar a tabela:{str(errinho)} </h3>"   
    
    conn.close()
    return mensagem + "<br><hr><a href='/'>Voltar ao Inicio</a>"


@app.route('/atribuir_paises_avenger')
def atribuir_paises_avenger():
    conn = sqlite3.connect("C:/Users/integral/Desktop/phelippe/consumo_alcool.db")
    df_avengers = pd.read_sql_query("SELECT * FROM avengers", conn)
    df_drinks = pd.read_sql_query("SELECT country FROM drinks", conn)

    random.seed(42)
    paises_possiveis = df_drinks["country"].unique()
    df_avengers["country"] = [random.choice(paises_possiveis) for _ in range(len(df_avengers))]

    df_avengers.to_sql("avengers", conn, if_exists="replace", index=False)
    conn.commit()
    conn.close()

    return "<h3>Paises Atribuidos aos Vingadores com sucesso !</h3><br><hr><br><a href='/'>Voltar ao Inicio</a>"


@app.route('/ver_avengers')
def ver_avengers():
    conn = sqlite3.connect("C:/Users/integral/Desktop/phelippe/consumo_alcool.db")
    try: df_avengers = pd.read_sql_query("SELECT * FROM avengers", conn)  
    except Exception as e:
        conn.close()
        return f"<h3>Erro ao consultar a tabela: {str(e)}</h3></h3><br><hr><br><a href='/'>Voltar ao Inicio</a>"
    conn.close() 

    if df_avengers.empty:
        return "<h3>A tabela 'avengers' esta vazia ou não existe</h3><br><a href='/'>Voltar ao inicio</a>" 
    
    return df_avengers.to_html(index=False) + "<br><a href='/'>Voltar ao inicio</a>" 


@app.route('/consultar_avenger')
def consultar_avenger():
    conn =sqlite3.connect("C:/Users/integral/Desktop/phelippe/consumo_alcool.db")
    df_avengers = pd.read_sql_query("SELECT * FROM avengers", conn)
    conn.close()

    #vamos continuar daqui!










# inicia o servidor flask
if __name__ == "__main__":
    app.run(debug=True)

