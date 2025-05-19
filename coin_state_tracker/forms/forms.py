from django import forms

class CoinFlipForm(forms.Form):
    thumb = forms.BooleanField(
        required=False,
        label="Krark's Thumb"
    )
    krark_count = forms.IntegerField(
        label="Number of Krarks",
        min_value=1,
        initial=1,
        help_text="How many Krarks do you have on the battlefield (including copies)"
    )
    storm_kiln_artist = forms.IntegerField(
        label="Storm-Kiln Artist count",
        min_value=0,
        initial=0,
        help_text="Number of Storm-Kiln Artists that create additional triggers"
    )
    trigger_adds = forms.IntegerField(
        label="Count of Permanent Trigger Adds",
        min_value=0,
        initial=0,
        help_text="Tracking Permanents that Add Triggers to Krark"
    )
    twinning_staff = forms.IntegerField(
        label="Twinning Staff count",
        min_value=0,
        initial=0,
        help_text="Each Twinning Staff doubles your copy effects"
    )
    num_simulations = forms.IntegerField(
        label="Number of simulations",
        min_value=1,
        max_value=10000,
        initial=1,
        help_text="Run multiple simulations to get statistical data"
    )