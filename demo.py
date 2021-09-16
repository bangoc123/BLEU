# Bleu Score Demo

from bleu_score import cal_corpus_bleu_score

candidates = ['eating chicken chicken is a eating a eating chicken',
              'eating chicken chicken is not good']
references_list = [['a chicken is eating chicken', 'there is a chicken eating chicken'], [
    'a chicken is eating chicken', 'there is a chicken eating chicken']]

bleu_score = cal_corpus_bleu_score(candidates, references_list,
                      weights=(0.25, 0.25, 0.25, 0.25), N=4)

print('Bleu Score: {}'.format(bleu_score))


