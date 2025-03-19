import re

import email_validator


def validate_password_strength(password: str) -> str:
    """
    Validate the strength of a password.

    Ensures the password meets minimum security requirements, including length,
    character types, and special characters.

    Args:
        password: The plain text password to validate.

    Returns:
        The validated password string if it meets all requirements.

    Raises:
        ValueError: If the password fails any of the following checks:
            - Less than 8 characters.
            - No uppercase letters.
            - No lowercase letters.
            - No digits.
            - No special characters (@, $, !, %, *, ?, #, &).
    """
    if len(password) < 8:
        raise ValueError("Password must contain at least 8 characters.")
    if not re.search(r"[A-Z]", password):
        raise ValueError(
            "Password must contain at least one uppercase letter."
        )
    if not re.search(r"[a-z]", password):
        raise ValueError("Password must contain at least one lower letter.")
    if not re.search(r"\d", password):
        raise ValueError("Password must contain at least one digit.")
    if not re.search(r"[@$!%*?&#]", password):
        raise ValueError(
            "Password must contain at least one special character: @, $, !, %, *, ?, #, &."
        )
    return password


def validate_email(user_email: str) -> str:
    """
    Validate and normalize an email address.

    Uses email-validator to check the email format and optionally normalize it.

    Args:
        user_email: The email address to validate.

    Returns:
        The normalized email address string.

    Raises:
        ValueError: If the email is invalid (e.g., incorrect format or syntax).
    """
    try:
        email_info = email_validator.validate_email(
            user_email, check_deliverability=False
        )
        email = email_info.normalized
    except email_validator.EmailNotValidError as error:
        raise ValueError(str(error))
    else:
        return email
