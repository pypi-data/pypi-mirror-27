from django.db import models
from django.utils import timezone

class TestMachine(models.Model):
    host = models.CharField(null=True, max_length=50, help_text="UUID of the test machine, independent from IP address.")
    address = models.CharField(null=True,  max_length=50, help_text="Internal IP address of the test machine, at the time of registration.")
    last_contact = models.DateTimeField(editable=False, default=timezone.now)
    config = models.TextField(null=True, help_text="Host configuration, as shown to the students, in JSON format.")
    enabled = models.BooleanField(default=True, help_text="Test machines can be temporarily disabled for maintenance. All jobs are held back during that time.")


    class Meta:
        app_label = 'opensubmit'

    def __str__(self):
        if self.address:
            return self.address
        else:
            return "Test Machine {0}".format(self.pk)

