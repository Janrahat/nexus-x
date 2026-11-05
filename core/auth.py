"""Authorization guard for active network checks."""
from .utils import confirm_authorization
def require_authorization():
    if not confirm_authorization():
        print("Authorization not confirmed; operation cancelled.")
        return False
    return True
