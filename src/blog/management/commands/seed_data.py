from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from datetime import date
from ...models import Topic, Comment


class Command(BaseCommand):
    help = 'Seeds the database with two topics, two comments each, and an admin user.'

    def handle(self, *args, **options):
        User = get_user_model()
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@dailyedison.com', 'Edison2026!')
            self.stdout.write(self.style.SUCCESS('Created superuser "admin".'))

        Comment.objects.all().delete()
        Topic.objects.all().delete()

        t1 = Topic.objects.create(
            TopicName='The Incandescent Light Bulb',
            TopicDescription=(
                "Thomas Edison's 1879 carbon-filament lamp was not the first electric "
                "light, but it was the first practical, long-lasting, and commercially "
                "viable one. This post explores the years of filament experiments that "
                "led to a bulb capable of burning for over 1,200 hours."
            ),
            TopicPublishingDate=date(2026, 1, 15),
        )
        Comment.objects.create(TopicID=t1, CommenterName='Nikola T.',
            CommentText='A brilliant piece of engineering, though I still prefer alternating current!')
        Comment.objects.create(TopicID=t1, CommenterName='Ada L.',
            CommentText='Fascinating detail on the filament trials. The persistence is inspiring.')

        t2 = Topic.objects.create(
            TopicName='The Phonograph: Capturing Sound',
            TopicDescription=(
                "In 1877 Edison recorded 'Mary Had a Little Lamb' onto tinfoil wrapped "
                "around a rotating cylinder, and the phonograph was born. This article "
                "traces how recorded sound moved from novelty to an industry that "
                "reshaped music, journalism, and business."
            ),
            TopicPublishingDate=date(2026, 1, 22),
        )
        Comment.objects.create(TopicID=t2, CommenterName='George W.',
            CommentText='The moment recorded sound became possible changed everything.')
        Comment.objects.create(TopicID=t2, CommenterName='Grace H.',
            CommentText='I love how the cylinder design is explained here. Very clear!')

        self.stdout.write(self.style.SUCCESS('Seeded 2 topics with 2 comments each.'))
