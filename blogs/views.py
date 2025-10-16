from django.urls import reverse_lazy
from django.db.models import F
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import BlogPost


class BlogListView(ListView):
    model = BlogPost
    template_name = 'blogs/blog_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return BlogPost.objects.filter(is_published=True).order_by('-created_at')


class BlogDetailView(DetailView):
    model = BlogPost
    template_name = 'blogs/blog_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        BlogPost.objects.filter(pk=obj.pk).update(views_count=F('views_count') + 1)
        obj.refresh_from_db(fields=['views_count'])
        return obj


class BlogCreateView(CreateView):
    model = BlogPost
    fields = ['title', 'content', 'preview', 'is_published']
    template_name = 'blogs/blog_form.html'

    def get_success_url(self):
        return reverse_lazy('blogs:detail', kwargs={'pk': self.object.pk})


class BlogUpdateView(UpdateView):
    model = BlogPost
    fields = ['title', 'content', 'preview', 'is_published']
    template_name = 'blogs/blog_form.html'

    def get_success_url(self):
        return reverse_lazy('blogs:detail', kwargs={'pk': self.object.pk})


class BlogDeleteView(DeleteView):
    model = BlogPost
    template_name = 'blogs/blog_confirm_delete.html'
    success_url = reverse_lazy('blogs:list')


