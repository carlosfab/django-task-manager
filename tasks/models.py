from django.db import models

# Create your models here.
class Task(models.Model):
	PRIORITY_CHOICES = [
		(1, 'Low'),
		(2, 'Medium'),
		(3, 'High'),
	]

	title = models.CharField(max_length=200)
	descrition = models.TextField(blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	due_date = models.DateTimeField(null=True, blank=True)
	priority = models.IntegerField(choices=PRIORITY_CHOICES, default=2)
	completed = models.BooleanField(default=False)

	def __str__(self):
		return self.title