def is_valid_email(email: str) -> bool:
    import re
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regex, email) is not None

def is_strong_password(password: str) -> bool:
    return (len(password) >= 8 and 
            any(char.isdigit() for char in password) and 
            any(char.isalpha() for char in password) and 
            any(char in "!@#$%^&*()-_=+[]{}|;:,.<>?/" for char in password))

def validate_account_data(username: str, email: str, password: str) -> list:
    errors = []
    if not username:
        errors.append("Username is required.")
    if not is_valid_email(email):
        errors.append("Invalid email format.")
    if not is_strong_password(password):
        errors.append("Password must be at least 8 characters long, contain letters, numbers, and special characters.")
    return errors