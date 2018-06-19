from lang_model import LM
from data import DataIter
from argparse import ArgumentParser

parser = ArgumentParser('python train.py')
parser.add_argument('--model', '-m', type=str, default='model.pickle',
                    help='output file name')
parser.add_argument('--ngram', '-n', type=int, default=3,
                    help='')
parser.add_argument('--verbose', action='store_true', help='')

hps = parser.parse_args()

if __name__ == '__main__':
    n = 3
    di = DataIter(n)

    model = LM(hps.ngram)

    print('start training %d gram' % hps.ngram)
    model.fit(di, verbose=hps.verbose)

    print('vocab=%d' % len(model.vocab))

    print('saving the model to %s' % hps.model)
    model.save(hps.model)
