from django.conf import settings
from django.contrib import messages
from django.core.management import call_command
from django.http.request import HttpRequest
from django.shortcuts import redirect, render

from uploads.models import Upload

from .utils import get_all_custom_models


def import_data(request: HttpRequest):
    if request.method == "POST":
        file_path = request.FILES.get("file_path")
        model_name = request.POST.get("model_name")

        upload = Upload.objects.create(file=file_path, model_name=model_name)

        relative_path = str(upload.file.url)
        base_url = str(settings.BASE_DIR)
        absolute_path = base_url + relative_path

        try:
            call_command("importdata", absolute_path, model_name)
            messages.success(request, "Data imported successfully!")
        except Exception as e:
            messages.error(request, str(e))
        return redirect("import_data")
    else:
        models = get_all_custom_models()
        context = {"models": models}
    return render(request, "dataentry/importdata.html", context)
