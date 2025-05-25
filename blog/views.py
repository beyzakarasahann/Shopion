from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .models import Article,Category
from .forms import CommentForm



def blog_list(request):
    articles = Article.objects.filter(is_approved=True).order_by('-created_at')
    categories = Category.objects.all()
    popular_articles = Article.objects.filter(is_approved=True).order_by('-id')[:5]

    paginator = Paginator(articles, 4)  # Her sayfada 4 makale
    page = request.GET.get('page')
    articles = paginator.get_page(page)

    return render(request, 'blog/blog_list.html', {
        'articles': articles,
        'categories': categories,
        'popular_articles': popular_articles,
    })

def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk, is_approved=True)
    comments = article.comments.filter(is_approved=True).order_by('-created_at')
    form = CommentForm()

    return render(request, 'blog/article_detail.html', {
        'article': article,
        'comments': comments,
        'form': form
    })


def add_comment(request, pk):
    article = get_object_or_404(Article, pk=pk, is_approved=True)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.article = article
            new_comment.user = request.user
            new_comment.save()  # is_approved default False
            return redirect('article_detail', pk=article.pk)

    return redirect('article_detail', pk=article.pk)
