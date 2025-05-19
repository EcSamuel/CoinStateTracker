from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from coin_state_tracker.forms.forms import CoinFlipForm
from coin_state_tracker.krark_engine import KrarkEngine


class CoinFlipView(View):
    def get(self, request):
        form = CoinFlipForm()
        return render(request, 'flip_template.html', {'form': form})

    def post(self, request):
        form = CoinFlipForm(request.POST)
        if form.is_valid():
            # Extract all form data
            thumb = form.cleaned_data['thumb']
            krark_count = form.cleaned_data['krark_count']
            storm_kiln_artist = form.cleaned_data['storm_kiln_artist']
            trigger_adds = form.cleaned_data['trigger_adds']
            twinning_staff = form.cleaned_data['twinning_staff']
            num_simulations = form.cleaned_data['num_simulations']

            # Create the engine with all parameters
            engine = KrarkEngine(
                thumb=thumb,
                krark_count=krark_count,
                storm_kiln_artist=storm_kiln_artist,
                trigger_adds=trigger_adds,
                twinning_staff=twinning_staff
            )

            # Run simulations
            simulation_results = engine.simulate(num_simulations=num_simulations)

            # Calculate probabilities
            probabilities = engine.calculate_probabilities()

            # Calculate the actual total triggers for display
            total_triggers = engine._calculate_total_triggers()

            return render(request, 'flip_template.html', {
                'form': form,
                'simulation_results': simulation_results,
                'probabilities': probabilities,
                'total_triggers': total_triggers
            })
        return render(request, 'flip_template.html', {'form': form})