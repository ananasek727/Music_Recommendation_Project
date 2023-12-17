import random
from urllib.parse import urlencode

from .execute_spotify_request import execute_spotify_api_request, RequestType


def get_users_top_artists(limit=10, offset=0) -> list:
    endpoint = "me/top/artists"
    request_data = urlencode({
        'limit': limit,
        'offset': offset
    })
    response = execute_spotify_api_request(endpoint=f"{endpoint}?{request_data}",
                                           request_type=RequestType.GET)

    artists_ids = []
    for artist in response['items']:
        artists_ids.append(artist['id'])

    return artists_ids


def get_users_top_tracks(limit=10, offset=0) -> list:
    endpoint = "me/top/tracks"
    request_data = urlencode({
        'limit': limit,
        'offset': offset
    })
    response = execute_spotify_api_request(endpoint=f"{endpoint}?{request_data}",
                                           request_type=RequestType.GET)

    track_ids = []
    for track in response['items']:
        track_ids.append(track['id'])

    return track_ids


def get_top_artist_rand(min_index: int, max_index: int) -> str:
    artist_ids = get_users_top_artists(max_index-min_index+1, min_index)
    rand_id = random.randint(0, max_index-min_index)
    return artist_ids[rand_id]


def get_top_track_rand(min_index: int, max_index: int) -> str:
    track_ids = get_users_top_tracks(max_index - min_index + 1, min_index)
    rand_id = random.randint(0, max_index - min_index)
    return track_ids[rand_id]


def get_top_artists_rand_seed(indexes: list[(int, int)]) -> str:
    artist_ids = []
    for min_index, max_index in indexes:
        artist_ids.append(get_top_artist_rand(min_index, max_index))

    return ','.join(artist_ids)


def get_top_tracks_rand_seed(indexes: list[(int, int)]) -> str:
    tracks_ids = []
    for min_index, max_index in indexes:
        tracks_ids.append(get_top_track_rand(min_index, max_index))

    return ','.join(tracks_ids)


# def get_rand_genres_seed(num_of_genre_seeds: int) -> str:
#     endpoint = "recommendations/available-genre-seeds"
#     response = execute_spotify_api_request(endpoint=endpoint, request_type=RequestType.GET)
#     selected_genres = random.sample(response['genres'], min(num_of_genre_seeds, len(response['genres'])))
#     return ','.join(selected_genres)


def set_popularity_range(parameters: dict, data: dict) -> None:
    # popularity_mapping = {
    #     'mainstream': (80, 100),
    #     'medium': (40, 85),
    #     'low': (10, 40)
    # }
    #
    # data['min_popularity'], data['max_popularity'] = popularity_mapping[parameters['popularity']]

    popularity_mapping = {
        'mainstream': 100,
        'medium': 70,
        'low': 20
    }

    data['target_popularity'] = popularity_mapping[parameters['popularity']]


def set_genre_seeds(parameters: dict, data: dict) -> None:
    # if not parameters['genres']:
    #     if parameters['personalization'] == 'low':
    #         data['seed_genres'] = get_rand_genres_seed(5)
    #     return

    data['seed_genres'] = ','.join(parameters['genres'])


