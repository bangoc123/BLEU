
# BLEU Score

Implementation for paper: 

[BLEU](https://aclanthology.org/P02-1040.pdf): a Method for Automatic Evaluation of Machine Translation

Author: Ba Ngoc from [ProtonX](https://protonx.ai/)

BLEU score is a popular metric to evaluate machine translation. Check out the recent [Transformer](https://github.com/bangoc123/transformer) project we published.

I. Usage

```python
from bleu_score import cal_corpus_bleu_score

candidates = ['eating chicken chicken is a eating a eating chicken',
              'eating chicken chicken is not good']
references_list = [['a chicken is eating chicken', 'there is a chicken eating chicken'], [
    'a chicken is eating chicken', 'there is a chicken eating chicken']]

bleu_score = cal_corpus_bleu_score(candidates, references_list,
                      weights=(0.25, 0.25, 0.25, 0.25), N=4)

print('Bleu Score: {}'.format(bleu_score))
```

II. BLEU Score Formula

### 1. Precision
$$
    p_n = \frac{\sum_{C \ \in \ \left \{ Candidates \right \}} \sum_{n-gram \ \in \ C} Count_{clip}(n-gram) }{\sum_{C' \ \in \ \left \{ Candidates \right \}} \sum_{n-gram' \ \in \ C'} Count(n-gram')} 
$$

We count specific n-grams in the candidates and the number of those grams in the references. Then we calculate the proportion of two countings and get the precision.

**Important to note:** Count clip means that the number of typical n-grams can not exceed the maximum number of that n-grams in **any single** reference.

For example: if `('a', 'a')` gram exists **3 times** in a candidate. However, the maximum number of this gram in any single reference is **2**. So we will use value 2 for calculation.

If you never heard about grams? It means that we count the number of continuous substrings with a pre-set length in a string.

Candidate 1: `'eating chicken chicken is a eating a eating chicken'`

-------Unigram------

|   |   |
|---|---|
eating | 3
chicken | 3
is | 1
a | 2

-------bigrams------

|   |   |
|---|---|
eating chicken | 2
chicken chicken | 1
chicken is | 1
is a | 1
a eating | 2
eating a | 1

We can do the same thing with trigrams and 4-grams

### 2. Sentence brevity penalty

We prefer the reference with a length that is closest to the candidate's.

Checkout function `get_eff_ref_length` in utils.py.

$c$: the total lengths of all candidates

$r$: the total lengths of all effective reference lengths

$$

\text{BP} = \left\{\begin{matrix} 1 \ \ \ \text{if}  \ \ \ c > r
\\ e^{1-\frac{r}{c}}

\end{matrix}\right.

$$


### 3. Sentence brevity penalty


$$
\text{BLEU} = \text{BP} * \text{exp} \begin{Bmatrix}
\sum_{n=1}^{N}w_n\log{p_n}
\end{Bmatrix}

$$

$N$: the number of grams


$w$: list of pre-set weight for each gram
