from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.http import JsonResponse
import logging
from .models import Topic

logger = logging.getLogger('blog')


def topic_list(request):
    """View all blog topics."""
    topics = Topic.objects.all()
    logger.info("topic_list served %d topics", topics.count())
    return render(request, 'blog/topic_list.html', {'topics': topics})


def topic_detail(request, topic_id):
    """View a single topic and its comments."""
    topic = get_object_or_404(Topic, pk=topic_id)
    return render(request, 'blog/topic_detail.html', {'topic': topic})


def topic_search(request):
    """Search all topics by name or description."""
    query = request.GET.get('q', '').strip()
    results = Topic.objects.none()
    if query:
        results = Topic.objects.filter(
            Q(TopicName__icontains=query) |
            Q(TopicDescription__icontains=query)
        )
        logger.info("search q=%r returned %d results", query, results.count())
    return render(request, 'blog/topic_search.html', {
        'query': query,
        'results': results,
    })


def health_check(request):
    """Health check endpoint for the Elastic Load Balancer target group."""
    return JsonResponse({'status': 'healthy'})
