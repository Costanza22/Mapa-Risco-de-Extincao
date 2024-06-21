
import folium
import pandas as pd
from folium.plugins import MousePosition

# Exemplo de dados de animais em risco de extinção, com URLs das imagens e descrição
data = {
    'Animal': ['Onça-Pintada', 'Mico-Leão-Dourado', 'Ararinha-Azul', 'Tartaruga-de-Couro'],
    'Latitude': [-15.7801, -22.9661, -5.8100, 0.3476],
    'Longitude': [-47.9292, -43.2075, -49.7959, -89.1574],
    'Status': ['Em Perigo', 'Em Perigo', 'Criticamente Em Perigo', 'Vulnerável'],
    'Imagem': [
        'https://www.infoescola.com/wp-content/uploads/2008/05/onca-pintada-591459416.jpg',
        'https://www.coisasdaroca.com/wp-content/uploads/2020/06/mico-2.jpg',
        'https://s2.glbimg.com/FR6jrT4gKQuTXit78yN94mCkhes=/0x0:1900x1461/1008x0/smart/filters:strip_icc()/i.s3.glbimg.com/v1/AUTH_59edd422c0c84a879bd37670ae4f538a/internal_photos/bs/2019/1/g/BjKNYuSBeVn9zupTRamA/araraazul.jpg',
        'https://th.bing.com/th/id/OIP.CzU3Hmx5NvnXYRwxx5QTXQHaFE?rs=1&pid=ImgDetMain'
    ],
    'Descricao': [
        'A onça-pintada é um grande felino das Américas. É o maior felino das Américas e o terceiro maior do mundo.',
        'O mico-leão-dourado é um pequeno primata encontrado na Mata Atlântica do Brasil. É conhecido por sua pelagem dourada brilhante.',
        'A ararinha-azul é uma espécie de ave psittaciforme endêmica do Brasil. É uma das aves mais raras do mundo.',
        'A tartaruga-de-couro é a maior das tartarugas marinhas e pode ser encontrada em todos os oceanos tropicais e subtropicais.'
    ]
}

# Criando um DataFrame
df = pd.DataFrame(data)

# Criando um mapa base
mapa = folium.Map(location=[-15.7801, -47.9292], zoom_start=4)

# Adicionando camadas de tiles públicas com atribuições
folium.TileLayer(
    'Stamen Terrain',
    name='Stamen Terrain',
    attr='Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL.'
).add_to(mapa)

folium.TileLayer(
    'Stamen Toner',
    name='Stamen Toner',
    attr='Map tiles by Stamen Design, under CC BY 3.0. Data by OpenStreetMap, under ODbL.'
).add_to(mapa)

# Função para adicionar marcador com popup
def add_marker(row):
    html = f"""
    <h4>{row['Animal']}</h4>
    <p>Status: {row['Status']}</p>
    <img src="{row['Imagem']}" alt="{row['Animal']}" width="150" height="100"><br>
    <p>{row['Descricao']}</p>
    """
    iframe = folium.IFrame(html=html, width=250, height=300)
    popup = folium.Popup(iframe, max_width=250)
    
    marker = folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=popup,
        icon=folium.Icon(color='red' if 'Criticamente' in row['Status'] else 'orange' if 'Perigo' in row['Status'] else 'blue')
    )
    marker.add_to(mapa)

# Adicionando marcadores ao mapa
for index, row in df.iterrows():
    add_marker(row)

# Adicionando controle de camadas
folium.LayerControl().add_to(mapa)

# Adicionando posição do mouse
formatter = "function(num) {return L.Util.formatNum(num, 5);};"
MousePosition(
    position='topright',
    separator=' Long: ',
    empty_string='NaN',
    lng_first=True,
    num_digits=20,
    prefix='Lat: ',
    lat_formatter=formatter,
    lng_formatter=formatter,
).add_to(mapa)

# Salvando o mapa em um arquivo HTML com a inclusão do favicon
html_content = mapa.get_root().render()

favicon_html = """
<link rel="shortcut icon" href="favicon.ico" type="image/x-icon">
<link rel="icon" href="favicon.ico" type="image/x-icon">
"""

html_content = html_content.replace("<head>", f"<head>{favicon_html}")

with open('mapa_animais_extincao.html', 'w') as file:
    file.write(html_content)
