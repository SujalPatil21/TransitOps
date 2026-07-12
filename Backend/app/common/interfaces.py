from abc import ABC, abstractmethod

class BaseNotificationService(ABC):
    """
    Abstract interface for notification providers (Dependency Inversion Principle).
    Allows swapping email sending or migrating to SMS/Push notifications
    without changing the core auth service.
    """

    @abstractmethod
    def send_registration_otp(self, email: str, username: str, otp: str, expires_in_seconds: int) -> bool:
        """
        Send the email verification OTP to a newly registered user.
        """
        pass

    @abstractmethod
    def send_login_otp(self, email: str, username: str, otp: str, expires_in_seconds: int) -> bool:
        """
        Send the login verification OTP to a logging in user.
        """
        pass

    @abstractmethod
    def send_forgot_password_otp(self, email: str, username: str, otp: str, expires_in_seconds: int) -> bool:
        """
        Send the password reset verification OTP to a user.
        """
        pass
