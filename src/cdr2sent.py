from argparse import ArgumentParser
import sys
import io

parser = ArgumentParser('python cdr2sent.py')
parser.add_argument('--delimiter', '-d', type=str, default='\t', help='')
parser.add_argument('--concat', '-c', type=str, default=' ', help='')
parser.add_argument('--EOS', type=str, default='EOS', help='')
hps = parser.parse_args()


if __name__ == '__main__':
    input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')

    counter = 0
    read_count = 0
    sents = ''
    error_flag = False
    words = []

    while True:
        read_count += 1

        try:
            line = input_stream.readline()
        except UnicodeDecodeError:
            sys.stderr.write('line %s: UnicodeDecodeError\n' % (read_count))
            error_flag = True
            continue
        except EOFError:
            break
        if line is '':
            break

        # sents += line

        words.append(line[:line.find(hps.delimiter)])

        if words[-1] == hps.EOS:
            if not error_flag:
                print(hps.concat.join(words))
            sents = ''
            counter += 1 if not error_flag else 0
            error_flag = False
            words = []

            # if hps.lines != 0 and counter >= hps.lines + hps.skip:
            #     break
