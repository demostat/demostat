from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.utils.http import urlencode
from django.conf import settings
from django.db.models import Q
import datetime
from .utils import Querystring

from . import version, release, develop

from .models import Organisation, Demo, Tag

def make_context_object(context):
    s = {}

    s['DEMOSTAT_VERSION'] = version
    s['DEMOSTAT_RELEASE'] = release
    s['DEMOSTAT_DEVELOP'] = develop

    try:
        s['SITE_TITLE'] = settings.SITE_TITLE
    except:
        pass

    try:
        s['SITE_IMPRINT_URL'] = settings.SITE_IMPRINT_URL
    except:
        pass

    try:
        s['SITE_PRIVACY_URL'] = settings.SITE_PRIVACY_URL
    except:
        pass

    # https://leafletjs.com/reference-1.4.0.html#tilelayer
    try:
        if settings.DEMOSTAT_LEAFLET['url'] and settings.DEMOSTAT_LEAFLET['attribution'] and settings.DEMOSTAT_LEAFLET['maxZoom']:
            s['DEMOSTAT_LEAFLET'] = settings.DEMOSTAT_LEAFLET
    except:
        pass

    return {**s, **context}

def to_slug_array(dicts):
    out = []
    for dict in dicts:
        out.append(dict.slug)
    return out

def filter_it(demo_list, get):
    filter = {}

    if "tag" in get:
        filter["tag"] = []

        for tag in sorted(get.getlist("tag")):
            try:
                tag = Tag.objects.get(slug=tag)
                filter["tag"].append(tag)
            except:
                pass

        if len(filter["tag"]):
            demo_list = demo_list.filter(tags__slug__in=to_slug_array(filter["tag"]))

    if "org" in get:
        filter["org"] = []

        for org in sorted(get.getlist("org")):
            try:
                org = Organisation.objects.get(slug=org)
                filter["org"].append(org)
            except:
                pass

        if len(filter["org"]):
            demo_list = demo_list.filter(organisation__slug__in=to_slug_array(filter["org"]))

    demo_list = demo_list.distinct()

    return demo_list, filter

# Create your views here.
def IndexView(request):
    demo_list = Demo.objects.filter(date__gt=timezone.now().date(), date__lt=timezone.now().date()+datetime.timedelta(weeks=4)).order_by('date')
    demo_next = Demo.objects.filter(date__gte=datetime.datetime(timezone.now().year, timezone.now().month, timezone.now().day)).order_by('date').first()

    return render(request, 'demostat/index.html', make_context_object({
        'demo_list': demo_list,
        'demo_next': demo_next,
    }))

def demos(request):
    demo_list = Demo.objects.all().order_by('date')

    if not demo_list:
        raise Http404()

    #=== FILTER ===

    demo_list, filter = filter_it(demo_list, request.GET)

    #=== FILTER ===

    return render(request, 'demostat/demos_list.html', make_context_object({
        'demo_list': demo_list,
        'filter': filter,
    }))

def demos_year(request, date__year):
    demo_list = Demo.objects.filter(date__year=date__year).order_by('date')

    if not demo_list:
        raise Http404()

    #=== FILTER ===

    demo_list, filter = filter_it(demo_list, request.GET)

    #=== FILTER ===

    demo_prev = Demo.objects.filter(date__year__lt=date__year).order_by('date').last()
    demo_next = Demo.objects.filter(date__year__gt=date__year).order_by('date').first()

    return render(request, 'demostat/demos_year_list.html', make_context_object({
        'date': datetime.date(int(date__year), 1, 1),
        'demo_list': demo_list,
        'demo_prev': demo_prev,
        'demo_next': demo_next,
        'filter': filter,
    }))

def demos_month(request, date__year, date__month):
    demo_list = Demo.objects.filter(date__year=date__year, date__month=date__month).order_by('date')

    if not demo_list:
        raise Http404()

    #=== FILTER ===

    demo_list, filter = filter_it(demo_list, request.GET)

    #=== FILTER ===

    demo_prev = Demo.objects.filter(date__year__lte=date__year, date__month__lt=date__month).order_by('date').last()
    demo_next = Demo.objects.filter(date__year__gte=date__year, date__month__gt=date__month).order_by('date').first()

    return render(request, 'demostat/demos_month_list.html', make_context_object({
        'date': datetime.date(int(date__year), int(date__month), 1),
        'demo_list': demo_list,
        'demo_prev': demo_prev,
        'demo_next': demo_next,
        'filter': filter,
    }))

def demos_day(request, date__year, date__month, date__day):
    return HttpResponseRedirect(reverse('demostat:demos_month', args=(date__year, date__month)) + '#' + date__day)


def demo(request, date__year, date__month, date__day, slug):
    demo = get_object_or_404(Demo, date__year=date__year, date__month=date__month, date__day=date__day, slug=slug)

    return render(request, 'demostat/demo_detail.html', make_context_object({
        'demo': demo,
    }))

def demo_id(request, demo_id):
    demo = get_object_or_404(Demo, pk=demo_id)
    return HttpResponseRedirect(reverse('demostat:demo', args=(demo.date.strftime("%Y"), demo.date.strftime("%m"), demo.date.strftime("%d"), demo.slug)))

def OrganisationView(request, slug):
    organisation = get_object_or_404(Organisation, slug=slug)
    demo_list = Demo.objects.filter(date__gt=timezone.now().date(), date__lt=timezone.now().date()+datetime.timedelta(weeks=4), organisation__slug=slug).order_by('date')

    return render(request, 'demostat/organisation_detail.html', make_context_object({
        'organisation': organisation,
        'demo_list': demo_list,
    }))

def tag(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    demo_list = Demo.objects.filter(date__gt=timezone.now().date(), date__lt=timezone.now().date()+datetime.timedelta(weeks=4), tags__slug=tag_slug).order_by('date')

    return render(request, 'demostat/tag_detail.html', make_context_object({
        'tag': tag,
        'demo_list': demo_list,
    }))

def AboutView(request):
    return render(request, 'demostat/about.html', make_context_object({}))
