from django import forms
from django.core.exceptions import ValidationError

from .models import Product


BANNED_WORDS = {
    'казино',
    'криптовалюта',
    'крипта',
    'биржа',
    'дешево',
    'бесплатно',
    'обман',
    'полиция',
    'радар',
}


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name',
            'description',
            'image',
            'category',
            'price',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply consistent styling
        for field_name, field in self.fields.items():
            if isinstance(field.widget, (forms.widgets.Select, forms.widgets.SelectMultiple)):
                field.widget.attrs.setdefault('class', 'form-select')
            elif not isinstance(field.widget, (forms.widgets.CheckboxInput, forms.widgets.ClearableFileInput)):
                field.widget.attrs.setdefault('class', 'form-control')
        # File input styling to match platform look
        if 'image' in self.fields:
            self.fields['image'].widget.attrs.setdefault('class', 'form-control')

    def _validate_no_banned_words(self, value: str, field_label: str) -> str:
        if not value:
            return value
        lowered = value.lower()
        if any(bad in lowered for bad in BANNED_WORDS):
            raise ValidationError(
                f"Поле '{field_label}' содержит запрещённые слова.",
                code='banned_words',
            )
        return value

    def clean_name(self) -> str:
        name = self.cleaned_data.get('name', '')
        return self._validate_no_banned_words(name, 'Наименование')

    def clean_description(self) -> str:
        description = self.cleaned_data.get('description', '')
        return self._validate_no_banned_words(description, 'Описание')

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is None:
            return price
        if price < 0:
            raise ValidationError('Цена не может быть отрицательной.', code='negative_price')
        return price


