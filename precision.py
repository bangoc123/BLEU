from utils import ngrams, get_max_ref_count
from collections import Counter, defaultdict

def cal_precision(candidate, references, n_grams=2):

    # Get candidate grams
    candidates_grams = defaultdict(int)

    max_ref_count = get_max_ref_count(references, n_grams)

    # Find the number of count clip grams
    count_clip_grams = 0

    total_grams_in_candidates = 0

    # Loop over candidates

    candidate_grams = Counter(ngrams(candidate, n_grams))

    for gram in candidate_grams:
        
		# Count gram in candidates
        candidates_grams[gram] += candidate_grams[gram]

        # Get minimum value between gram in this candidate and the max number of it in any single reference
        count_clip_grams += min(max_ref_count[gram], candidates_grams[gram])

        total_grams_in_candidates += candidates_grams[gram]

    # Using small epsilon for avoiding denominator is 0

    return [count_clip_grams, total_grams_in_candidates]
