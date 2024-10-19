import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go


st.title("ANALISIS DE MY PLAYLIST")

playlist = pd.read_csv('data/my_playlist.csv')
kanye_west = pd.read_csv('data/Kanye West.csv')
kendrick_lamar = pd.read_csv('data/Kendrick Lamar.csv')

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

l1, l2 = st.columns(2)

with l1:
      st.subheader('Total de canciones')
      kanye_west_songs = kanye_west['track_name'].nunique()
      st.write(f'**{kanye_west_songs}**')

with l2:
      st.subheader('Total de albumes')
      kanye_west_albumes = kanye_west['album'].nunique()
      st.write(f'**{kanye_west_albumes}**')


st.subheader('¿Cuales son los albumes mas populares de Kanye?')
kanye_west = pd.merge(
    kanye_west,
    playlist[['album', 'album_image_url']],
    on = 'album',
    how = 'inner'
    
)

kanye_west = kanye_west.drop_duplicates()

kanye_west.loc[kanye_west['album'] == 'KIDS SEE GHOSTS', 'album_image_url'] = \
    kanye_west.loc[kanye_west['album'] == 'KIDS SEE GHOSTS', 'album_image_url'].where(
        kanye_west['album_image_url'].notna(), 
        'https://www.thebackpackerz.com/wp-content/uploads/2018/08/FullSizeRender-2.jpg'
    )

kanye_west.loc[kanye_west['album'] == 'Watch The Throne (Deluxe)', 'album_image_url'] = \
    kanye_west.loc[kanye_west['album'] == 'Watch The Throne (Deluxe)', 'album_image_url'].where(
        kanye_west['album_image_url'].notna(), 
        'https://i.scdn.co/image/ab67616d0000b2735c837cc621c1ec82bf3c81ac'
    )

kanye_west.loc[kanye_west['album'] == '808s & Heartbreak', 'album_image_url'] = \
    kanye_west.loc[kanye_west['album'] == '808s & Heartbreak', 'album_image_url'].where(
        kanye_west['album_image_url'].notna(), 
        'https://i.scdn.co/image/ab67616d0000b273346d77e155d854735410ed18'
    )

kanye_west.loc[kanye_west['album'] == 'Late Orchestration', 'album_image_url'] = \
    kanye_west.loc[kanye_west['album'] == 'Late Orchestration', 'album_image_url'].where(
        kanye_west['album_image_url'].notna(), 
        'https://m.media-amazon.com/images/I/81X+h7CMPgL._AC_UF1000,1000_QL80_.jpg'
    )

kanye_west.loc[kanye_west['album'] == 'Late Registration', 'album_image_url'] = \
    kanye_west.loc[kanye_west['album'] == 'Late Registration', 'album_image_url'].where(
        kanye_west['album_image_url'].notna(), 
        'https://i.scdn.co/image/ab67616d0000b273428d2255141c2119409a31b2'
    )

popular_album = kanye_west.groupby(['album', 'album_image_url','year']).agg({
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

popular_album_1= kanye_west.groupby(['album','year']).agg({
      'popularity':'mean',
      'track_name':'nunique'
}).reset_index().sort_values('popularity', ascending=False)

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=popular_album_1['popularity'],  # Años en el eje X
        y=popular_album_1['year'],  # Popularidad en el eje Y
        mode='markers+text',  # Mostrar marcadores y texto
        marker=dict(
            size=10,
            color=popular_album_1['popularity'],  # Usar popularidad como base de los colores
            colorscale='Viridis',
            showscale=False  # Mostrar la escala de colores
        ),
        text=popular_album_1['album'],  # Nombres de álbumes como etiquetas
        textposition='top center',  # Posición del texto sobre el marcador
        showlegend=False
    )
)
# fig.add_trace(
#       go.Scatter(
#          x = popular_album_1['year'].sort_values(),
#          y = popular_album_1['popularity'],
#          mode = 'markers',
#          marker=dict(
#                size = 10,
#                color = popular_album_1['popularity'],
#                colorscale = 'Viridis',
#                showscale = False
#          ),
#         showlegend=False

#       )
# )

  
st.plotly_chart(fig)
# kanye_west          
#·analizaremos el recorrido de la carrera de kanye west, los albumes lanzados por años 

year_album = kanye_west.groupby(['year', 'album', 'album_image_url'])['album'].nunique().reset_index(name = 'count')
year_album['year'] = year_album['year'] .astype(int)

