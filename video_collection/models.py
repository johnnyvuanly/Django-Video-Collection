from urllib import parse
from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.
class Video(models.Model):
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=400)
    notes = models.TextField(blank=True, null=True) # Allow null values in the database
    video_id = models.CharField(max_length=40, unique=True) # added unique so that you cannot add same video more than once 

    def save(self, *args, **kwargs):
        # Extract the video id from a YouTube URL

        if not self.url.startswith('https://www.youtube.com/watch'):  # We can also check if it is a YouTube url
            raise ValidationError(f'Not a YouTube URL {self.url}')

        url_components = parse.urlparse(self.url)
        query_string = url_components.query
        if not query_string:
            raise ValidationError(f'Invalid YouTube URL {self.url}')
        parameters = parse.parse_qs(query_string, strict_parsing=True) # 'v=12345678' v is the key, value is the id, dictionary
        v_parameters_list = parameters.get('v') # return None if no key found, e.g abc=1234&abc=12345678
        if not v_parameters_list: # Checking if None or empty list
            raise ValidationError(f'Invalid YouTube URL, missing parameters {self.url}')
        self.video_id = v_parameters_list[0] # string

        super().save(*args, **kwargs) # Call to Django save function

    def __str__(self):
        # String displayed in the admin console, or when printing a model object
        # You can return any useful string here
        return f'ID: {self.pk}, Name: {self.name}, URL: {self.url}, Video ID: {self.video_id} Notes: {self.notes[:200]}' # first 200 characters shown in notes