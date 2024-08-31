from django.shortcuts import render, redirect
from .forms import CompressImageForm
from PIL import Image
import io
from django.contrib import messages
from django.http import HttpResponse


def compress(request):
    user = request.user
    if request.method == 'POST':
        form = CompressImageForm(request.POST, request.FILES)
        if form.is_valid():
            original_img = form.cleaned_data['original_img']
            quality = form.cleaned_data['quality']

            # temporarily saves the form
            compressed_image = form.save(commit=False)
            compressed_image.user = user

            # perform the  compression
            img = Image.open(original_img)

            # set the image format based on the uploaded image's format
            output_format = img.format

            buffer = io.BytesIO()
            img.save(buffer, format=output_format, quality=quality)
            buffer.seek(0)

            # save teh compressed image inside the model with filename format
            compressed_image.compressed_img.save(
                f'compressed_{original_img}', buffer
            )
            # return redirect('compress')
            # Automatically download the compressed file not as binary value but as formatted image
            response = HttpResponse(
                buffer.getvalue(), content_type=f'image/{output_format.lower()}')
            response['Content-Disposition'] = f'attachment;filename=compressed_{original_img}'
            return response

    else:
        form = CompressImageForm()
        context = {
            'form': form,
        }
        return render(request, 'image_compression/compress.html', context)
