from django.shortcuts import render
from .forms import QRCodeForm
import qrcode
import os
from django.conf import settings


def generate_qr_codes(request):
    if request.method == "POST":
        form = QRCodeForm(request.POST)
        if form.is_valid():
            res_name = form.cleaned_data['restaurant_name']
            url = form.cleaned_data['url']

            # Get size from form, default to 350
            size = int(request.POST.get('size', 350))
            size = max(150, min(size, 700))  # clamp to safe range

            # Generate QR Code at selected box_size
            qr = qrcode.QRCode(
                version=None,
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                box_size=max(4, size // 35),
                border=3,
            )
            qr.add_data(url)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            file_name = res_name.replace(" ", "_").lower() + '_menu.png'
            file_path = os.path.join(settings.MEDIA_ROOT, file_name)
            img.save(file_path)

            # Build URL with forward slashes (NOT os.path.join — breaks on Windows)
            qr_url = settings.MEDIA_URL + file_name

            context = {
                'res_name': res_name,
                'qr_url': qr_url,
                'file_name': file_name,
                'size': size,
            }
            return render(request, 'qr_result.html', context)

        # form invalid — re-render with errors
        return render(request, 'generate_qr_code.html', {'form': form})

    # GET
    form = QRCodeForm()
    return render(request, 'generate_qr_code.html', {'form': form})