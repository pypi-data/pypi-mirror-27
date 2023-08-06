from django.db import models

from simple_diff.models import ModelDiffMixin


class TestDiff(ModelDiffMixin, models.Model):
    name = models.CharField(max_length=100)
    number = models.IntegerField(default=0)
    test_date = models.DateField(blank=True, null=True)

    recorded_name_change = 0

    def on_name_change(self, old, new):
        self.recorded_name_change += 1
        self.save()
