import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go


st.title("ANALISIS DE MY PLAYLIST")

playlist = pd.read_csv(r'C:\Users\Dussand\Desktop\proyectsDS\Python\Machine Learning\spotify\myplaylist_spotify\data\my_playlist.csv')
kanye_west = pd.read_csv(r'C:\Users\Dussand\Desktop\proyectsDS\Python\Machine Learning\spotify\myplaylist_spotify\data\Kanye West.csv')
kendrick_lamar = pd.read_csv(r'C:\Users\Dussand\Desktop\proyectsDS\Python\Machine Learning\spotify\myplaylist_spotify\data\Kendrick Lamar.csv')

playlist = playlist.drop(columns=['Unnamed: 0'])
kanye_west = kanye_west.drop(columns=['Unnamed: 0'])
kendrick_lamar = kendrick_lamar.drop(columns=['Unnamed: 0'])

playlist['year'] = playlist['release_date'].str.slice(0,4)
kanye_west['year'] = kanye_west['release_date'].str.slice(0,4)
kendrick_lamar['year'] = kendrick_lamar['release_date'].str.slice(0,4)

k1, k2 = st.columns(2)

with k1:
    st.metric(
        label='Cantidad de canciones el la playlist: ',
        value= playlist['name'].count()
)

with k2:
    sd = playlist.groupby('artist')['name'].count().sort_values(ascending=False).reset_index()
    st.metric(
        label = 'Artista con mas canciones',
        value = sd.iloc[0]['artist']

    )
# Título en la barra lateral
st.sidebar.title("Elige tu cancion para escuchar")

# Título de la aplicación

artist = playlist['artist'].unique()
artist_sb = st.sidebar.selectbox('Selecciona uno de los albumes de tu playlist', artist)
song_sb = st.sidebar.selectbox('Selecciona una cancion: ', playlist[playlist['artist']== artist_sb]['name'].unique())

# Filtrar el DataFrame para obtener la URL de la imagen del álbum seleccionado
image_url = playlist.loc[playlist['artist'] == artist_sb, 'album_image_url'].values[0]

track_id = playlist.loc[playlist['name'] == song_sb, 'track_id'].values[0]
    
# Crear la URL del embed de Spotify
spotify_embed_url = f"https://open.spotify.com/embed/track/{track_id}"

col1, col2 = st.sidebar.columns(2)

with col1:
    st.sidebar.markdown(
    f"""

    <iframe src="{spotify_embed_url}" width="300" height="380" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>
    """,
    unsafe_allow_html=True
 )

#veremos los albumes con mas presencia en mi playlist
st.header('TOP 5 ALBUMES CON MAYOR PRESENCIA EN LA PLAYLIST')
st.write('')
st.write('')

top_5_albumes = playlist.groupby(['album', 'album_image_url'])['album'].count().reset_index(name = 'count').sort_values('count', ascending=False)
# top_5_albumes
c1, c2, c3= st.columns(3)

with c1:
    st.markdown(
    """
    <style>
    .img-rounded {
        border-radius: 10px;
        width: 40%;
        max-width: 20px;
        height: auto;
    }
    </style>
    """'',
    unsafe_allow_html=True
)
    #itermaos sobre los albumes
    for i in range(5):
        st.markdown(
            f'<img src="{top_5_albumes.iloc[i, 1]}" alt="Imagen Redondeada" style="border-radius: 10px; width: 70%; max-width: 85px; height: auto;">',
            unsafe_allow_html=True
        )
        st.write('')
with c2:
     for i in range(5):
         album_frecuency = top_5_albumes.iloc[i]['album']
         st.metric(label = 'Album Name', value = album_frecuency )
         st.write('')
with c3:
    for i in range (5):
        count_album = top_5_albumes.iloc[i]['count']
        st.metric(label = 'Songs amount', value = count_album)
        st.write('')

st.header('ALBUM CON MAS POPULARIDAD Y CANCION CON MAS POPULARIDAD')
st.write('Analizaremos que album tiene mas popularidad en la plataforma, asimismo con la cancion')

album_popularity = playlist.groupby(['album', 'album_image_url'])['popularity'].mean().sort_values(ascending = False).reset_index()
# album_popularity

colu1, colu2 = st.columns(2)