def set_artists_and_songs_seeds(parameters: dict, data: dict) -> None:
    num_of_top_artists = len(get_users_top_artists(50, 0))
    art_nums = sorted(random.sample(range(num_of_top_artists), 10))

    num_of_top_tracks = len(get_users_top_tracks(50, 0))
    track_nums = sorted(random.sample(range(num_of_top_tracks), 15))

    if parameters['personalization'] == 'high':
        if len(parameters['genres']) == 3:
            data['seed_artists'] = get_top_artists_rand_seed([(art_nums[0], art_nums[2])])
            data['seed_tracks'] = get_top_tracks_rand_seed([(track_nums[0], track_nums[2])])
        elif len(parameters['genres']) == 2:
            data['seed_artists'] = get_top_artists_rand_seed([(art_nums[0], art_nums[2])])
            data['seed_tracks'] = get_top_tracks_rand_seed([(track_nums[0], track_nums[2]),
                                                            (track_nums[3], track_nums[4])])
        elif len(parameters['genres']) == 1:
            data['seed_artists'] = get_top_artists_rand_seed([(art_nums[0], art_nums[1]),
                                                              (art_nums[2], art_nums[3])])
            data['seed_tracks'] = get_top_tracks_rand_seed([(track_nums[0], track_nums[2]),
                                                            (track_nums[3], track_nums[4])])
        # elif len(parameters['genres']) == 0:
        #     data['seed_artists'] = get_top_artists_rand_seed([(art_nums[0], art_nums[1]),
        #                                                       (art_nums[2], art_nums[3])])
        #     data['seed_tracks'] = get_top_tracks_rand_seed([(track_nums[0], track_nums[1]),
        #                                                     (track_nums[2], track_nums[3]),
        #                                                     (track_nums[4], track_nums[5])])

    elif parameters['personalization'] == 'medium':
        if len(parameters['genres']) == 3:
            data['seed_artists'] = get_top_artists_rand_seed([(art_nums[-4], art_nums[-2])])
            data['seed_tracks'] = get_top_tracks_rand_seed([(track_nums[-7], track_nums[-2])])
        elif len(parameters['genres']) == 2:
            data['seed_artists'] = get_top_artists_rand_seed([(art_nums[-4], art_nums[-2])])
            data['seed_tracks'] = get_top_tracks_rand_seed([(track_nums[-7], track_nums[-3]),
                                                            (track_nums[-2], track_nums[-1])])
        elif len(parameters['genres']) == 1:
            data['seed_artists'] = get_top_artists_rand_seed([(art_nums[-4], art_nums[-2])])
            data['seed_tracks'] = get_top_tracks_rand_seed([(track_nums[-7], track_nums[-5]),
                                                            (track_nums[-4], track_nums[-3]),
                                                            (track_nums[-2], track_nums[-1])])
        # elif len(parameters['genres']) == 0:
        #     data['seed_artists'] = get_top_artists_rand_seed([(art_nums[-5], art_nums[-3]),
        #                                                       (art_nums[-2], art_nums[-1])])
        #     data['seed_tracks'] = get_top_tracks_rand_seed([(track_nums[-7], track_nums[-5]),
        #                                                     (track_nums[-4], track_nums[-3]),
        #                                                     (track_nums[-2], track_nums[-1])])


