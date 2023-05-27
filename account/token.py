from django.contrib.auth.tokens import PasswordResetTokenGenerator


class ActivationTokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        return f"{user.username}{timestamp}{user.pk}{user.email}"

AccountActivationTokenGenerator = ActivationTokenGenerator()
