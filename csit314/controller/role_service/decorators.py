from flask import g, render_template, session
from functools import wraps

def agent_only(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user and g.user.role == 'agent':
            return view(*args, **kwargs)
        else:
            return render_template('error/error.html',
                                   message='Available only to agents.'), 403
    return wrapped_view

def buyer_only(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user and g.user.role == 'buyer':
            return view(*args, **kwargs)
        else:
            return render_template('error/error.html',
                                   message='Available only to buyers.'), 403
    return wrapped_view

def seller_only(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user and g.user.role == 'seller':
            return view(*args, **kwargs)
        else:
            return render_template('error/error.html',
                                   message='Available only to sellers.'), 403
    return wrapped_view

def buyer_seller_only(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user and g.user.role == 'buyer' or g.user.role == 'seller':
            return view(*args, **kwargs)
        else:
            return render_template('error/error.html',
                                   message='Available only to buyers and sellers.'), 403
    return wrapped_view


def admin_only(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user and g.user.role == 'admin':
            return view(*args, **kwargs)
        else:
            return render_template('error/error.html',
                                   message='Available only to admin.'), 403
    return wrapped_view

def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user:
            return view(*args, **kwargs)
        else:
            return render_template('error/error.html',
                                   message='Login required'), 401
    return wrapped_view

def suspended(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if not g.user or g.user.status == "Active":
            return view(*args, **kwargs)
        else:
            return render_template('error/error.html',
                                   message='Your account is suspended.'
                                           'Send Active Request to Administrator.'
                                           'admin@minyong.com'), 403
    return wrapped_view

def is_logged_in():
    # check logged in status
    return 'user_id' in session

def already_logged_in(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if not is_logged_in():
            return view(*args, **kwargs)
        else:
            return render_template('error/error.html',
                                   message='You are already logged in. Logout first.'), 403
    return wrapped_view

