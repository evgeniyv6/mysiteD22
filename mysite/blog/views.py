from django.core.mail import send_mail
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views.generic import ListView

from .models import Post
from .forms import EmailPostForm


class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'blog/post/list.html'

def post_list(request):
    object_list = Post.published.all()
    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    #posts = Post.published.all()
    return render(request, 'blog/post/list.html', {'page': page, 'posts': posts})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,status='published', publish__year=year,
                             publish__month=month,publish__day=day)
    return render(request,'blog/post/detail.html', {'post': post})

def post_share(request, post_id):
    post = get_object_or_404(Post,id=post_id, status='published')
    sent = False
    if request.method=='POST':
        f = EmailPostForm(request.POST)
        if f.is_valid():
            cd = f.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subj = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            msg = 'Read "{}" at {}\n\n{}\'s comments:{}'.format(post.title, post_url,cd['name'],cd['comments'])
            send_mail(subj, msg, 'admin@blog.com',[cd['ti']])
            sent = True
        else:
            f = EmailPostForm()
            return render(request, 'blog/post/share.html', {'post': post, 'form': f, 'sent': sent})

