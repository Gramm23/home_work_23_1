from django import forms
from django.forms import CheckboxInput, ValidationError

from product.models import *

FORBIDDEN_WORDS = [
    "казино",
    "криптовалюта",
    "крипта",
    "биржа",
    "дешево",
    "бесплатно",
    "обман",
    "полиция",
    "радар",
]


def validate_no_forbidden_words(value):
    for word in FORBIDDEN_WORDS:
        if word.lower() in value.lower():
            raise ValidationError(f"Слово '{word}' не допускается.")


class ContactForm(forms.Form):
    first_name = forms.CharField(label="Имя", max_length=20)
    email = forms.EmailField(label="Email")
    question = forms.CharField(
        label="Введите Ваш вопрос",
        max_length=200,
        help_text="не более 200 символов",
        widget=forms.Textarea(attrs={"style": "height: 65px;"}),
    )


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["title", "description", "image", "price", "active", "category"]
        widgets = {"active": CheckboxInput()}
        labels = {
            "title": "Название",
            "description": "Описание",
            "image": "Изображение",
            "price": "Стоимость",
            "active": "Активная",
            "category": "Категория",
        }

        title = forms.CharField(
            label="Название", max_length=50, validators=[validate_no_forbidden_words]
        )
        description = forms.CharField(
            label="Описание",
            max_length=600,
            help_text="не более 600 символов",
            validators=[validate_no_forbidden_words],
        )


class VersionForm(forms.ModelForm):
    class Meta:
        model = Version
        fields = "__all__"

    def clean(self):
        cleaned_data = super().clean()
        counter = 0

        try:

            existing_instance = self.instance.product.versions.filter(active=True)
            for active_version in existing_instance:
                print(active_version)
                if active_version:
                    if self.instance.pk is not None:
                        self.instance.active = cleaned_data.get('active', False)
                        counter += 1

            if counter > 1:
                raise forms.ValidationError('Активная версия должна быть только одна')


        except Version.DoesNotExist:
            pass

        return cleaned_data

    def save(self, commit=True):
        instance = super().save(commit=commit)
        if commit and instance.active:
            existing_active_versions = instance.product.versions.filter(active=True).exclude(pk=instance.pk)
            for active_version in existing_active_versions:
                active_version.active = False
                active_version.save()
        return instance
