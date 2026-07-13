from django.db import models


class Topic(models.Model):
    """A blog topic/post for The Daily Thomas Edison."""
    TopicID = models.AutoField(primary_key=True)
    TopicName = models.CharField(max_length=200)
    TopicDescription = models.TextField()
    TopicPublishingDate = models.DateField()

    class Meta:
        ordering = ['-TopicPublishingDate']

    def __str__(self):
        return self.TopicName


class Comment(models.Model):
    """A reader comment attached to a Topic."""
    CommentNumber = models.AutoField(primary_key=True)
    CommenterName = models.CharField(max_length=150)
    CommentText = models.TextField()
    # Foreign key implements the "TopicID" relationship in the spec.
    TopicID = models.ForeignKey(
        Topic,
        on_delete=models.CASCADE,
        related_name='comments',
        db_column='TopicID',
    )

    class Meta:
        ordering = ['CommentNumber']

    def __str__(self):
        return f"Comment #{self.CommentNumber} by {self.CommenterName}"
