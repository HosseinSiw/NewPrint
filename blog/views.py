from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Blog


class PostListView(ListView):
    model = Blog
    template_name = 'blog/blog_list.html'
    context_object_name = 'blogs'
    paginate_by = 10

    def get_queryset(self):
        """
        Return published blogs with prefetch_related for performance
        """
        queryset = Blog.objects.filter(
            status=Blog.Status.PUBLISHED
            ).select_related().prefetch_related('tags').order_by('-publish_date')

        return queryset

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # Add popular tags to context
    #     context['popular_tags'] = Tag.objects.annotate(
    #         num_blogs=Count('blogs')
    #     ).order_by('-num_blogs')[:10]

    #     # Add current tag to context if filtering
    #     tag_slug = self.kwargs.get('tag_slug')
    #     if tag_slug:
    #         context['current_tag'] = get_object_or_404(Tag, slug=tag_slug)

    #     return context
    
    
class PostDetailView(DetailView):
    model = Blog
    template_name = 'blog/blog_details.html'
    context_object_name = 'blog'
    
    def get_object(self, queryset = None):
        slug = self.kwargs['slug']
        return get_object_or_404(
            Blog, slug=slug, 
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ordered_sections'] = self.object.ordered_sections
        return context
    