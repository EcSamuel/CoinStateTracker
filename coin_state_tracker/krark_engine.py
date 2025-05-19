import random
from math import comb

class KrarkEngine:
    def __init__(self, thumb=False, krark_count=1, storm_kiln_artist=0, trigger_adds=0, twinning_staff=0):
        self.thumb = thumb
        self.krark_count = krark_count
        self.storm_kiln_artist = storm_kiln_artist  # Adds additional triggers
        self.trigger_adds = trigger_adds  # Doubles triggers from Krark
        self.twinning_staff = twinning_staff  # Doubles copy effects from winning flips

        # Calculate total triggers
        self.total_triggers = self._calculate_total_triggers()

    def _calculate_total_triggers(self):
        """Calculate the total number of triggers based on board state"""
        # Base triggers from Krark clones
        base_triggers = self.krark_count

        # Harmonic Prodigy doubles triggers from each Krark
        if self.trigger_adds > 0:
            base_triggers *= (2 ** self.trigger_adds)

        # Storm-Kiln Artist adds additional triggers
        base_triggers += self.storm_kiln_artist

        return base_triggers

    def simulate(self, num_simulations=1):
        """Simulate the coin flips and return detailed results"""
        all_results = []

        for _ in range(num_simulations):
            # List to store individual flip results
            flip_results = []
            heads_count = 0
            tails_count = 0

            # For each trigger
            for _ in range(self.total_triggers):
                if self.thumb:
                    # Krark's Thumb: flip twice and choose the better result
                    flip1 = random.choice(["heads", "tails"])
                    flip2 = random.choice(["heads", "tails"])
                    result = max(flip1, flip2)  # "heads" > "tails" in lexicographic order
                    flips = [flip1, flip2]
                else:
                    # Regular flip
                    result = random.choice(["heads", "tails"])
                    flips = [result]

                # Count the result
                if result == "heads":
                    heads_count += 1
                else:
                    tails_count += 1

                flip_results.append({
                    "result": result,
                    "flips": flips
                })

            # Calculate copies based on heads and Twinning Staff
            copy_count = heads_count * (2 ** self.twinning_staff)

            all_results.append({
                "flip_results": flip_results,
                "heads_count": heads_count,
                "tails_count": tails_count,
                "copy_count": copy_count,
                "all_tails": heads_count == 0,
                "all_heads": tails_count == 0
            })

        return all_results

    def calculate_probabilities(self):
        """Calculate various probabilities for the current board state"""
        probabilities = {}

        # Calculate probability of getting all tails (bust)
        probabilities["bust_probability"] = self._calculate_bust_probability()

        # Calculate probability distribution of heads
        probabilities["heads_distribution"] = self._calculate_heads_distribution()

        # Calculate expected number of copies
        probabilities["expected_copies"] = self._calculate_expected_copies()

        return probabilities

    def _calculate_bust_probability(self):
        """Calculate the probability of all flips resulting in tails"""
        per_flip_tail_prob = 0.5  # Base probability of tails on a single flip

        if self.thumb:
            # With Krark's Thumb, we need to get tails on both flips
            per_flip_tail_prob = 0.25  # 0.5 * 0.5

        # Probability of all tails is the probability of tails raised to the power of total triggers
        return per_flip_tail_prob ** self.total_triggers

    def _calculate_heads_distribution(self):
        """Calculate the probability distribution of getting X heads"""
        distribution = {}

        # Individual flip probabilities
        p_heads = 0.75 if self.thumb else 0.5  # Probability of heads with/without Thumb
        p_tails = 1 - p_heads

        # For each possible number of heads
        for h in range(self.total_triggers + 1):
            # Binomial probability: C(n,k) * p^k * (1-p)^(n-k)
            prob = comb(self.total_triggers, h) * (p_heads ** h) * (p_tails ** (self.total_triggers - h))
            distribution[h] = prob

        return distribution

    def _calculate_expected_copies(self):
        """Calculate the expected number of copies from winning flips"""
        # Expected number of heads
        p_heads = 0.75 if self.thumb else 0.5
        expected_heads = self.total_triggers * p_heads

        # Account for Twinning Staff multiplier
        multiplier = 2 ** self.twinning_staff

        return expected_heads * multiplier