def validate_singer_data(data):
    """
    Validate singer data
    """
    errors = {}
    if not data.get('id'):
        errors['id'] = 'Singer id is required'
    if not data.get('name'):
        errors['name'] = 'Name is required'

    return errors


def validate_song_data(data):
    errors = {}
    if not data.get('title'):
        errors['title'] = 'Song title is required.'
    if not data.get('author'):
        errors['author'] = 'author is required.'
    return errors
