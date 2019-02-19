import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import argparse
import os
from veridisQuo import VeridisQuo


def parse_arguments():
    parser = argparse.ArgumentParser(description='spotify playlist creator')
    parser.add_argument('-u', '--username', type=str, default='shaquzum',
                        help='Enter username')
    parser.add_argument('-a', '--artist', type=str, default=None,
                        help='Enter artist uri you want to discover')
    parser.add_argument('-s', '--song_count', type=int, default=30, choices=[30, 60, 90],
                        help='Number of songs you want this script to add your playlist')
    parser.add_argument('-p', '--songs_per_artist', type=int,  default=1, choices=[1, 2, 3],
                        help='Number of songs per artist you want to add to playlist')
    parser.add_argument('-n', '--playlist_name', type=str,
                        default=None, help='Name of your playlist')
    parser.add_argument('-f', '--features', type=str, default='false', choices=['true', 'false'],
                        help='Set this to true if you want songs\' features to effect chosen songs')
    parser.add_argument('-l', '--log', type=str, default='false', choices=['true', 'false'],
                        help='Set this to true if you want songs\' features to effect chosen songs')
    args = parser.parse_args()
    return args


def main(args):
    username = args.username
    cid = os.environ['SPOTIPY_CLIENT_ID']
    secret = os.environ['SPOTIPY_CLIENT_SECRET']
    redirect_uri = os.environ['SPOTIPY_REDIRECT_URI']
    #artist_to_discover_uri = 'spotify:artist:0WwSkZ7LtFUFjGjMZBMt6T'

    veridisquo = VeridisQuo(username, cid, secret, redirect_uri)

    if veridisquo.token:
        print("Logged in as: " + veridisquo.current_user_id + '\n')

        artist_to_discover_uri = args.artist.split(':')[-1]
        song_count = args.song_count
        songs_per_artist = args.songs_per_artist
        audio_features = args.features

        discovered_artists = []
        discovered_songs = []
        print('Discovering ' + veridisquo.sp.artist(
            artist_to_discover_uri)['name'] + '!')
        first_artist_name = veridisquo.sp.artist(
            artist_to_discover_uri)['name']

        if args.playlist_name is None:
            playlist_name = 'Discovery of ' + first_artist_name
        else:
            playlist_name = args.playlist_name

        if audio_features is True:
            audio_features_inital = veridisquo.sp.audio_features(
                veridisquo.sp.artist_top_tracks(artist_to_discover_uri)['tracks'][0]['uri'])
            veridisquo.first_artist_name = veridisquo.sp.artist(
                artist_to_discover_uri)['name']
            playlist = veridisquo.discover_artist(artist_to_discover_uri,
                                                  discovered_artists, discovered_songs, song_count, songs_per_artist, True, audio_features_inital)
        else:
            playlist = veridisquo.discover_artist(artist_to_discover_uri,
                                                  discovered_artists, discovered_songs, song_count, songs_per_artist)

        veridisquo.add_to_playlist(
            playlist, playlist_name)

    else:
        print("Can't get token for", username)


if __name__ == '__main__':
    args = parse_arguments()
    main(args)
