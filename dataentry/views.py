from django.conf import settings
from django.contrib import messages
from django.http.request import HttpRequest
from django.shortcuts import redirect, render

from uploads.models import Upload

from .task import export_data_task, import_data_task
from .utils import check_csv_errors, get_models_to_context


def import_data(request: HttpRequest):
    if request.method == "POST":
        file_path = request.FILES.get("file_path")
        model_name = request.POST.get("model_name")

        upload = Upload.objects.create(file=file_path, model_name=model_name)

        relative_path = str(upload.file.url)
        base_url = str(settings.BASE_DIR)
        absolute_path = base_url + relative_path

        try:
            check_csv_errors(absolute_path, model_name)
        except Exception as e:
            messages.error(request, str(e))
            return redirect("import_data")

        import_data_task.delay(absolute_path, model_name)

        messages.success(
            request,
            "Your data is being processed, you will be notified once it is done!",
        )
        return redirect("import_data")
    else:
        context = get_models_to_context()
    return render(request, "dataentry/importdata.html", context)


def export_data(request: HttpRequest) -> render:
    if request.method == "POST":
        model_name = request.POST.get("model_name")

        export_data_task.delay(model_name)
        messages.success(
            request,
            "Your data is being exported, you will be notified once it is done!",
        )
        return redirect("export_data")

    else:
        context = get_models_to_context()
    return render(request, "dataentry/exportdata.html", context)
