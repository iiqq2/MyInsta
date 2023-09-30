from api.models import Photo
from django import forms


class ImageForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('title', 'image', 'user')
