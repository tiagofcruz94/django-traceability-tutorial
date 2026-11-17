from django import forms

from .models import Carcass


class CarcassForm(forms.ModelForm):
    """Register a carcass. Validation comes from the model (unique fields, yield range)."""

    class Meta:
        model = Carcass
        fields = ["animal", "slaughter_number", "slaughtered_at", "hot_weight", "lot"]
        # Portuguese users type decimals with a comma, not a dot.
        localized_fields = ["hot_weight"]