def set_emotion_parameters(emotion: str, data: dict) -> None:
    data['max_liveness'] = 0.8

    if emotion == 'angry':
        # data.update({'min_energy': 0.6, 'max_energy': 1, 'target_energy': 0.8})
        # data.update({'min_valence': 0.6, 'max_valence': 1, 'target_valence': 0.8})
        # # data.update({'min_loudness': '-60', 'max_loudness': '-20', 'target_loudness': -45})
        # data.update({'min_mode': 0, 'max_mode': 0, 'target_mode': 0})
        # data.update({'min_key': 6, 'max_key': 11})
        # data.update({'min_tempo': 100})
        data.update({'target_energy': 0.8})
        data.update({'target_valence': 0.8})
        data.update({'target_loudness': -40})
        data.update({'target_mode': 0})
        data.update({'target_key': 9})
        data.update({'target_tempo': 140})

    elif emotion == 'disgust':
        # data.update({'min_energy': 0.5, 'max_energy': 0.8, 'target_energy': 0.65})
        # data.update({'min_valence': 0, 'max_valence': 0.4, 'target_valence': 0.1})
        # data.update({'min_mode': 0, 'max_mode': 0, 'target_mode': 0})
        # data.update({'max_tempo': 100})
        data.update({'target_energy': 0.65})
        data.update({'target_valence': 0.15})
        data.update({'target_mode': 0})
        data.update({'target_tempo': 60})

    elif emotion == 'fear':
        # data.update({'min_energy': 0.5, 'max_energy': 0.95, 'target_energy': 0.75})
        # data.update({'min_valence': 0, 'max_valence': 0.4, 'target_valence': 0.2})
        # # data.update({'min_loudness': -15, 'max_loudness': 0, 'target_loudness': -7})
        # data.update({'min_key': 6, 'max_key': 11})
        # data.update({'min_tempo': 100})
        data.update({'target_energy': 0.7})
        data.update({'target_valence': 0.2})
        data.update({'target_loudness': -7})
        data.update({'target_key': 9})
        data.update({'target_tempo': 140})

    elif emotion == 'happy':
        # data.update({'min_energy': 0.6, 'max_energy': 1, 'target_energy': 0.8})
        # data.update({'min_valence': 0.6, 'max_valence': 1, 'target_valence': 0.95})
        # data.update({'min_mode': 1, 'max_mode': 1, 'target_mode': 1})
        # data.update({'min_key': 0, 'max_key': 6})
        # data.update({'min_tempo': 100})
        data.update({'target_energy': 0.8})
        data.update({'target_valence': 0.95})
        data.update({'target_mode': 1})
        data.update({'target_key': 3})
        data.update({'target_tempo': 120})

    elif emotion == 'neutral':
        # data.update({'min_energy': 0, 'max_energy': 0.5})
        # data.update({'min_valence': 0.3, 'max_valence': 0.8})
        # # data.update({'min_loudness': -10, 'max_loudness': 0, 'target_loudness': -3})
        # data.update({'min_key': 0, 'max_key': 7})
        # data.update({'min_tempo': 20, 'max_tempo': 100})
        data.update({'target_energy': 0.25})
        data.update({'target_valence': 0.5})
        data.update({'target_loudness': -3})
        data.update({'target_key': 4})
        data.update({'target_tempo': 65})

    elif emotion == 'sad':
        # data.update({'min_energy': 0.1, 'max_energy': 0.6})
        # data.update({'min_valence': 0, 'max_valence': 0.3})
        # # data.update({'min_loudness': -15, 'max_loudness': 0, 'target_loudness': -7})
        # data.update({'min_mode': 0, 'max_mode': 0, 'target_mode': 0})
        # data.update({'min_key': 0, 'max_key': 6})
        # data.update({'max_tempo': 100})
        data.update({'target_energy': 0.3})
        data.update({'target_valence': 0})
        data.update({'target_loudness': -5})
        data.update({'target_mode': 0})
        data.update({'target_key': 2})
        data.update({'target_tempo': 70})

    elif emotion == 'surprise':
        # data.update({'min_energy': 0.4, 'max_energy': 0.8, 'target_energy': 0.6})
        # data.update({'min_valence': 0.1, 'max_valence': 0.3, 'target_valence': 0.2})
        # data.update({'min_key': 6, 'max_key': 11})
        # data.update({'min_tempo': 100})
        data.update({'target_energy': 0.6})
        data.update({'target_valence': 0.2})
        data.update({'target_key': 8})
        data.update({'target_tempo': 130})


def get_recommendation_request_parameters(parameters) -> dict:
    data = {
        'limit': 10,
        'market': 'PL'
    }

    set_popularity_range(parameters, data)
    set_genre_seeds(parameters, data)
    set_artists_and_songs_seeds(parameters, data)

    set_emotion_parameters(parameters['emotion'], data)

    return data


def get_recommendations(parameters) -> list:
    endpoint = "recommendations"

    tracks = []
    request_data = urlencode(get_recommendation_request_parameters(parameters))
    response = execute_spotify_api_request(endpoint=f"{endpoint}?{request_data}", request_type=RequestType.GET)

    for track in response['tracks']:
        artist_string = ""
        for i, artist in enumerate(track['artists']):
            if i > 0:
                artist_string += ", "
            name = artist['name']
            artist_string += name

        duration_seconds = int(track['duration_ms']) / 1000
        minutes, seconds = divmod(duration_seconds, 60)
        formatted_duration = "{:d}:{:02}".format(int(minutes), int(seconds))

        tracks.append({
            'title': track['name'],
            'artist_str': artist_string,
            'duration': formatted_duration,
            'image_url': track['album']['images'][0]['url'],
            'id': track['id'],
            'uri': track['uri']
        })

    return tracks
