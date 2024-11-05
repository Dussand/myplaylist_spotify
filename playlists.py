import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import spotipy
from spotipy.oauth2 import SpotifyOAuth

#definimos las credenciales

client_id = 'b6841f7c97974c8aacbdf448dae8677f'
client_secret = 'bc15cade85bc41f88d451fbb2c832eff'
redirect_url = 'http://localhost:8888/callback/'

#scope (permisos) para acceder a tus playlist
scope = 'playlist-read-private'

#autenticacion 
sp = spotipy.Spotify(auth_manager = SpotifyOAuth(
    client_id = client_id,
    client_secret = client_secret,
    redirect_uri = redirect_url,
    scope = scope
))

# Obtener tus playlists
playlists = sp.current_user_playlists()

#especifico el ID de mi playist a explorar
playlist_id = None

st.title('SELECCIONA UNA PLAYLIST')

#mostrar lso nombres de las playlist y sus IDS
for playlist in playlists['items']:
    playlist_name = playlist['name']
    playlist_id_value = playlist['id']

    if st.button(playlist_name, key = playlist_id_value):
        playlist_id = playlist_id_value


st.write('Selecciona una playlist')

# Verificar si se ha seleccionado una playlist
if playlist_id:
    # Obtener las canciones de la playlist seleccionada
    results = sp.playlist_tracks(playlist_id)

    # Lista para almacenar todas las canciones
    all_tracks = []
    artists_cache = {}  # Caché para almacenar información de los artistas ya consultados

    # Iterar mientras haya canciones en la respuesta
    while results['items']:
        for item in results['items']:
            track = item['track']
            artist_id = track['artists'][0]['id']
            
            # Verificar si el artista ya está en la caché
            if artist_id in artists_cache:
                artist_info = artists_cache[artist_id]
            else:
                artist_info = sp.artist(artist_id)
                artists_cache[artist_id] = artist_info  # Almacenar en la caché

            genres = artist_info['genres']
            album = track['album']
            album_image_url = album['images'][0]['url'] if album['images'] else None
            artist_image_url = artist_info['images'][0]['url'] if artist_info['images'] else None

            all_tracks.append({
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'album': track['album']['name'],
                'duration_sec': track['duration_ms'] / 1000,
                'popularity': track['popularity'],
                'release_date': track['album']['release_date'],
                'album_image_url': album_image_url,
                'artist_image_url': artist_image_url,
                'genres': ', '.join(genres),
                'track_id': track['id']
            })
        
        # Incrementar el offset para obtener el siguiente bloque de canciones
        offset = len(all_tracks)
        results = sp.playlist_tracks(playlist_id, offset=offset)

    # Crear DataFrame con todos los datos de las canciones
    playlist = pd.DataFrame(all_tracks)

    # Separar la columna 'genres' por comas y expandir los resultados en columnas
    genres_split = playlist['genres'].str.split(', ', expand=True)

    # Renombrar las columnas resultantes
    genres_split.columns = [f'genre_{i+1}' for i in range(genres_split.shape[1])]

    # Convertir todos los valores de la columna 'genres' a cadenas por si acaso hay valores no string
    playlist['genres'] = playlist['genres'].astype(str)

    # Contar la cantidad de géneros en cada fila
    playlist['genre_count'] = playlist['genres'].apply(lambda x: len(x.split(', ')))

    # Unir el DataFrame original con el DataFrame de géneros separados
    playlist = pd.concat([playlist, genres_split], axis=1)

    playlist['year'] = playlist['release_date'].str.slice(0,4)

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
    st.sidebar.title("Elige tu cancion para escuchar") #para otra 
    st.sidebar.selectbox('Selecciona una pagina', ('Pagina 1', 'Pagina 2'))

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

    st.title("TOP 5 ALBUMES CON MAYOR PRESENCIA EN LA PLAYLIST")

    top_5_albumes = playlist.groupby(['album', 'album_image_url'])['album'].count().reset_index(name = 'count').sort_values('count', ascending=False)

    for i in range(5):
        # Crear columnas para el layout
        col1, col2, col3, col4 = st.columns([1, 3, 2, 1])
        
        # Mostrar el ranking
        with col1:
            st.write(f"**#{i+1}**")

        # Mostrar la imagen del álbum (puedes ajustar el src)
        with col2:
            st.image(top_5_albumes['album_image_url'].iloc[i], width=60)
        
            # Mostrar el nombre del álbum
        with col3:
            st.write(f"**{top_5_albumes['album'].iloc[i]}**")
        
        # Mostrar la cantidad de canciones
        with col4:
            st.write(f"**{top_5_albumes['count'].iloc[i]}** canciones")
        

    st.title('ALBUM CON MAS POPULARIDAD Y CANCION CON MAS POPULARIDAD')
    st.write('Analizaremos que album tiene mas popularidad en la plataforma, asimismo con la cancion')

    album_popularity = playlist.groupby(['album', 'album_image_url'])['popularity'].mean().sort_values(ascending = False).reset_index()
    # album_popularity

    colu1, colu2 = st.columns(2)

    with colu1:
        #itermaos sobre los albumes
        for i in range(1):
            st.markdown(
            f'<img src="{album_popularity.iloc[i, 1]}"  alt="Imagen Redondeada" style="border-radius: 10px; width: 100%; max-width: 400px; height: auto; box-shadow: 4px 4px 12px rgba(0, 0, 0, 0.5); /* sombra */">',
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
    st.title('CANCIONES POR AÑO DE LANZAMIENTO DEL ALBUM')

    oldest_album = playlist.groupby(['album', 'name', 'album_image_url'])['release_date'].min().reset_index()
    oldest_album['year'] = oldest_album['release_date'].str.slice(0,4)

    # Manejar errores durante la conversión
    oldest_album['year'] = pd.to_numeric(oldest_album['year'], errors='coerce').astype('Int64')
    oldest_album['year'] = oldest_album['year'].astype(int)


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
                <img src = "{name_df['album_image_url'].values[0]}" alt="Imagen Redondeada" style="border-radius: 10px; width: 90%; max-width: 400px; height: auto; box-shadow: 4px 4px 12px rgba(0, 0, 0, 0.5); /* sombra */">
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

    st.title('ARTISTAS CON MAS PRESENCIA EN LA PLAYLIST')
    st.write('Veremos los artistas con mayor presencia en la playlist')

    artist_frequemcy = playlist.groupby(['artist', 'artist_image_url'])['name'].count().reset_index(name = 'count').sort_values(by = 'count',ascending=False)
    #artist_frequemcy

    aa1, aa2 = st.columns(2)

    with aa1:

            st.markdown(
                f"""
                <img src = "{artist_frequemcy['artist_image_url'].values[0]}" alt="Imagen Redondeada" style="border-radius: 10px; width: 90%; max-width: 400px; height: auto; box-shadow: 4px 4px 12px rgba(0, 0, 0, 0.5); /* sombra */">
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
                <img src = "{artist_frequemcy['artist_image_url'].values[1]}" alt="Imagen Redondeada" style="border-radius: 10px; width: 90%; max-width: 400px; height: auto;box-shadow: 4px 4px 12px rgba(0, 0, 0, 0.5); /* sombra */">
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