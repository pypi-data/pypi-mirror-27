import re
from .exceptions import(
    InvalidURIException,
    InvalidTrackNumber,
    InvalidTrackTime,
    InvalidSourceType,
    InvalidAlbumNameException,
    InvalidArtistNameException
)

def validate_url(uri):
    uri = uri.strip()
    pattern_url = '^(http|https)\:\/\/(([a-zA-Z0-9]|\?|\/|\=|\+|\.|\-|\_))+$'
    pattern_local_file = '^(([\.\/])*([a-zA-Z0-9\-\.\_\~]+))+$'
    regex_url = re.compile(pattern_url)
    regex_local_file = re.compile(pattern_local_file)
    if regex_url.match(uri) is None and regex_local_file.match(uri) is None:
        raise InvalidURIException
    return uri

def validate_track_number(number):
    try:
        value = int(number)
        if value < 1:
            raise InvalidTrackNumber
        return value
    except ValueError:
        raise InvalidTrackNumber

def validate_track_time(time_):
    pattern = '([\d]{2}:)?([\d]{2}:[\d]{2})$'
    regex = re.compile(pattern)
    if regex.match(time_) is None:
        raise InvalidTrackTime
    return time_

def validate_source_type(type_):
    type_ = type_.lower()
    if type_ == 'l':
        return 'local'
    return 'youtube'

def _validate_name(name, exception):
    if len(name) < 1:
        raise exception
    return name

def validate_artist_name(name):
    return _validate_name(name, InvalidArtistNameException)

def validate_album_name(name):
    return _validate_name(name, InvalidAlbumNameException)
