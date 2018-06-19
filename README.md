# N-gram language model
Master SLP meeting task

## Train

```
$ cat data/train.cdr | ./src/cdr2sent.py| python ./src/train.py -m trigram.model -n 3
start training 3 gram
saving the model to trigram.model
elapsed (real): 638.418s; RSS=12700.3M
```

## Test

Add-1 smoothing

```
$ cat data/test.cdr | python src/cdr2sent.py| python ./src/test.py -m trigram.model -s 1
n=3, k=1, vocab=652835
entropy=14.30238, perplexity=20204.37974
elapsed (real): 168.577s; RSS=19042.0M
```
