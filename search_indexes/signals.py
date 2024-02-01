from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from django_elasticsearch_dsl.registries import registry

from article.models import Article

@receiver(post_save)
def update_document(sender, instance, **kwargs):
    app_label = sender._meta.app_label

    if sender is Article:
        return

    """
        Update elasticsearch records when a related model changes.
    """
    if app_label == 'articles':
        instances = instance.articles.all()
        print('eraan')
        for _instance in instances:
            registry.update(_instance)

@receiver(post_delete)
def update_document(sender, instance, **kwargs):
    app_label = sender._meta.app_label

    if sender is Article:
        return

    """
        Update elasticsearch records when a related model has been deleted.
    """
    if app_label == 'articles':
        # re-index
        instances = Article.objects.all()
        for _instance in instances:
            registry.update(_instance)