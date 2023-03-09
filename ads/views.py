import json

from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView

from ads.models import Announcements, Category


# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class AnnouncementsView(View):

    def get(self, request):
        announce = Announcements.objects.all()

        response = []
        for i in announce:
            response.append({
                "id": i.pk,
                "name": i.name,
                "author": i.author,
                "price": i.price,
            })
        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False})

    def post(self, request):
        announce_data = json.loads(request.body)

        announce = Announcements()

        announce.name = announce_data["name"]
        announce.author = announce_data["author"]
        announce.price = announce_data["price"]
        announce.description = announce_data["description"]
        announce.address = announce_data["address"]
        announce.is_published = announce_data["is_published"]

        announce.save()

        return JsonResponse({
            "id": announce.pk,
            "name": announce.name,
            "author": announce.author,
            "price": announce.price,
            "description": announce.description,
            "address": announce.address,
            "is_published": announce.is_published,
        })

class AnnouncementsDetailView(DetailView):
    model = Announcements

    def get(self, request, *args, **kwargs):
        announce = self.get_object()

        return JsonResponse({
            "id": announce.pk,
            "name": announce.name,
            "author": announce.author,
            "price": announce.price,
            "description": announce.description,
            "address": announce.address,
            "is_published": announce.is_published,
        })



@method_decorator(csrf_exempt, name='dispatch')
class CategoryView(View):

    def get(self, request):
        categories = Category.objects.all()

        response = []
        for category in categories:
            response.append({
                "id": category.pk,
                "name": category.category_name,
            })
        return JsonResponse(response, safe=False, json_dumps_params={"ensure_ascii": False})

    def post(self, request):
        category_data = json.loads(request.body)

        category = Category()
        category.category_name = category_data["name"]
        category.save()

        return JsonResponse({
            "id": category.pk,
            "name": category.category_name,
        })


class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        category = self.get_object()

        return JsonResponse({
            "id": category.pk,
            "name": category.category_name,
        })
