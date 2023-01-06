

def get_session_key(request):
    """
    This func will simply return session key if present else None
    """
    session_key = request.session.session_key
    if not session_key:
        return None
    return session_key


def get_or_create_session_key(request):
    """
    This func will return a session key or create new session
    """
    session_key = request.session.session_key
    if not session_key:
        session_key = request.session.create()
    return session_key


