from .models import BannerSlider


def sliders(request):
    sliders = BannerSlider.objects.filter(is_active=True).order_by("position")
    return dict(sliders=sliders)