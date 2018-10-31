from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.utils import timezone


class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = CharField(_("Name of User"), blank=True, max_length=255)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})


# keep encrypted passwords around to ensure that user does not re-use
# any of the previous 10
class PasswordHistoryItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()  # password becomes invalid at...
    locked_until = models.DateTimeField()  # password cannot be changed until
    encrypted_password = models.CharField(_("password"), max_length=128)

    class Meta:
        get_latest_by = "created"

    @classmethod
    def current_for_user(cls, user):
        return user.passwordhistoryitem_set.latest()

    def can_change_password(self):
        now = timezone.now()
        return now > self.locked_until

    def must_change_password(self):
        now = timezone.now()
        return self.expires_at < now


# User Failed Login Attempts
class FailedLoginAttempt(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # comma-separated timestamp values, right now it's a 10 digit number,
    # so we can store about 91 last failed attempts
    failed_attempts = models.CharField(max_length=1000)

    def __unicode__(self):
        attempts_no = (
            0 if not self.failed_attempts else len(self.failed_attempts.split(","))
        )
        return "%s has %s failed login attempts" % (self.user, attempts_no)

    def clean_attempts(self, timestamp):
        """ Leave only those that happened after <timestamp> """
        attempts = self.failed_attempts.split(",")
        self.failed_attempts = ",".join([fa for fa in attempts if int(fa) >= timestamp])

    def failed(self, timestamp):
        """ Add another failed attempt """
        attempts = self.failed_attempts.split(",") if self.failed_attempts else []
        attempts.append(str(int(timestamp)))
        self.failed_attempts = ",".join(attempts)

    def too_many_attempts(self, value, timestamp):
        """ Compare number of failed attempts to <value> """
        self.clean_attempts(timestamp)
        attempts = self.failed_attempts.split(",")
        return len(attempts) > value


class TemporaryLockout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
