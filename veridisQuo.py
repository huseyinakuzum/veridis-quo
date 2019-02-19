import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import argparse
import os


class VeridisQuo():
    def __init__(self, username, cid, secret, redirect_uri):
        self.username = username
        self.scope = 'user-library-read playlist-read-private playlist-modify-private playlist-modify-public user-top-read user-read-recently-played'
        self.cid = cid
        self.secret = secret
        self.redirect_uri = redirect_uri
        # artist_to_discover_uri = '0HgZEgGO4KjuGbeAXXl25w'
        SpotifyClientCredentials(client_id=self.cid, client_secret=self.secret)
        self.token = util.prompt_for_user_token(
            self.username, self.scope, redirect_uri=self.redirect_uri)

        if self.token:
            self.sp = spotipy.Spotify(auth=self.token)
            self.current_user_id = self.sp.current_user()['id']

        else:
            print("Can't get token for", username)
            quit()

    def discover_artist(self, artist_to_discover_uri, discovered_artists,
                        discovered_songs, song_count, song_per_artist_count,
                        audio_features=False, audio_features_initial=None, log=False):

        if song_count == 0:
            return discovered_songs

        last_discovered_artist_uri = ''
        artist_related_artists = self.sp.artist_related_artists(
            artist_to_discover_uri)['artists']

        for i in artist_related_artists:
            discovered_artist_uri = i['uri']

            if discovered_artist_uri not in discovered_artists:
                discovered_artists.append(discovered_artist_uri)
                last_discovered_artist_uri = discovered_artist_uri
                inserted_song_for_artist = 0
                discover_artist_top_tracks = self.sp.artist_top_tracks(
                    discovered_artist_uri)['tracks']

                for j in discover_artist_top_tracks:
                    if inserted_song_for_artist == song_per_artist_count:
                        return self.discover_artist(last_discovered_artist_uri,
                                                    discovered_artists, discovered_songs,
                                                    song_count-inserted_song_for_artist,
                                                    song_per_artist_count, audio_features_initial)

                    discovered_song_uri = j['uri']

                    # if audio features enabled
                    if audio_features == True and audio_features_initial is not None:
                        if discovered_song_uri not in discovered_songs:
                            audio_features_discovered = self.sp.audio_features(
                                discovered_song_uri)

                            if audio_features_discovered[0]['energy'] >= audio_features_initial[0]['energy'] or \
                                    audio_features_discovered[0]['tempo'] >= audio_features_initial[0]['tempo']:
                                if log == True:
                                    print(j['name'] + ' from ' +
                                          i['name'] + ' is being added!')
                                discovered_songs.append(j['uri'])
                                inserted_song_for_artist += 1
                    ############################
                    else:
                        discovered_songs.append(discovered_song_uri)
                        if log == True:
                            print(j['name'] + ' from ' +
                                  i['name'] + ' is being added!')
                        inserted_song_for_artist += 1

    def add_to_playlist(self, playlist, playlist_name):
        playlist_created = self.sp.user_playlist_create(
            self.current_user_id, playlist_name)
        if len(playlist) < 100:
            playlist_created = self.sp.user_playlist_add_tracks(
                self.current_user_id, playlist_created['uri'], playlist)
            return playlist_created

        else:
            song_count = len(playlist)
            while song_count > 100:
                playlist_created = self.sp.user_playlist_add_tracks(
                    self.current_user_id, self.sp.user_playlist_create(
                        self.current_user_id, playlist_name)['uri'], playlist[0:99])
                playlist = playlist[100:]
                song_count -= 100
            playlist_created = self.sp.user_playlist_add_tracks(
                self.current_user_id, self.sp.user_playlist_create(
                    self.current_user_id, playlist_name)['uri'], playlist)
            return playlist_created
