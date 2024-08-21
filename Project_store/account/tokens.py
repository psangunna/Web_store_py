#Esta clase se utiliza comúnmente para generar tokens asociados a restablecimientos de contraseña.
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type # biblioteca que facilita la compatibilidad entre Python 2 y Python 3: text_type se utiliza para convertir valores a texto unicode.

"""Se define un generador de tokens de activación de cuenta que hereda de PasswordResetTokenGenerator y proporciona una implementación específica 
para la creación de la cadena utilizada para generar el hash del token. Este generador personalizado es útil cuando se implementa la funcionalidad
 de activación de cuentas por correo electrónico en una aplicación Django."""
class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp): #devuelve una cadena que se utilizará para generar el hash del token.
        return (
            text_type(user.pk) + text_type(timestamp) +
            text_type(user.is_active)
        )


account_activation_token = AccountActivationTokenGenerator()