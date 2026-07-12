from enum import Enum

class UserRole(str, Enum):
    """
    Extensible User Roles.
    Roles are string-based to easily integrate with security claims.
    """
    USER = "USER"
    ADMIN = "ADMIN"
    MODERATOR = "MODERATOR"

class OTPPurpose(str, Enum):
    """
    Defines the purposes for which OTPs can be generated.
    Ensures OTPs cannot be reused across different flows (e.g. registration OTP used to reset password).
    """
    REGISTRATION = "REGISTRATION"
    LOGIN = "LOGIN"
    FORGOT_PASSWORD = "FORGOT_PASSWORD"
