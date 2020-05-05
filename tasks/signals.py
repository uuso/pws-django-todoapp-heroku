from django.db.models.signals import m2m_changed, post_delete, post_save
from django.dispatch import receiver
from tasks.models import TodoItem, Category
from collections import Counter


@receiver(post_delete, sender=TodoItem)
def task_removed(sender, **kwargs):
    print("\n\ncatched POST_DELETE @ TodoItem\n\n")
    task_cats_changed('dummy', 'dummy', 'post_remove', 'dummy')
    # task_saved(sender)
    

# @receiver(post_save, sender=TodoItem)
# def task_saved(sender, **kwargs):
#     '''при добавлении таски данный метод сработает после сохранения
#     самого TodoItem, но до сохранения его M2M поля Category.
#     Поэтому он не учтёт в подсчете текущий добавленный TodoItem.'''
    # перенесён в m2m_changed
    

    # todos_qs = TodoItem.objects.prefetch_related('category')
    
    # for cat in Category.objects.all():
    #     cat_qs = todos_qs.filter(category__id=cat.id)
    #     print(cat.slug, list(cat_qs))
        
    #     prior_high = cat_qs.filter(priority=TodoItem.PRIORITY_HIGH).count()
    #     prior_medium = cat_qs.filter(priority=TodoItem.PRIORITY_MEDIUM).count()
    #     prior_low = cat_qs.filter(priority=TodoItem.PRIORITY_LOW).count()
        
    #     cat.prior_high=prior_high
    #     cat.prior_medium=prior_medium
    #     cat.prior_low=prior_low
    #     cat.save()

@receiver(m2m_changed, sender=TodoItem.category.through)
def task_cats_changed(sender, instance, action, model, **kwargs):
    # print("got_action: " + action)
    if action == "post_add":
        # update only the instance's Categories
        qs = instance.category.all()
    elif action == "post_remove":
        # update all the Categories
        qs = Category.objects.all()
    else:
        return
    # print("catched: " + action)
    for cat in qs:
        Category.objects.filter(id=cat.id).update(
            todos_count = TodoItem.objects.filter(category__id=cat.id).count())

    # подсчет тасок по приоритетам и категориям
    todos_qs = TodoItem.objects.prefetch_related('category')
    
    for cat in Category.objects.all():
        cat_qs = todos_qs.filter(category__id=cat.id)
        # print(cat.slug, list(cat_qs))
        
        prior_high = cat_qs.filter(priority=TodoItem.PRIORITY_HIGH).count()
        prior_medium = cat_qs.filter(priority=TodoItem.PRIORITY_MEDIUM).count()
        prior_low = cat_qs.filter(priority=TodoItem.PRIORITY_LOW).count()
        
        cat.prior_high=prior_high
        cat.prior_medium=prior_medium
        cat.prior_low=prior_low
        cat.save()