# Slider para seleccionar un valor entre 0 y 100
años = st.selectbox('Selecciona un año: ', year_album['year'].unique())

#filtramos por año seleccionado
year_album_filtered = year_album[year_album['year'] == años]

if not year_album_filtered.empty:
     year_album_sb = year_album_filtered[year_album_filtered['year'] == años]
     o1, o2 = st.columns(2)

     with o1:

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
          for i in range(len(year_album_sb)):
            st.markdown(
            f'<img src="{year_album_sb['album_image_url'].values[i]}" alt="Imagen Redondeada" style="border-radius: 10px; width: 90%; max-width: 250px; height: auto;">',
            unsafe_allow_html=True
        ) 
          #   st.header(year_album_sb['album'].values[i])   
            st.write('')
     
     with o2:

          for i in range(len(year_album_sb)):
                 st.subheader(f"Nombre del album")
                 st.write(f'_{year_album_sb.iloc[i]['album']}_')
                 yezz  = kanye_west[kanye_west['album'] == year_album_sb.iloc[i]['album']]['track_name'].nunique()
                 st.subheader(f'Cantidad de canciones: ')
                 st.write(f'_{yezz}_')
                 st.write('')
                 st.write('')
                 st.write('')
                 st.write('')
                 st.write('')
else:
     st.write('No publico albumes este año el patrón.')


kanye_west['year'] = kanye_west['year'].astype(int)
album_per_year_kw = kanye_west[kanye_west['year'] == años]

# Comprobar si hay más de dos álbumes únicos
if album_per_year_kw['album'].nunique() >= 2:
      # Seleccionar álbum o álbumes
     selected_albums = st.multiselect('Selecciona uno o dos álbumes:', album_per_year_kw['album'].unique())

# Botón para filtrar
     if st.button('Filtrar álbumes'):
    # Filtrar el DataFrame por los álbumes seleccionados
          if selected_albums:
               filtered_df = album_per_year_kw[album_per_year_kw['album'].isin(selected_albums)]
               
               fig = go.Figure(
                     layout=go.Layout(
                           width=800,
                           height=800

                     )
               )

               fig.add_trace(
                    go.Scatter(
                         x=filtered_df['popularity'],  # Años en el eje X
                         y=filtered_df['track_name'],  # Popularidad en el eje Y
                         mode='markers+text',  # Mostrar marcadores y texto
                         marker=dict(
                                   size=10,
                                   color=filtered_df['popularity'],  # Usar popularidad como base de los colores
                                        colorscale='Viridis',
                                             showscale=False  # Mostrar la escala de colores
                                   )
                         )
               )


               fig.add_trace(
                    go.Scatter(
                         x=filtered_df['popularity'],  # Años en el eje X
                         y=filtered_df['track_name'],  # Popularidad en el eje Y
                         mode='markers+text',  # Mostrar marcadores y texto
                         marker=dict(
                                   size=10,
                                   color=filtered_df['popularity'],  # Usar popularidad como base de los colores
                                   colorscale='Viridis',
                                   showscale=False  # Mostrar la escala de colores
                                   )
                         )
               )

               st.plotly_chart(fig, key = 'fig2')

else:

      fig = go.Figure(
          layout = go.Layout(
               width=800,
               height=800
          )
      )

      fig.add_trace(
            go.Scatter(
                  x = album_per_year_kw['popularity'],
                  y = album_per_year_kw['track_name'],
                  mode = 'markers+text',
                  marker= dict(
                        size = 10,
                        color=album_per_year_kw['popularity'],
                        colorscale = 'Viridis',
                        showscale =False
                  )
            )
      )

      st.plotly_chart(fig, key = 'fig1')

st.write('')
st.write('')
st.write('')
st.write('')

st.header('**ANALISIS DEL SEGUNDO ARTISTA CON MAYOR FRECUENCIA EN LA PLAYLIST**')
st.header('KENDRICK LAMAR')

kd1, kd2 = st.columns(2)

with kd1:
      st.subheader('Total de canciones')
      kdot_songs = kendrick_lamar['track_name'].nunique()
      st.write(f'**{kdot_songs}**')

with kd2:
      st.subheader('Total de albumes')
      kdot_albumes = kendrick_lamar['album'].nunique()
      st.write(f'**{kdot_albumes}**')



