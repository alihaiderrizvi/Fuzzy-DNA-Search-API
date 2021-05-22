from flask import Flask, render_template, request, redirect, url_for
from fm_index import FMIndex
from util import save_pickle, load_pickle, load_files, get_file_name_via_index
import time

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return 'Fuzzy DNA Search API'

@app.route('/search', methods=['GET', 'POST'])
def index():
    fmi = FMIndex()
    if request.method == 'GET':
        return 'send post request'
    else:
        print('request received\n')

        substring = request.files['substring'].read().decode()
        T = request.files['file'].read().decode()
        filename = request.files['file'].filename
        
        print(filename)

        fmi = FMIndex()

        if '.dict' in filename:
            saved_data = load_pickle(filename)
            bw = saved_data['bwt']
            fmi.set_dict(saved_data)        
        
        else:
            print('encode text...')

            start = time.time()
            bw, sa = fmi.encode(T)
            # print(sa)
            stop = time.time()
            
            print('suffix array time:', stop-start)
            
            start = time.time()
            ranks, ch_count = fmi.rank_bwt(bw)
            print(ch_count)
            stop = time.time()
            
            print('ranking time:', stop-start)
            
            save_pickle({'bwt': bw, 'sa': sa, 'text_len': len(T), 'ch_count': ch_count}, 'index.dict')
            fmi.ch_count = ch_count
            
            print('encode done!')

        start = time.time()

        results = {}
        for i in range(len(substring), int(len(substring)*0.79), -1):
            s = substring[:i]
            perc = int((len(s) / len(substring)) * 100)
            match = fmi.search(s)
            results[perc] = match
        
        stop = time.time()

        print('searching time:', stop-start)
        return results

if __name__ == '__main__':
    app.debug = True
    app.run()