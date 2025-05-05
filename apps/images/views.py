from django.views.generic import TemplateView, ListView, View
from django.shortcuts import get_object_or_404, render
from django.http import FileResponse, HttpResponseForbidden
from django.core.paginator import InvalidPage
import logging
from .models import CarouselImage, Image

logger = logging.getLogger(__name__)


class CarouselFragmentView(TemplateView):
    template_name = "images/components/carousel_fragment.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["carousel_images"] = CarouselImage.objects.only("image")[:10]
        context["carousel_title"] = "Entre tradition et modernité ..."
        return context


class ImageWallView(ListView):
    model = Image
    template_name = "images/image_wall.html"
    context_object_name = "images"
    paginate_by = 10

    def get_queryset(self):
        return Image.objects.order_by("-uploaded_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_obj"] = context["page_obj"]
        return context

    def render_to_response(self, context, **response_kwargs):
        if self.request.htmx:
            return render(
                self.request,
                "images/partials/_image_list.html",
                context,
                **response_kwargs,
            )
        return super().render_to_response(context, **response_kwargs)

    def paginate_queryset(self, queryset, page_size):
        paginator = self.get_paginator(
            queryset, page_size, allow_empty_first_page=True
        )
        page_number = self.request.GET.get("page") or 1
        try:
            page = paginator.page(page_number)
        except InvalidPage:
            logger.warning(
                f"[Pagination out-of-bounds] page={page_number} | max={paginator.num_pages}"
            )
            page = paginator.page(1)

        return paginator, page, page.object_list, page.has_other_pages()


class ImageDownloadView(View):
    def get(self, request, pk):
        if not request.user.is_authenticated:
            return HttpResponseForbidden(
                "You must be logged in to download images."
            )

        image = get_object_or_404(Image, pk=pk)
        return FileResponse(
            image.image.open(),
            as_attachment=True,
            filename=image.image.name.split("/")[-1],
        )


class LastImageFragmentView(ListView):
    model = Image
    template_name = "images/components/last_image_fragment.html"
    context_object_name = "last_images"
    paginate_by = None

    def get_queryset(self):
        return Image.objects.order_by("-uploaded_at")[:3]
