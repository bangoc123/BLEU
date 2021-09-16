
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
<!-- $$
    p_n = \frac{\sum_{C \ \in \ \left \{ Candidates \right \}} \sum_{n-gram \ \in \ C} Count_{clip}(n-gram) }{\sum_{C' \ \in \ \left \{ Candidates \right \}} \sum_{n-gram' \ \in \ C'} Count(n-gram')} 
$$ -->


<img src='https://latex.codecogs.com/gif.latex?%5Chuge%20p_n%20%3D%20%5Cfrac%7B%5Csum_%7BC%20%5C%20%5Cin%20%5C%20%5C%7B%20Candidates%20%5C%7D%7D%20%5Csum_%7Bn-gram%20%5C%20%5Cin%20%5C%20C%7D%20Count_%7Bclip%7D%28n-gram%29%20%7D%7B%5Csum_%7BC%27%20%5C%20%5Cin%20%5C%20%5C%7B%20Candidates%20%5C%7D%7D%20%5Csum_%7Bn-gram%27%20%5C%20%5Cin%20%5C%20C%27%7D%20Count%28n-gram%27%29%7D' width=500 >



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

`c`: the total lengths of all candidates

`r`: the total lengths of all effective reference lengths

<!-- $$

\text{BP} = \left\{\begin{matrix} 1 \ \ \ \text{if}  \ \ \ c > r
\\ e^{1-\frac{r}{c}}

\end{matrix}\right.

$$ -->

<img src='https://latex.codecogs.com/gif.latex?%5Chuge%20%5Ctext%7BBP%7D%20%3D%20%5Cleft%5C%7B%5Cbegin%7Bmatrix%7D%201%20%5C%20%5C%20%5C%20%5Ctext%7Bif%7D%20%5C%20%5C%20%5C%20c%20%3E%20r%20%5C%5C%20e%5E%7B1-%5Cfrac%7Br%7D%7Bc%7D%7D%20%5C%20%5C%20%5C%20%5Ctext%7Bif%7D%5C%20%5C%20%5C%20c%20%5Cleq%20r%20%5Cend%7Bmatrix%7D%5Cright.' width=200 />


### 3. BLEU Formula


<!-- $$
\text{BLEU} = \text{BP} * \text{exp} \begin{Bmatrix}
\sum_{n=1}^{N}w_n\log{p_n}
\end{Bmatrix}

$$ -->


<img src='https://latex.codecogs.com/gif.latex?%5Chuge%20%5Ctext%7BBLEU%7D%20%3D%20%5Ctext%7BBP%7D%20%5Ctimes%20%5Ctext%7Bexp%7D%20%5Cbegin%7BBmatrix%7D%20%5Csum_%7Bn%3D1%7D%5E%7BN%7Dw_n%5Clog%7Bp_n%7D%20%5Cend%7BBmatrix%7D' width=500>

`N`: the number of grams

`w`: list of pre-set weight for each gram
