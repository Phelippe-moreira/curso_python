from flask import Flask, render_template_string
import plotly.express as px
import pandas as pd

# Inicia o Flask
app = Flask(__name__)

# Cria nosso dataframe
df_consolidado = pd.DataFrame({
    'Status': [
        'Ativo',
        'Inativo',
        'Ativo',
        'Inativo',
        'Ativo',
        'Inativo',
        'cancelado',
        'cancelado',
        'Ativo'
    ]
})

# Rota do gráfico de pizza usando o plotly
@app.route('/')
def grafico_pizza():
    # Contar as ocorrências de cada status
    status_dist = df_consolidado['Status'].value_counts().reset_index()
    status_dist.columns = ['Status', 'Quantidade']

    # Criar o gráfico com plotly
    fig = px.pie(
        status_dist,
        values='Quantidade',
        names='Status',
        title='Distribuição do Status'
    )

    # Converter o gráfico para HTML (isso já gera um HTML pronto com <div>, <style>, e { })
    grafico_html = fig.to_html(full_html=False)

    html = '''
        <html>
            <head>
                <meta charset="UTF-8">
                <title>Feito com ♥ por Lalala</title>
            </head>
            <body>
                <h2>Gráfico com plotly</h2>
                <!-- Aqui usamos {{ grafico_html | safe }} ao invés de {grafico_html} -->
                {{ grafico_html | safe }}
            </body>
        </html>
    '''

    # Passamos a variável grafico_html como argumento para o template
    return render_template_string(html, grafico_html=grafico_html)

if __name__ == '__main__':
    app.run(debug=True)
