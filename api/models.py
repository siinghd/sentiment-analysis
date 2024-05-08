from django.db import models
import uuid
import hashlib

class SentimentAnalysis(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.TextField()
    text_hash = models.CharField(max_length=40, unique=True, editable=False)
    sentiment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.text_hash = hashlib.sha1(self.text.encode()).hexdigest()
        super(SentimentAnalysis, self).save(*args, **kwargs)

    @classmethod
    def get_or_create(cls, text):
        text_hash = hashlib.sha1(text.encode()).hexdigest()
        obj, created = cls.objects.get_or_create(text_hash=text_hash, defaults={'text': text})
        return obj, created
