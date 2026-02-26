import secrets
import string


def generate_short_code(length: int = 7) -> str:
    """Generate a cryptographically secure random short code.
    
    Uses a mix of lowercase, uppercase letters and digits.
    7 characters = 62^7 ≈ 3.5 trillion possible combinations.
    """
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))
