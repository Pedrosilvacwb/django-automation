import io

from django.contrib.auth.models import AbstractBaseUser, AnonymousUser
from django.forms import ModelForm
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from PIL import Image
from PIL.ImageFile import ImageFile

from .forms import CompressImageForm
from .models import CompressImage

# Create your views here.


def compress(request: HttpRequest):
    user: AbstractBaseUser | AnonymousUser = request.user
    if request.method == "POST":
        form: ModelForm = CompressImageForm(request.POST, request.FILES)

        if form.is_valid():
            original_img: str = form.cleaned_data["original_img"]
            quality: str = form.cleaned_data["quality"]

            compressed_image: CompressImage = form.save(commit=False)
            compressed_image.user = user
            img: ImageFile = Image.open(original_img)
            output_format = img.format

            buffer: io.BytesIO = io.BytesIO()

            img.save(buffer, format=output_format, quality=quality)
            buffer.seek(0)

            compressed_image.compressed_image.save(f"compressed_{original_img}", buffer)

            response: HttpResponse = HttpResponse(
                buffer.getvalue(), content_type=f"image/{output_format.lower()}"
            )
            response["Content-Disposition"] = (
                f"attachment; filename=compressed_{original_img}"
            )
            return response

    else:
        form: ModelForm = CompressImageForm()
        context: dict = {"form": form}
    return render(request, "image_compression/compress.html", context)
