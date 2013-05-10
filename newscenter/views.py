from django import http, shortcuts, template
from django.conf import settings
from newscenter import models
from django.views.generic.dates import YearArchiveView, MonthArchiveView
from django.contrib.sites.models import Site
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import get_object_or_404


class NmMixin(object):
    date_field = 'release_date'
    make_object_list = True

    def get_queryset(self):
        self.newsroom = self.kwargs['newsroom']
        return models.Article.objects.get_published().filter(newsroom__slug=self.kwargs['newsroom'])

    def get_context_data(self, **kwargs):
        context = super(NmMixin, self).get_context_data(**kwargs)
        context['newsroom'] = self.kwargs['newsroom']
        return context


class NmYearArchive(NmMixin, YearArchiveView):
    pass


class NmMonthArchive(NmMixin, MonthArchiveView):
    pass


archive_year = NmYearArchive.as_view()
archive_month = NmMonthArchive.as_view()


def article_detail(request, newsroom, year, month, slug):
    request,
    year = year,
    month = month,
    article = get_object_or_404(models.Article.objects.get_published(), slug__exact=slug)
    newsroom = article.newsroom
    return shortcuts.render_to_response(
        'newscenter/article_detail.html', locals(),
        context_instance=template.RequestContext(request))

def category_detail(request, slug):
    category = models.Category.objects.get(slug__exact=slug)
    article_list = category.articles.get_published()
    return shortcuts.render_to_response(
        'newscenter/category_detail.html', 
        {'category': category, 'article_list': article_list,},
        context_instance=template.RequestContext(request))

def newsroom_detail(request, slug):
    site = Site.objects.get_current()
    newsroom = get_object_or_404(models.Newsroom, slug__exact=slug)
    article_list = newsroom.articles.get_published()
    paginator = Paginator(article_list, 10)
    page = int(request.GET.get('page', '1'))
    article_list = paginator.page(page)

    return shortcuts.render_to_response(
        'newscenter/newsroom.html', locals(),
        context_instance=template.RequestContext(request))
