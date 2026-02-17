from django import forms

from .models import ChoreTask


class MultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class ChoreTaskForm(forms.ModelForm):
    class Meta:
        model = ChoreTask
        fields = ['title', 'description', 'assigned_to', 'due_date']
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
        }


class TaskPhotoUploadForm(forms.Form):
    photos = forms.FileField(
        required=False,
        widget=MultiFileInput(
            attrs={
                'accept': 'image/*',
                'capture': 'environment',
            }
        ),
    )

    def clean_photos(self):
        files = self.files.getlist('photos')
        if not files:
            raise forms.ValidationError('Please select at least one image.')
        if len(files) > 3:
            raise forms.ValidationError('You can upload up to 3 photos at once.')
        return files
