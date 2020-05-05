from datetime import datetime
from django.shortcuts import get_object_or_404, render
from django.http.response import HttpResponse
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.decorators.cache import cache_page
from tasks.models import TodoItem, Category



def index(request):
    counts = {c: c.todos_count for c in Category.objects.all().order_by("-todos_count")}    

    return render(request, "tasks/index.html", {"counts": counts})


def filter_tasks(tags_by_task):
    return set(sum(tags_by_task, []))


def tasks_by_cat(request, cat_slug=None):
    u = request.user
    tasks = TodoItem.objects.filter(owner=u).all()

    categories = []
    for t in tasks:
        for cat in t.category.all():
            if cat not in categories:
                categories.append(cat)

    cat = None
    if cat_slug:
        cat = get_object_or_404(Category, slug=cat_slug)
        tasks = tasks.filter(category__in=[cat])


    return render(
        request,
        "tasks/list_by_cat.html",
        {"category": cat, "tasks": tasks, 
        "categories": sorted(categories, key=lambda x: x.todos_count, reverse=True)},
    )


class TaskListView(ListView):
    model = TodoItem
    context_object_name = "tasks"
    template_name = "tasks/list.html"

    def get_queryset(self):
        u = self.request.user
        qs = super().get_queryset()
        return qs.filter(owner=u)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_tasks = self.get_queryset()
        tags = []
        for t in user_tasks:
            tags.append(list(t.category.all()))
        context["categories"] = sorted(
            filter_tasks(tags), key=lambda cat: cat.todos_count, reverse=True)

        # categories = []
        # for cat in t.category.all():
        #     if cat not in categories:
        #         categories.append(cat)
        # context["categories"] = categories

        return context


class TaskDetailsView(DetailView):
    model = TodoItem
    template_name = "tasks/details.html"

@cache_page(300)
def cached_page(request):
    return HttpResponse(f"<p>Cached time: {datetime.now().isoformat()}</p><p>Wait 5 minutes to update.</p>")
