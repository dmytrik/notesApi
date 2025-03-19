from pydantic import BaseModel, EmailStr, field_validator

from src.auth.validators import validate_email, validate_password_strength


class BaseEmailPasswordSchema(BaseModel):
    """
        Base schema for email and password validation.

        This schema defines common fields and validation logic for email and password,
        used as a parent class for registration and login request schemas.
    """

    email: EmailStr
    password: str

    model_config = {
        "from_attributes": True
    }

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        """
            Validate the email field using a custom validator.

            Args:
                value: The email string to validate.

            Returns:
                The validated email string.
        """
        return validate_email(value)

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        """
            Validate the password field using a custom strength validator.

            Args:
                value: The password string to validate.

            Returns:
                The validated password string.
        """
        return validate_password_strength(value)


class UserRegistrationRequestSchema(BaseEmailPasswordSchema):
    """
        Schema for user registration request.

        Inherits email and password fields with validation from BaseEmailPasswordSchema.
        Used to validate data when registering a new user.
    """
    pass


class UserRegistrationResponseSchema(BaseModel):
    """
        Schema for user registration response.

        Defines the structure of the response returned after successful user registration.
    """

    id: int
    email: EmailStr

    model_config = {
        "from_attributes": True
    }


class UserLoginRequestSchema(BaseEmailPasswordSchema):
    """
        Schema for user login request.

        Inherits email and password fields with validation from BaseEmailPasswordSchema.
        Used to validate data when logging in a user.
    """
    pass


class UserLoginResponseSchema(BaseModel):
    """
        Schema for user login response.

        Defines the structure of the response returned after successful login,
        including access and refresh tokens.
    """

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenRefreshRequestSchema(BaseModel):
    """
        Schema for token refresh request.

        Defines the structure of the request
        to refresh an access token using a refresh token.
    """

    refresh_token: str


class TokenRefreshResponseSchema(BaseModel):
    """
        Schema for token refresh response.

        Defines the structure of the response returned
        after successful token refresh,
        including a new access token.
    """

    access_token: str
    token_type: str = "bearer"
