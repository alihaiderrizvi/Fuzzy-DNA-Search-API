from flask import Flask, render_template, request, redirect, url_for
from fm_index import FMIndex
from util import save_pickle, load_pickle, load_files, get_file_name_via_index
import time

app = Flask(__name__)

def fuzzy_search(substring, fmi):
    results = {}
        
    #fuzzy search
    for i in range(len(substring), int(len(substring)*0.79), -1):
        s = substring[:i]
        perc = int((len(s) / len(substring)) * 100)
        match = fmi.search(s)
        results[perc] = match
    
    return results


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

        # read substring and dna file from request
        substring = request.files['substring'].read().decode()
        T = request.files['file'].read().decode()
        filename = request.files['file'].filename
        
        print(filename)

        fmi = FMIndex()
        
        #check if DNA index is received
        if '.dict' in filename:
            saved_data = load_pickle(filename)
            bw = saved_data['bwt']
            fmi.set_dict(saved_data)
        
        else:
            print('encode text...')

            #build burrow's wheeler and suffix array
            start = time.time()
            bw, sa = fmi.encode(T)
            stop = time.time()
            
            print('suffix array time:', stop-start)
            
            # find character count and ranks
            start = time.time()
            ranks, ch_count = fmi.rank_bwt(bw)
            stop = time.time()
            
            print('ranking time:', stop-start)
            
            #save index
            save_pickle({'bwt': bw, 'sa': sa, 'text_len': len(T), 'ch_count': ch_count}, 'index.dict')
            fmi.ch_count = ch_count
            
            print('encode done!')

        start = time.time()

        results = fuzzy_search(substring, fmi)
        
        # #fuzzy search
        # for i in range(len(substring), int(len(substring)*0.79), -1):
        #     s = substring[:i]
        #     perc = int((len(s) / len(substring)) * 100)
        #     match = fmi.search(s)
        #     results[perc] = match
        
        stop = time.time()

        print('searching time:', stop-start)
        return results


@app.route('/preloaded', methods=['GET', 'POST'])
def preloaded():
    files = ['Candidatus Carsonella ruddii.dict', 'coronavirus 2 isolate.dict', 'peach.dict']
    
    if request.method == 'GET':
        return 'send post request'
    
    else:
        marker = int(request.files['marker'].read().decode())
        substring = request.files['substring'].read().decode()
    
        if not (1 <= marker <= 3):
            return 'marker should be an int within the range 1-4 inclusive'
        
        ind = marker - 1
        file = load_pickle(files[ind])

        fmi = FMIndex()
        bw = file['bwt']
        fmi.set_dict(file)
        
        print('loaded index')
        results = fuzzy_search(substring, fmi)

        return results

if __name__ == '__main__':
    app.debug = True
    app.run()