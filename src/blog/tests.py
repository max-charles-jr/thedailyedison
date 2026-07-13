from django.test import TestCase
from django.urls import reverse
from datetime import date
from .models import Topic, Comment


class ModelTests(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(
            TopicName='Test Topic', TopicDescription='A description',
            TopicPublishingDate=date(2026, 1, 1))
        Comment.objects.create(TopicID=self.topic, CommenterName='Tester',
            CommentText='Nice post')

    def test_topic_str(self):
        self.assertEqual(str(self.topic), 'Test Topic')

    def test_comment_relationship(self):
        self.assertEqual(self.topic.comments.count(), 1)
        self.assertEqual(self.topic.comments.first().CommenterName, 'Tester')


class ViewTests(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(
            TopicName='Incandescent Light', TopicDescription='About bulbs',
            TopicPublishingDate=date(2026, 1, 1))

    def test_topic_list_view(self):
        resp = self.client.get(reverse('blog:topic_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Incandescent Light')

    def test_topic_detail_view(self):
        resp = self.client.get(reverse('blog:topic_detail', args=[self.topic.TopicID]))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'About bulbs')

    def test_search_finds_topic(self):
        resp = self.client.get(reverse('blog:topic_search'), {'q': 'Incandescent'})
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Incandescent Light')

    def test_search_no_match(self):
        resp = self.client.get(reverse('blog:topic_search'), {'q': 'zzzzz'})
        self.assertContains(resp, 'No topics matched')

    def test_health_check(self):
        resp = self.client.get(reverse('blog:health_check'))
        self.assertEqual(resp.status_code, 200)
        self.assertJSONEqual(resp.content, {'status': 'healthy'})
