from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import ClothingItem, Category, Size, ClothingItemSize

from django.db.models import Q


class CatalogView(ListView):
    model = ClothingItem
    template_name = "main/product/list.html"
    context_object_name = "clothing_items"

    def get_queryset(self):
        queryset = super().get_queryset()
        category_slugs = self.request.GET.getlist("category")
        size_names = self.request.GET.getlist("size")
        min_price = self.request.GET.get("min_price")
        max_price = self.request.GET.get("max_price")

        if category_slugs:
            queryset = queryset.filter(category__slug__in=category_slugs)

        if size_names:
            queryset = queryset.filter(
                Q(size__name__in=size_names)
                & Q(sizes__clothingitemsize__available=True)
            ).distinct()

        if min_price:
            queryset = queryset.filter(price__gte=min_price)

        if max_price:
            queryset = queryset.filter(price__lte=max_price)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["sizes"] = Size.objects.all()
        context["selected_cateqories"] = self.request.GET.getlist("category")
        context["selected_sizes"] = self.request.GET.getlist("size")
        context["min_prise"] = self.request.GET.get("min_prise", "")
        context["max_prise"] = self.request.GET.get("max_prise", "")
        return context


class ClothingItemDetailView(DetailView):
    model = ClothingItem
    template_name = "main/product/detail.html"
    context_object_name = "clothing_item"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        clothing_item = self.get_object()
        available_sizes = ClothingItemSize.objects.filter(
            clothing_item=clothing_item, available=True
        )
        context["available_sizes"] = available_sizes
        return context


# from django.shortcuts import render
# from .models import ClothingItem, Category, Size

# def catalog_view(request):
#     clothing_items = ClothingItem.objects.all()
#     categories = Category.objects.all()
#     sizes = Size.objects.all()

#     selected_categories = request.GET.getlist('category')
#     selected_sizes = request.GET.getlist('size')

#     context = {
#         'clothing_items': clothing_items,
#         'categories': categories,
#         'sizes': sizes,
#         'selected_categories': selected_categories,
#         'selected_sizes': selected_sizes,
#     }
#     return render(request, 'main/product/list.html', context)