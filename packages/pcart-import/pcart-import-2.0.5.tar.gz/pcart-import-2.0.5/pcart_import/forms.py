from django import forms
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from .models import XLSImportProfile, YMLImportProfile


class XLSImportProfileForm(forms.ModelForm):
    model = XLSImportProfile

    class Meta:
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(XLSImportProfileForm, self).__init__(*args, **kwargs)
        self.fields['language'] = forms.ChoiceField(
            choices=settings.LANGUAGES,
            label=_('Language'),
        )


class YMLImportProfileForm(forms.ModelForm):
    model = YMLImportProfile

    class Meta:
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(YMLImportProfileForm, self).__init__(*args, **kwargs)
        self.fields['language'] = forms.ChoiceField(
            choices=settings.LANGUAGES,
            label=_('Language'),
        )
