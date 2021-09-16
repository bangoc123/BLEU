from utils import get_eff_ref_length, cal_brevity_penalty
from precision import cal_precision
import math

def cal_corpus_bleu_score(candidates, references_list, N, weights=None):
    assert N > 0, 'N must be greater than 0'

    if not weights:
        weights = [1 / N for _ in range(N)]

    candidates = [candidate.split() for candidate in candidates]

    for i, references in enumerate(references_list):
        for j, reference in enumerate(references):
            references_list[i][j] = reference.split()
    sum_candidate_lengths = 0
    sum_eff_ref_lengths = 0

    ps_numerators = [0 for _ in range(N)]
    ps_denominators = [0 for _ in range(N)]

    # Working on each candidate with its references
    for candidate, references in zip(candidates, references_list):

        # Candidate length
        candidate_length = len(candidate)

        # Loop over each weight

        for i, w in enumerate(weights):

            n_grams = i + 1

            # Calculate precision on each group
            numerator, denominator = cal_precision(
                candidate, references, n_grams)

            ps_numerators[i] += numerator
            ps_denominators[i] += denominator

        # Sum of all candidate lengths: c in paper
        sum_candidate_lengths += candidate_length

        # Calculate effective reference length
        eff_ref_length = get_eff_ref_length(candidate, references)

        # Sum of all effective reference lengths: r in paper
        sum_eff_ref_lengths += eff_ref_length

    # calculate BP
    bp = cal_brevity_penalty(eff_ref_length, sum_candidate_lengths)

    average_precisions = 0

    import sys
    sys.float_info.min
    for i, w in enumerate(weights):
        w = weights[i]
        ps_n = ps_numerators[i]
        ps_d = ps_denominators[i]

        # smoothing function: avoid 0
        if ps_n != 0 and ps_d != 0:
            average_precisions += w * math.log(ps_n / ps_d)
        else:
            print(
                'There are no common {} grams between candidates and references'.format(i + 1))
    bleu_score = bp * math.exp(average_precisions)

    return bleu_score

