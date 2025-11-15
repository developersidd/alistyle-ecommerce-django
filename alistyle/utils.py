def get_session_key(request):
    session_key = request.session.session_key
    if not session_key:
        session_key = request.session.create()
    return session_key
