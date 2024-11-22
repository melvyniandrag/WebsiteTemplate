from django import forms
from .models import AstronomyBlogPost

class AstronomyBlogPostForm(forms.ModelForm):
	class Meta:
		model = AstronomyBlogPost
		fields = [
			"title",
			"body",
			"category"
		]
