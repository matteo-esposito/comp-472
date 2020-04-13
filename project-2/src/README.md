https://github.com/matteo-esposito/comp-472

# COMP472 - Project 2

## Setup

First, clone the repo and cd into the src folder.

```bash
git clone https://github.com/matteo-esposito/comp-472.git
cd comp-472/project-2/src/
```
## Classification

**Note:** If you want to provide your own test/train cases, modify the .txt file path in the `test_file` or `train_file` variable of the parametrized NBClassifier constructor in `main.py`.

### 1. Standard Model

Modify the `V,n,delta` values depending on what configuration is desired. Then run the following snippet, 

```bash
python main.py
```

### 2. BYOM
First adjust the weights based on which models you choose to give preference.

- w1 will be the weight used to adjust the trigram
- w2 will be used to adjust the bigram
- w3 = 1 - (w1 + w2) will be used to adjust the unigram. 

All weights must respect the following inequality: 

`w1 + w2 + w3 < 1.`

Then select a preferred vocabulary set between 0 and 2 and delta less than 1.Finally run the BYOM the same way as the other models (see above).