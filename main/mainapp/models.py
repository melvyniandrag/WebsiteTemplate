from django.db import models
from django.core.validators import RegexValidator

# Create your models here.
class AstronomyBlogPost(models.Model):
	Categories = [
        (0, "Interesting Fact"),
        (1, "Upcoming Event"),
        (2, "Mathematical")
	]
	title = models.TextField(
		validators = [RegexValidator('^[a-zA-Z0-9_-]+$', "only letters, numbers, hyphens and underscores")]
	)
	body = models.TextField()
	category = models.IntegerField(choices = Categories)
	
	def __str__(self):
		return self.title


	class Meta:
		db_table = "blog_posts"
