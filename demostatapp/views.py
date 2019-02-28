from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, get_list_or_404, render
from django.urls import reverse
from django.views import generic
from django.utils import timezone
import datetime

from .models import Organisation, Demo

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'demostatapp/index.html'
    context_object_name = 'demo_list'

    def get_queryset(self):
        return Demo.objects.filter(date__gt=timezone.now().date(), date__lt=timezone.now().date()+datetime.timedelta(weeks=4)).order_by('date')

def demos(request):
    return HttpResponse('hi')

#class DemoView(generic.DetailView):
#    model = Demo
#    template_name = 'demostatapp/demo_detail.html'

def demo(request, date__year, date__month, date__day, slug):
    demo = get_object_or_404(Demo, date__year=date__year, date__month=date__month, date__day=date__day, slug=slug)

    return render(request, 'demostatapp/demo_detail.html', {'demo': demo})

def demo_id(request, demo_id):
    demo = get_object_or_404(Demo, pk=demo_id)
    return HttpResponseRedirect(reverse('demo', args=(demo.slug,)))

class OrganisationView(generic.DetailView):
    model = Organisation
    template_name = 'demostatapp/organisation_detail.html'

def tag(response, tag_slug):
    demo_list = get_list_or_404(Demo, tags__slug__exact=tag_slug, date__gt=timezone.now().date(), date__lt=timezone.now().date()+datetime.timedelta(weeks=4))
    tag_name = tag_slug

    for tag in demo_list[0].tags.all():
        if tag.slug == tag_slug:
            tag_name = tag.name
            break

    return render(response, 'demostatapp/tag_detail.html', {'tag_slug': tag_slug, 'tag_name': tag_name, 'demo_list': demo_list})
