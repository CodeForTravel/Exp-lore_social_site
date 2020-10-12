from django import forms
from . import models

class ImageForm(forms.Form):
    image = forms.ImageField(label='Image', required=False, )
    caption = forms.CharField(
        label='Caption',
        max_length=400,
        required=False,
        widget=forms.Textarea(attrs={'placeholder': 'Write about your picture!'})
    )


    def clean(self):
        caption = self.cleaned_data.get('caption')
        image = self.cleaned_data.get('image')

        if len(caption) < 1 :
            raise forms.ValidationError('Write about your image ')
        else:
            if not image:
                raise forms.ValidationError('You must upload a image!')
    def deploy(self):
        caption = self.cleaned_data.get('caption')
        image = self.cleaned_data.get('image')

        img = models.ImagePost(
            caption = caption,
            image = image
        )
        img.save()

