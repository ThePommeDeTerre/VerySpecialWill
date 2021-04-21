from flask import session
import secrets


def start_session(app):
    if session.get("s_key") is None:
        session["s_key"] = secrets.token_urlsafe(16)
    return

