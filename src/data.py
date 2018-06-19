import sys
import io
import queue

UNK_WORD = '<unk>'
START_WORD = '<s>'
END_WORD = 'EOS'


class DataIter(object):
    def __init__(self, n, inp=sys.stdin):
        self.input = inp
        self.n = n
        self.q = queue.Queue()

    def __iter__(self):
        return self

    def __next__(self):
        if self.q.empty():
            self.fill_que()

        return self.q.get()

    def fill_que(self):
        line = self.input.readline()
        if line == '':
            raise StopIteration
        words = [START_WORD] * (self.n - 1) + line.strip().split(' ')

        for i in range(len(words) - self.n + 1):
            self.q.put(words[i:i + self.n])


if __name__ == '__main__':
    input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
    di = DataIter(4, inp=input_stream)

    for i, item in enumerate(di):
        print(i, item)
