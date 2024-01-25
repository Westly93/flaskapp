from functools import wraps
from flask import abort
from flask_login import current_user

def role_required(*required_roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            if not current_user.is_authenticated:
                # Redirect to login page or handle unauthenticated users
                return redirect(url_for('auth.login'))

            if not any(current_user.has_role(role) for role in required_roles):
                # Handle unauthorized access
                abort(403)  # Alternatively, you can render a custom error page
           
            return view_func(*args, **kwargs)

        return wrapper

    return decorator