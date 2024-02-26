from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render

from .models import Category, Poi


def poi_list_view(request):
    id_search = request.GET.get("id_search", "").strip()
    external_id_search = request.GET.get(
        "external_id_search", ""
    ).strip()
    filter_query = request.GET.get("filter", "").strip()

    categories = Category.objects.all().order_by("name")
    page_obj = None

    if id_search or external_id_search or filter_query:
        query = Q()

        if id_search:
            query &= Q(id=int(id_search))
        if external_id_search:
            query &= Q(external_id=external_id_search)
        if filter_query:
            query &= Q(category__name=filter_query)

        result_list = (
            Poi.objects.filter(query)
            .select_related("category")
            .order_by("id")
        )
        paginator = Paginator(result_list, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

    return render(
        request,
        "searchfilter_template.html",
        {
            "page_obj": page_obj,
            "categories": categories,
            "selected_filter": filter_query,
        },
    )
