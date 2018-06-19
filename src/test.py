from lang_model import load_model, LM, AddkLM
from data import DataIter
from argparse import ArgumentParser
import math
import sys

parser = ArgumentParser('python train.py')
parser.add_argument('--model', '-m', type=str, default='model.pickle', help='')
parser.add_argument(
    '--smoothing', '-s', type=str, default='none', help='none, {num}(=add_k)')

hps = parser.parse_args()

if __name__ == '__main__':
    m = load_model(hps.model)
    smoothing = hps.smoothing.lower()
    # ここ調整
    if smoothing == 'none':
        model = LM(m.n)
        # model.tri = m.tri
    elif smoothing.isdigit():
        model = AddkLM(m.n, int(smoothing))
        # model.tri = m.tri
    # model.vocab = m.vocab
    model.copy_from(m)

    sys.stderr.write('n=%d, k=%d, vocab=%d\n' % (model.n, model.k
                                                 if smoothing.isdigit() else 0,
                                                 len(model.vocab)))

    di = DataIter(model.n)

    ent = model.entropy(di)
    perp = math.pow(2, ent)
    sys.stderr.write('entropy=%.5f, perplexity=%.5f\n' % (ent, perp))