with colu1:
    st.markdown(
    """
    <style>
    .img-rounded {
        border-radius: 10px;
        width: 50%;
        max-width: 40px;
        height: auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)
    #itermaos sobre los albumes
    for i in range(1):
        st.markdown(
        f'<img src="{album_popularity.iloc[i, 1]}"  alt="Imagen Redondeada" style="border-radius: 10px; width: 100%; max-width: 400px; height: auto;">',
            unsafe_allow_html=True
        )

with colu2:
         for i in range(1):
              top_song = album_popularity.iloc[i]['album']
              st.metric(
                   label = 'Song name:',
                   value = top_song
              )


st.write('')
st.write('')
st.write('')
st.header('CANCIONES POR AÑO DE LANZAMIENTO DEL ALBUM')

oldest_album = playlist.groupby(['album', 'name', 'album_image_url'])['release_date'].min().reset_index()
oldest_album['year'] = oldest_album['release_date'].str.slice(0,4)
# oldest_album
# Manejar errores durante la conversión
oldest_album['year'] = pd.to_numeric(oldest_album['year'], errors='coerce').astype('Int64')
oldest_album['year'] = oldest_album['year'].astype(int)
# oldest_album


# Slider para seleccionar un valor entre 0 y 100
valor = st.slider(
    "Selecciona un valor:", 
    min_value=oldest_album['year'].min(), 
    max_value=oldest_album['year'].max(), 
    value=oldest_album['year'].min()  # O cualquier valor inicial que prefieras
)


#filtramos por año seleccionado
oldest_album_filtered = oldest_album[oldest_album['year'] == valor]

if not oldest_album_filtered.empty:
     oa_sb = oldest_album_filtered[oldest_album_filtered['year'] == valor]['album'].unique()
     select_album = st.selectbox(f'ALBUMES DEL AÑO {valor} DE LA LISTA', oa_sb)
     name_df = oldest_album_filtered[oldest_album_filtered['album'] == select_album]

     a1, a2 = st.columns(2)

     with a1:
          st.markdown(
               f"""
               <style>
               .img.rounded {{
               border-radius: 15px;
               width: 100%;
               max-width: 40px;
               height: auto;
               }}
               </style>
               <img src = "{name_df['album_image_url'].values[0]}" alt="Imagen Redondeada" style="border-radius: 10px; width: 90%; max-width: 400px; height: auto;">',
               """,
               unsafe_allow_html=True
               
          )
     with a2:
          st.subheader(f"Canciones de {select_album} en tu playlist: ")
          for i in range(len(name_df)):
               oldest_name = name_df.iloc[i]['name']
               st.write(f'**{oldest_name}**')
          
else:
     st.write('No hay resultados para este año')




year_song = playlist.groupby('year')['name'].count().reset_index()

fig = px.bar(
     data_frame=year_song,
     x = 'year',
     y = 'name',
     color = 'name',
     color_continuous_scale=px.colors.sequential.Reds
)

st.plotly_chart(fig)

st.header('ARTISTAS CON MAS PRESENCIA EN LA PLAYLIST')
st.write('Veremos los artistas con mayor presencia en la playlist')

artist_frequemcy = playlist.groupby(['artist', 'artist_image_url'])['name'].count().reset_index(name = 'count').sort_values(by = 'count',ascending=False)
#artist_frequemcy

aa1, aa2 = st.columns(2)

with aa1:

          st.markdown(
               f"""
               <style>
               .img.rounded {{
               border-radius: 15px;
               width: 100%;
               max-width: 40px;
               height: auto;
               }}
               </style>
               <img src = "{artist_frequemcy['artist_image_url'].values[0]}" alt="Imagen Redondeada" style="border-radius: 10px; width: 90%; max-width: 400px; height: auto;">',
               """,
               unsafe_allow_html=True
               
          )

          st.metric(
               label= 'Artista',
               value= artist_frequemcy.iloc[0]['artist']
               
          )

          st.metric(
               label= 'Numero de canciones en la playlist',
               value= artist_frequemcy.iloc[0]['count']
               
          )
          kanye  = playlist.groupby(['album', 'artist'])['name'].nunique().reset_index().sort_values('name', ascending=False)
          value_ye = artist_frequemcy['artist'].values[0]
          fig = px.bar(
               data_frame=kanye[kanye['artist'] == value_ye],
               x = 'album',
               y = 'name',
               color = 'name',
               color_continuous_scale=px.colors.sequential.Greys
          )
          
          st.plotly_chart(fig)

with aa2:
          st.markdown(
               f"""
               <style>
               .img.rounded {{
               border-radius: 15px;
               width: 100%;
               max-width: 40px;
               height: auto;
               }}
               </style>
               <img src = "{artist_frequemcy['artist_image_url'].values[1]}" alt="Imagen Redondeada" style="border-radius: 10px; width: 90%; max-width: 400px; height: auto;">',
               """,
               unsafe_allow_html=True
               
          )

          st.metric(
               label= 'Artista',
               value= artist_frequemcy.iloc[1]['artist']
               
          )

          st.metric(
               label= 'Numero de canciones en la playlist',
               value= artist_frequemcy.iloc[1]['count']
               
          )

          kdot  = playlist.groupby(['album', 'artist'])['name'].nunique().reset_index().sort_values('name', ascending=False)
          value_kdot = artist_frequemcy['artist'].values[1]
          fig = px.bar(
               data_frame=kdot[kdot['artist'] == value_kdot],
               x = 'album',
               y = 'name',
               color = 'name',
               color_continuous_scale=px.colors.sequential.Oranges
          )
          
          st.plotly_chart(fig)
    
st.header('ANALIZAREMOS UN POCO MAS A LOS DOS ARTISTAS CON MAYOR PRESENCIA EN LA PLAYLIST')

st.subheader('¿Cuales son los albumes mas populares de Kanye?')
kanye_west = pd.merge(
    kanye_west,
    playlist[['album', 'album_image_url']],
    on = 'album',
    how = 'left'
    
)

popular_album = kanye_west.groupby(['album', 'album_image_url']).agg({
      'popularity':'mean',
      'track_name':'nunique'
}).reset_index().sort_values('popularity', ascending=False)


q1, q2, q3 = st.columns(3)

with q1:

          st.markdown(
               f"""
               <style>
               .img.rounded {{
               border-radius: 15px;
               width: 100%;
               max-width: 40px;
               height: auto;
               }}
               </style>
               <img src = "{popular_album['album_image_url'].values[0]}" alt="Imagen Redondeada" style="border-radius: 10px; width: 90%; max-width: 400px; height: auto;">',
               """,
               unsafe_allow_html=True
               
          )

          st.metric(
               label= 'Album',
               value= popular_album.iloc[0]['album']
               
          )

          st.metric(
               label= 'Canciones',
               value= popular_album.iloc[0]['track_name']
               
          ) 

          st.metric(
               label= 'Popularidad de la cancion (limite 100)',
               value= round(popular_album.iloc[0]['popularity'], 2)
               
          )


with q2:
          st.markdown(
               f"""
               <style>
               .img.rounded {{
               border-radius: 15px;
               width: 100%;
               max-width: 40px;
               height: auto;
               }}
               </style>
               <img src = "{popular_album['album_image_url'].values[1]}" alt="Imagen Redondeada" style="border-radius: 10px; width: 90%; max-width: 400px; height: auto;">',
               """,
               unsafe_allow_html=True
               
          )


          st.metric(
               label= 'Album',
               value= popular_album.iloc[1]['album']
               
          )

          st.metric(
               label= 'Canciones',
               value= popular_album.iloc[1]['track_name']
               
          )

          st.metric(
               label= 'Popularidad de la cancion (limite 100)',
               value= round(popular_album.iloc[1]['popularity'], 2)
               
          )


with q3:
          st.markdown(
               f"""
               <style>
               .img.rounded {{
               border-radius: 15px;
               width: 100%;
               max-width: 40px;
               height: auto;
               }}
               </style>
               <img src = "{popular_album['album_image_url'].values[2]}" alt="Imagen Redondeada" style="border-radius: 10px; width: 90%; max-width: 400px; height: auto;">',
               """,
               unsafe_allow_html=True
               
          )


          st.metric(
               label= 'Album',
               value= popular_album.iloc[2]['album']
               
          )

          st.metric(
               label= 'Canciones',
               value= popular_album.iloc[2]['track_name']
               
          )

          st.metric(
               label= 'Popularidad de la cancion (limite 100)',
               value= round(popular_album.iloc[2]['popularity'], 2)
               
          )

st.write('')

st.title('LINEA DE POPULARIDAD DE LOS ALBUMES DE KANYE WEST')

fig = go.Figure()

fig.add_trace(
      go.Scatter(
        x=popular_album['album'],  # Repetimos el eje x para que la línea siga el mismo formato
        y= popular_album['popularity'],  # Línea horizontal en la popularidad 60

        name='Línea de Referencia',  # Nombre que aparecerá en la leyenda
        line=dict(color='red', dash='dash')  # Estilo de la línea
    )
            
)
  
st.plotly_chart(fig)