st.subheader('¿Cuales son los albumes mas populares de Kendrick?y')
kendrick_lamar = pd.merge(
    kendrick_lamar,
    playlist[['album', 'album_image_url']],
    on = 'album',
    how = 'left'
    
)

kendrick_lamar = kendrick_lamar.drop_duplicates()


kendrick_lamar.loc[kendrick_lamar['album'] == 'Black Panther The Album Music From And Inspired By', 'album_image_url'] = \
    kendrick_lamar.loc[kendrick_lamar['album'] == 'Black Panther The Album Music From And Inspired By', 'album_image_url'].where(
        kendrick_lamar['album_image_url'].notna(), 
        'https://i.scdn.co/image/ab67616d0000b273c027ad28821777b00dcaa888'
    )

kendrick_lamar.loc[kendrick_lamar['album'] == 'DAMN. COLLECTORS EDITION.', 'album_image_url'] = \
    kendrick_lamar.loc[kendrick_lamar['album'] == 'DAMN. COLLECTORS EDITION.', 'album_image_url'].where(
        kendrick_lamar['album_image_url'].notna(), 
        'https://i.scdn.co/image/ab67616d0000b273add9eb25744782c3717c9368'
    )

kendrick_lamar.loc[kendrick_lamar['album'] == 'untitled unmastered.', 'album_image_url'] = \
    kendrick_lamar.loc[kendrick_lamar['album'] == 'untitled unmastered.', 'album_image_url'].where(
        kendrick_lamar['album_image_url'].notna(), 
        'https://media.pitchfork.com/photos/5929b49e9d034d5c69bf4ec7/1:1/w_450%2Cc_limit/1bcdfd6b.jpg'
    )

kendrick_lamar.loc[kendrick_lamar['album'] == 'Overly Dedicated', 'album_image_url'] = \
    kendrick_lamar.loc[kendrick_lamar['album'] == 'Overly Dedicated', 'album_image_url'].where(
        kendrick_lamar['album_image_url'].notna(), 
        'https://i.scdn.co/image/ab67616d0000b2739b035b031d9f0a6a75ae464e'
    )

