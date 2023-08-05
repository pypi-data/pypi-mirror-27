import argparse
import collections
import getpass
import itertools
import json
import random
import sys
import time

import gmusicapi

import escapeorangebox


# TODO Add python logging and log info methods as tool progresses
# TODO Make artists an actual list and add ids


def truthy_mode(iterable):
    return (collections.Counter((i for i in iterable if i)).most_common(1)
            or [[None]])[0][0]


def truthy_mode_order(iterable):
    return [v[0] for v
            in collections.Counter((i for i in iterable if i)).most_common()]


def normalize_track(title, artist, trackNumber, durationMillis, genre='',
                    storeId=None, **_):
    return {
        'title': title,
        'artists': [{'name': artist}],
        'genre': genre,
        'track': trackNumber,
        'duration_ms': int(durationMillis),
        'ids': {} if storeId is None else {'google': storeId},
        'type': 'track',
    }


def normalize_album(name='', artist='', tracks=[], year=None, albumId=None,
                    **_):
    artist = (artist or truthy_mode(t['albumArtist'] for t in tracks)
              or truthy_mode(t['artist'] for t in tracks))
    return {
        'name': name or truthy_mode(t['album'] for t in tracks) or '',
        'artists': [] if artist is None else [{'name': artist}],
        'tracks': sorted((normalize_track(**t) for t in tracks),
                         key=lambda t: t['track']),
        'num_tracks': max(max(t['trackNumber'] for t in tracks),
                          len(tracks)) if tracks else 0,
        'art': truthy_mode_order(itertools.chain.from_iterable(
            (a['url'] for a in t.get('albumArtRef', ())) for t in tracks)),
        'ids': {} if albumId is None else {'google': albumId},
        'year': year or truthy_mode(t.get('year', None) for t in tracks),
        'type': 'album',
    }


def normalize_playlist(name, tracks, **_):
    return {
        'name': name,
        'tracks': [normalize_track(**t) for t in tracks],
        'type': 'playlist',
    }


def album_key(album, albumArtist, **_):
    return album, albumArtist


def download_song_info(client, update=True, timeout_func=lambda: 0):
    """FIXME

    Parameters
    ----------
    client : Mobileclient
        A gmusicapi mobile client.
    update : boolean, optional
        If true, update song and album information with what's available on
        Google.
    """
    user_tracks = {}
    user_albums = {}
    store_albums = {}
    user_playlists = [
        p for p in client.get_all_user_playlist_contents() if not p['deleted']]
    star_tracks = []

    # Get all library songs and group into albums
    for chunk in client.get_all_songs(True):
        for track in chunk:
            if track['deleted']:
                continue
            user_tracks[track['id']] = track
            if track.get('rating', None) == '5':
                star_tracks.append(track)
            if 'albumId' in track:
                tracks = store_albums.setdefault(
                    track['albumId'], {'tracks': []})['tracks']
            else:
                tracks = user_albums.setdefault(album_key(**track), [])
            tracks.append(track)

    if update:
        # Update albums
        for aid, album in store_albums.items():
            try:
                time.sleep(timeout_func())
                album.update(client.get_album_info(aid))
                user_albums.pop((album['name'], album['artist']), None)
            except gmusicapi.CallFailure:
                pass  # Couldn't find album
        # Update individual songs
        for tracks in user_albums.values():
            for track in tracks:
                tid = track.get('storeId', None) or track.get('nid', None)
                if tid is not None:
                    try:
                        time.sleep(timeout_func())
                        track.update(client.get_track_info(tid))
                    except gmusicapi.CallFailure:
                        pass  # Couldn't find track

    # Get track info for playlists
    # This happens after update so we potentially get updated track info
    for play in user_playlists:
        for track in play['tracks']:
            base = user_tracks[track['trackId']]
            tid = base.get('storeId', None) or base.get('nid', None)
            if (update and tid is not None and
                    'trackAvailableForPurchase' not in base):
                try:
                    time.sleep(timeout_func())
                    base.update(client.get_track_info(tid))
                except gmusicapi.CallFailure:
                    pass  # Couldn't find track
            track.update(base)

    # Add star playlist
    user_playlists.append({'name': 'Star', 'tracks': star_tracks})

    # Merge albums
    final_albums = {}
    for album in store_albums.values():
        norm = normalize_album(**album)
        artist = next((a['name'] for a in norm['artists']), '')
        final_albums[norm['name'], artist] = album
    for key, tracks in user_albums.items():
        final_albums.setdefault(key, {'tracks': []})['tracks'].extend(tracks)

    return {
        'albums': [normalize_album(**a) for a in final_albums.values()],
        'playlists': [normalize_playlist(**p) for p in user_playlists],
    }


def main():
    parser = argparse.ArgumentParser(
        description="""Command line tool to download metadata from Google Play
        Music""")
    parser.add_argument(
        '-V', '--version', action='version',
        version='%(prog)s {}'.format(escapeorangebox.__version__))
    parser.add_argument(
        'user', metavar='<google-username>', help="""The google account
        username to pull sing information from.""")
    parser.add_argument(
        '-o', '--output', metavar='<file>', type=argparse.FileType('w'),
        default=sys.stdout, help="""Output file. (default: stdout)""")
    parser.add_argument(
        '-t', '--timeout', metavar='<timeout>', type=float, default=0.1,
        help="""Average timeout to
        wait between requests to avoid rate limiting.
        (default: %(default)g)""")
    args = parser.parse_args()
    client = gmusicapi.Mobileclient(False, True, True)
    if not client.login(
            args.user,
            getpass.getpass('Google password for {}: '.format(args.user)),
            client.FROM_MAC_ADDRESS):
        sys.stderr.write('Authentication failed')  # TODO Make log message
        sys.exit(1)
    if args.timeout > 0:
        def tfunc():
            return random.expovariate(1 / args.timeout)
    else:
        def tfunc():
            return 0
    output = download_song_info(client, True, tfunc)
    json.dump(output, args.output, separators=(',', ':'))
    args.output.write('\n')


if __name__ == '__main__':
    main()
