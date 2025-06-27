from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import Http404
from .models import Blog, Tag


class PostListView(ListView):
    model = Blog
    template_name = 'blog/blog_list.html'
    context_object_name = 'blogs'
    paginate_by = 10
    
    def get_queryset(self):
        """
        Return published blogs with prefetch_related
        """
        queryset = Blog.objects.filter(
            status=Blog.Status.PUBLISHED
            ).select_related().prefetch_related('tags').order_by('-publish_date')

        tag_slug = self.request.GET.get('tag')
        if tag_slug:
            if not Tag.objects.filter(slug=tag_slug).exists():
                raise Http404("Tag not found")
            else:
                queryset = queryset.filter(tags__slug=tag_slug)
        return queryset

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['current_tag'] = self.request.GET.get('tag', '')
        context['all_tags'] = Tag.objects.all()
        return context

    
class PostDetailView(DetailView):
    model = Blog
    template_name = 'blog/blog_details.html'
    context_object_name = 'blog'
    
    def get_object(self, queryset = None):
        slug = self.kwargs['slug']
        return get_object_or_404(
            Blog, slug=slug, status=Blog.Status.PUBLISHED
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ordered_sections'] = self.object.ordered_sections
        return context
    