popular_album_kdot = kendrick_lamar.groupby(['album', 'album_image_url','year']).agg({
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
               <img src = "{popular_album_kdot['album_image_url'].values[0]}" alt="Imagen Redondeada" style="border-radius: 10px; width: 90%; max-width: 400px; height: auto;">',
               """,
               unsafe_allow_html=True
               
          )

          st.metric(
               label= 'Album',
               value= popular_album_kdot.iloc[0]['album']
               
          )

          st.metric(
               label= 'Canciones',
               value= popular_album_kdot.iloc[0]['track_name']
               
          ) 

          st.metric(
               label= 'Popularidad de la cancion (limite 100)',
               value= round(popular_album_kdot.iloc[0]['popularity'], 2)
               
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
               <img src = "{popular_album_kdot['album_image_url'].values[1]}" alt="Imagen Redondeada" style="border-radius: 10px; width: 90%; max-width: 400px; height: auto;">',
               """,
               unsafe_allow_html=True
               
          )


          st.metric(
               label= 'Album',
               value= popular_album_kdot.iloc[1]['album']
               
          )

          st.metric(
               label= 'Canciones',
               value= popular_album_kdot.iloc[1]['track_name']
               
          )

          st.metric(
               label= 'Popularidad de la cancion (limite 100)',
               value= round(popular_album_kdot.iloc[1]['popularity'], 2)
               
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
               <img src = "{popular_album_kdot['album_image_url'].values[2]}" alt="Imagen Redondeada" style="border-radius: 10px; width: 90%; max-width: 400px; height: auto;">',
               """,
               unsafe_allow_html=True
               
          )


          st.metric(
               label= 'Album',
               value= popular_album_kdot.iloc[2]['album']
               
          )

          st.metric(
               label= 'Canciones',
               value= popular_album_kdot.iloc[2]['track_name']
               
          )

          st.metric(
               label= 'Popularidad de la cancion (limite 100)',
               value= round(popular_album_kdot.iloc[2]['popularity'], 2)
               
          )

st.write('')

st.title('LINEA DE POPULARIDAD DE LOS ALBUMES DE KENDRICK LAMAR')

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=popular_album_kdot['popularity'],  # Años en el eje X
        y=popular_album_kdot['year'],  # Popularidad en el eje Y
        mode='markers+text',  # Mostrar marcadores y texto
        marker=dict(
            size=10,
            color=popular_album_kdot['popularity'],  # Usar popularidad como base de los colores
            colorscale='Viridis',
            showscale=False  # Mostrar la escala de colores
        ),
        text=popular_album_kdot['album'],  # Nombres de álbumes como etiquetas
        textposition='top center',  # Posición del texto sobre el marcador
        showlegend=False
    )
)
st.plotly_chart(fig)
# kendrick_lamar          
#·analizaremos el recorrido de la carrera de kanye west, los albumes lanzados por años 

year_album = kendrick_lamar.groupby(['year', 'album_image_url', 'album'])['album'].nunique().reset_index(name = 'count')
year_album['year'] = year_album['year'].astype(int)

# Slider para seleccionar un valor entre 0 y 100
años = st.selectbox('Selecciona un año: ', year_album['year'].unique())

#filtramos por año seleccionado
year_album_filtered = year_album[year_album['year'] == años]

if not year_album_filtered.empty:
     year_album_sb = year_album_filtered[year_album_filtered['year'] == años]
     o1, o2 = st.columns(2)

     with o1:

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
          for i in range(len(year_album_sb)):
            st.markdown(
            f'<img src="{year_album_sb['album_image_url'].values[i]}" alt="Imagen Redondeada" style="border-radius: 10px; width: 90%; max-width: 250px; height: auto;">',
            unsafe_allow_html=True
        )
            st.write('')
     
     with o2:

          for i in range(len(year_album_sb)):
                 st.subheader(f"Nombre del album")
                 st.write(f'_{year_album_sb.iloc[i]['album']}_')
                 yezz  = kendrick_lamar[kendrick_lamar['album'] == year_album_sb.iloc[i]['album']]['track_name'].nunique()
                 st.subheader(f'Cantidad de canciones: ')
                 st.write(f'_{yezz}_')
                 st.write('')
                 st.write('')
                 st.write('')
                 st.write('')
                 st.write('')
else:
     st.write('No publico albumes este año el mejor rapero del siglo.')
  
kendrick_lamar['year'] = kendrick_lamar['year'].astype(int)
album_per_year = kendrick_lamar[kendrick_lamar['year'] == años]
# Comprobar si hay más de dos álbumes únicos
if album_per_year['album'].nunique() >= 2:
      # Seleccionar álbum o álbumes
     selected_albums = st.multiselect('Selecciona uno o dos álbumes:', album_per_year['album'].unique())

# Botón para filtrar
     if st.button('Filtrar álbumes'):
    # Filtrar el DataFrame por los álbumes seleccionados
          if selected_albums:
               filtered_df_kdot = album_per_year[album_per_year['album'].isin(selected_albums)]
               
               fig = go.Figure(
                     layout=go.Layout(
                           width=800,
                           height=800

                     )
               )

               fig.add_trace(
                    go.Scatter(
                         x=filtered_df_kdot['popularity'],  # Años en el eje X
                         y=filtered_df_kdot['track_name'],  # Popularidad en el eje Y
                         mode='markers+text',  # Mostrar marcadores y texto
                         marker=dict(
                                   size=10,
                                   color=filtered_df_kdot['popularity'],  # Usar popularidad como base de los colores
                                        colorscale='Viridis',
                                             showscale=False  # Mostrar la escala de colores
                                   )
                         )
               )


               fig.add_trace(
                    go.Scatter(
                         x=filtered_df_kdot['popularity'],  # Años en el eje X
                         y=filtered_df_kdot['track_name'],  # Popularidad en el eje Y
                         mode='markers+text',  # Mostrar marcadores y texto
                         marker=dict(
                                   size=10,
                                   color=filtered_df_kdot['popularity'],  # Usar popularidad como base de los colores
                                   colorscale='Viridis',
                                   showscale=False  # Mostrar la escala de colores
                                   )
                         )
               )

               st.plotly_chart(fig, key = 'fig2')

else:

      fig = go.Figure(
          layout = go.Layout(
               width=800,
               height=800
          )
      )

      fig.add_trace(
            go.Scatter(
                  x = album_per_year['popularity'],
                  y = album_per_year['track_name'],
                  mode = 'markers+text',
                  marker= dict(
                        size = 10,
                        color=album_per_year['popularity'],
                        colorscale = 'Viridis',
                        showscale =False
                  )
            )
      )

      st.plotly_chart(fig, key = 'fig4')
