from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    # make the token with time stamp
    """
        The token needs to have some properties for it to be secure:

        1- It should not be possible for users to create their own token.
        2- Tokens should expire, so that they are not valid forever.
        3- Tokens should be invalidated once used.

    """
    def _make_hash_value(self, user, timestamp):
        return (
            text_type(user.pk) + text_type(timestamp) + text_type(user.is_active)
        )

account_activation_token = AccountActivationTokenGenerator()