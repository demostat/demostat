from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.utils.http import urlencode
import datetime

from .models import Organisation, Demo

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'demostatapp/index.html'
    context_object_name = 'context'

    def get_queryset(self):
        demo_list = Demo.objects.filter(date__gt=timezone.now().date(), date__lt=timezone.now().date()+datetime.timedelta(weeks=4)).order_by('date')
        demo_next = Demo.objects.filter(date__gte=datetime.datetime(timezone.now().year, timezone.now().month, timezone.now().day)).order_by('date').first()

        return {
            'demo_list': demo_list,
            'demo_next': demo_next,
        }

def demos(request):
    demo_list = get_list_or_404(Demo)

    return render(request, 'demostatapp/demos_list.html', {
        'demo_list': demo_list
    })

def demos_year(request, date__year):
    demo_list = get_list_or_404(Demo, date__year=date__year)
    demo_prev = Demo.objects.filter(date__year__lt=date__year).order_by('date').last()
    demo_next = Demo.objects.filter(date__year__gt=date__year).order_by('date').first()

    return render(request, 'demostatapp/demos_year_list.html', {
        'date': datetime.date(int(date__year), 1, 1),
        'demo_list': demo_list,
        'demo_prev': demo_prev,
        'demo_next': demo_next,
    })

def demos_month(request, date__year, date__month):
    demo_list = Demo.objects.filter(date__year=date__year, date__month=date__month).order_by('date')

    if not demo_list:
        raise Http404()

    if 'tag' in request.GET:
        demo_list = demo_list.filter(tags__slug__in=request.GET.getlist('tag'))

    if 'org' in request.GET:
        demo_list = demo_list.filter(organisation__slug=request.GET['org'])

    demo_prev = Demo.objects.filter(date__year__lte=date__year, date__month__lt=date__month).order_by('date').last()
    demo_next = Demo.objects.filter(date__year__gte=date__year, date__month__gt=date__month).order_by('date').first()

    return render(request, 'demostatapp/demos_month_list.html', {
        'date': datetime.date(int(date__year), int(date__month), 1),
        'demo_list': demo_list,
        'demo_prev': demo_prev,
        'demo_next': demo_next,
        'filter_tag': sorted(request.GET.getlist('tag')),
        'filter_org': request.GET.get('org'),
    })

def demos_day(request, date__year, date__month, date__day):
    return HttpResponseRedirect(reverse('demostatapp:demos_month', args=(date__year, date__month)) + '#' + date__day)


def demo(request, date__year, date__month, date__day, slug):
    demo = get_object_or_404(Demo, date__year=date__year, date__month=date__month, date__day=date__day, slug=slug)

    return render(request, 'demostatapp/demo_detail.html', {
        'demo': demo
    })

def demo_id(request, demo_id):
    demo = get_object_or_404(Demo, pk=demo_id)
    return HttpResponseRedirect(reverse('demostatapp:demo', args=(demo.date.strftime("%Y"), demo.date.strftime("%m"), demo.date.strftime("%d"), demo.slug)))

class OrganisationView(generic.DetailView):
    model = Organisation
    template_name = 'demostatapp/organisation_detail.html'

def tag(request, tag_slug):
    demo_list = get_list_or_404(Demo, tags__slug__exact=tag_slug, date__gt=timezone.now().date(), date__lt=timezone.now().date()+datetime.timedelta(weeks=4))
    tag_name = tag_slug

    for tag in demo_list[0].tags.all():
        if tag.slug == tag_slug:
            tag_name = tag.name
            break

    return render(request, 'demostatapp/tag_detail.html', {
        'tag_slug': tag_slug,
        'tag_name': tag_name,
        'demo_list': demo_list
    })
