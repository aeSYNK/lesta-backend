from django.db import models
from django.core.exceptions import ValidationError


class Document(models.Model):
    file = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)

    def clean(self):
        if not self.file.name.endswith('.txt'):
            raise ValidationError("Only text files are accepted")

    def __str__(self):
        return self.file.name


class WordStat(models.Model):
    document = models.ForeignKey(
        Document, on_delete=models.CASCADE, related_name='word_stats'
    )
    word = models.CharField(max_length=100)
    tf = models.FloatField(help_text="Term Frequency")
    idf = models.FloatField(
        null=True, blank=True, help_text="Inverse Document Frequency"
    )

    class Meta:
        indexes = [
            models.Index(fields=['word']),
            models.Index(fields=['idf']),
        ]

    def __str__(self):
        return f"{self.word} (tf: {self.tf}, idf: {self.idf})"
