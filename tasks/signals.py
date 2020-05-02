from django.db.models.signals import m2m_changed, post_delete
from django.dispatch import receiver
from tasks.models import TodoItem, Category
from collections import Counter


@receiver(post_delete, sender=TodoItem)
def task_removed(sender, **kwargs):
    task_cats_changed('dummy', 'dummy', 'post_remove', 'dummy')


@receiver(m2m_changed, sender=TodoItem.category.through)
def task_cats_changed(sender, instance, action, model, **kwargs):
    if action == "post_add":
        qs = instance.category.all()
    else if action == "post_remove":
        qs = Category.objects.all()
    else:
        return

    for cat in qs:
        Category.objects.filter(id=cat.id).update(
            todos_count = TodoItem.objects.filter(category__id=cat.id).count())
