from flask import Flask, render_template, request, redirect, url_for
from fm_index import FMIndex
from util import save_pickle, load_pickle, load_files, get_file_name_via_index
import time
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    fmi = FMIndex()
    if request.method == 'GET':
        # message = 'hi'
        pat = request.args.get('keyword')
        # request.form['keyword'])
        # return render_template('index.html', message=message)

        if pat:
            # pat = request.form['keyword']
            # pat = '日本の'
            match = fmi.search(pat)
            print('Results of search("{}")'.format(pat))
            print('match', match)
            rng = 15
            results = []
            for i, m in enumerate(match):
                beg = m[0]
                end = m[1]
                # print('(beg, end) = ({}, {})'.format(beg, end))
                f_name = get_file_name_via_index(db, beg)
                print('{} [{}]: ({}, {})'.format(i, f_name, beg, end))
                # print('---{}"{}"{}---'.format(dec[beg-rng: beg], dec[beg:end], dec[end:end+rng]))
                print('---{}"{}"{}---'.format(T[beg-rng: beg], T[beg:end], T[end:end+rng]))
                v = '{}<span class="match">{}</span>{}'.format(T[beg-rng: beg], T[beg:end], T[end:end+rng])
                results.append((f_name, v))
                # print(decoded[m[0]:])
            return render_template('index.html', results=results)
        else:
            return render_template('index.html')
    else:
        print('request received\n')

        substring = request.files['substring'].read().decode()
        T = request.files['file'].read().decode()
        fmi = FMIndex()
        
        save_idx = 'data/idx_test'
        datafile = 'test_data'

        print('encode text...')
        bw, sa = fmi.encode(T)
        ranks, ch_count = fmi.rank_bwt(bw)
        save_pickle({'bwt': bw, 'sa': sa, 'text_len': len(T), 'ch_count': ch_count}, 'index.dict')
        fmi.ch_count = ch_count
        print('encode done!')

        start = time.time()
        match = fmi.search(substring)
        stop = time.time()
        print(stop-start)
        # print('Results of search("{}")'.format(substring))
        # print('match', match)
        return {'match' : match}
        # data.save(os.path.join('data/', datafile))
        # data = file.read()
        # print('starting building Index')
        # start = time.time()
        # idx = fmindex.index(data)
        # stop = time.time()
        # print('FM-Index built in:', stop-start, 'seconds')
        # fmindex.save(save_idx, idx)
        # print('FM-Index saved!')
        # print()
        # print('Fuzzy DNA matching in progress. . .')
        
        # d = {}
        # start = time.time()
        # for i in range(len(substring), int(len(substring)*0.65), -1):
        #     s = substring[:i]
        #     score = int((len(s)/len(substring)) * 100)
        #     ans = idx.search(s)
        #     d[score] = (s,ans)
        # stop = time.time()
        # print()
        # print('Fuzzy Matching done in', stop-start, 'seconds')
        # print()
        # print(d)
        # return d

if __name__ == '__main__':
    app.debug = True
    app.run()