from data import DataIter
import math
# import pygtrie as trie
import pickle
from collections import defaultdict
# import time


def load_model(file):
    return pickle.load(open(file, 'rb'))


class LM(object):
    def __init__(self, n):
        self.n = n
        # self.ngram = trie.StringTrie()
        self.ngram = defaultdict(int)
        self.vocab = set()

    def fit(self, data_iter, verbose=False):
        # t = time.time()
        # summary = defaultdict(float)
        for i, word_set in enumerate(data_iter):
            # t2 = time.time(); summary['load words'] += t2 - t; t = t2
            if verbose and i % 100000 == 0:
                print('sample: %d' % i)

            self.vocab.add(word_set[-1])
            # t2 = time.time(); summary['update vocab'] += t2 - t; t = t2

            ctxs = self.split_ctx(word_set)
            # t2 = time.time(); summary['make ngram'] += t2 - t; t = t2
            for ctx in ctxs:
                # if ctx not in self.ngram:
                #     self.ngram[ctx] = 0

                self.ngram[ctx] += 1
            # t2 = time.time(); summary['add'] += t2 - t; t = t2

        # for a, v in summary.items():
        #     print('%s: %f ms' % (a, v * 1000))

    def split_ctx(self, word_set):
        ctxs = ['/'.join(word_set[:i]) for i in range(1, len(word_set) + 1)]
        return ctxs

    def log_p(self, word_set):
        ctxs = self.split_ctx(word_set)
        ctx, tgt = ctxs[-2:]

        if tgt in self.ngram:
            return math.log2(self.ngram[tgt] / self.ngram[ctx])
        else:
            return -float('inf')

    def entropy(self, data_iter, display=False):
        p = num = 0
        for word_set in data_iter:
            if len(word_set) == self.n:
                num += 1
                p += self.log_p(word_set)

        return - (p / num)

    def perplexity(self, data_iter):
        p = self.entropy(data_iter)
        return math.pow(2, p)

    def save(self, out_file):
        with open(out_file, 'wb') as f:
            pickle.dump(self, f, protocol=pickle.HIGHEST_PROTOCOL)

    def copy_from(self, lm):
        self.ngram = lm.ngram
        self.vocab = lm.vocab
        self.n = lm.n
        return self


class AddkLM(LM):
    def __init__(self, n, addk=1):
        super(AddkLM, self).__init__(n)
        self.k = addk

    def log_p(self, word_set):
        ctxs = self.split_ctx(word_set)
        ctx, tgt = ctxs[-2:]

        wn = self.ngram[tgt] if tgt in self.ngram else 0
        wn_1 = self.ngram[ctx] if ctx in self.ngram else 0
        V = len(self.vocab) + 1

        return math.log2((wn + self.k) / (wn_1 + self.k * V))


if __name__ == '__main__':
    import io

    n = 3
    di = DataIter(n)

    model = LM(n)
    model.fit(di, verbose=True)

    model.save('model.pickle')

    model2 = AddkLM(n, 1)
    model2.copy_from(load_model('model.pickle'))

    s = 'よる ー EOS\nよる ー EOS\n'
    stream = io.StringIO(s)
    test_di = DataIter(n, stream)

    ent = model2.entropy(test_di, display=True)
    print('ent: %s' % ent)
