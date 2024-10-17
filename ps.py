import streamlit as st
import pandas as pd


st.title("ANALISIS DE MY PLAYLIST")

playlist = pd.read_csv(r'C:\Users\Dussand\Desktop\proyectsDS\Python\Machine Learning\spotify\myplaylist_spotify\data\my_playlist.csv')

# Título de la aplicación

album = playlist['album'].unique()
album_sb = st.selectbox('Selecciona uno de los albumes de tu playlist', album)
song_sb = st.selectbox('Selecciona una cancion: ', playlist[playlist['album']== album_sb]['name'].unique())

# Filtrar el DataFrame para obtener la URL de la imagen del álbum seleccionado
image_url = playlist.loc[playlist['album'] == album_sb, 'album_image_url'].values[0]

track_id = playlist.loc[playlist['name'] == song_sb, 'track_id'].values[0]
    
# Crear la URL del embed de Spotify
spotify_embed_url = f"https://open.spotify.com/embed/track/{track_id}"

# playlist_df = pd.merge(
#     album_images,
#     on = 'album'
# )
# Agregar una imagen

col1, col2 = st.columns(2)

with col1:
    st.markdown(
    f"""
    <iframe src="{spotify_embed_url}" width="300" height="380" frameborder="0" allowtransparency="true" allow="encrypted-media"></iframe>
    """,
    unsafe_allow_html=True
)
 
with col2:
    
    # Filtra el DataFrame para obtener el valor de popularidad del álbum seleccionado
    album_popularity = playlist.loc[playlist['album'] == album_sb, 'name'].count()
    
    # Muestra la métrica con el valor de popularidad
    st.metric(label=f"Canciones en tu playlist de: {album_sb}", value=album_popularity)

    # Filtra el DataFrame para obtener el valor de popularidad del álbum seleccionado
    song_popularity = playlist.loc[playlist['album'] == album_sb, 'name'].values[0]
    
    # Muestra la métrica con el valor de popularidad
    st.metric(label=f"Canciones en tu playlist de: {album_sb}", value=song_popularity)

    # Filtra el DataFrame para obtener el valor de popularidad del álbum seleccionado
    date_released = playlist.loc[playlist['album'] == album_sb, 'release_date'].values[0]
    
    # Muestra la métrica con el valor de popularidad
    st.metric(label=f"Canciones en tu playlist de: {album_sb}", value=date_released)











