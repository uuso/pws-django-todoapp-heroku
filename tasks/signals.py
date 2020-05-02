from django.db.models.signals import m2m_changed, post_delete
from django.dispatch import receiver
from tasks.models import TodoItem, Category
from collections import Counter


receiver(post_delete, sender=TodoItem)(lambda: task_cats_removed('dummy', 'dummy', 'post_remove', 'dummy'))
# def task_removed(sender, **kwargs):
#     task_cats_removed(1,2,"post_remove",3)


@receiver(m2m_changed, sender=TodoItem.category.through)
def task_cats_added(sender, instance, action, model, **kwargs):
    print("m2m postadd?")
    if action != "post_add":
        return
    print("entered post_add")

    for cat in instance.category.all():
        Category.objects.filter(id=cat.id).update(
            todos_count = TodoItem.objects.filter(category__id=cat.id).count())
        # slug = cat.slug

        # new_count = 0
        # for task in TodoItem.objects.all():
        #     new_count += task.category.filter(slug=slug).count()
        
        # Category.objects.filter(slug=slug).update(todos_count=new_count)


@receiver(m2m_changed, sender=TodoItem.category.through)
def task_cats_removed(sender, instance, action, model, **kwargs):
    print("m2m postremove?")
    if action != "post_remove":
        return

    print("entered post_remove")
    for cat in Category.objects.all():
        Category.objects.filter(id=cat.id).update(
            todos_count = TodoItem.objects.filter(category__id=cat.id).count())
    # cat_counter = Counter()
    # for t in TodoItem.objects.all():
    #     for cat in t.category.all():
    #         cat_counter[cat.slug] += 1

    # for slug, new_count in cat_counter.items():
    #     Category.objects.filter(slug=slug).update(todos_count=new_count)