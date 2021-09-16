from collections import Counter, defaultdict
import math

def ngrams(sequence, n_grams):
    assert len(sequence) > 0, 'Sequence Length is not empty'
    assert len(
        sequence) >= n_grams, 'Sequence Length shoule be greater than n_grams'

    grams = Counter()

    sequence_length = len(sequence)

    for i in range(sequence_length - n_grams + 1):
        gram = tuple(sequence[i:(i+n_grams)])
        grams[gram] += 1

    return grams


def get_max_ref_count(references, n_grams):

    # Loop over references
    max_ref_count = defaultdict(int)

    for reference in references:
        single_reference_grams = Counter(ngrams(reference, n_grams))

        # Count the max number of a gram in any single reference
        for gram in single_reference_grams:

            # Update the max value of the number of this gram is any single reference
            max_ref_count[gram] = max(
                max_ref_count[gram], single_reference_grams[gram])

    return max_ref_count


def get_eff_ref_length(candidate, references):
    candidate_len = len(candidate)
    reference_lens = [len(reference) for reference in references]
    min_different_length = float('inf')

    effective_length = candidate_len

    for refer_len in reference_lens:
        if abs(refer_len - candidate_len) <= min_different_length:
            min_different_length = abs(refer_len - candidate_len)
            effective_length = refer_len

    return effective_length


def cal_brevity_penalty(r, c):
  if c == 0:
    return 0
  
  if c > r:
    return 1

  return math.exp(1 - r/c)

  