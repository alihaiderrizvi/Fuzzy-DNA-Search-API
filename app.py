from flask import Flask, render_template, request, redirect, url_for
from fm_index import FMIndex
from util import save_pickle, load_pickle, load_files, get_file_name_via_index
import time
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def fuzzy_search(substring, fmi):
    results = {}
    unique = set()
    
    for i in range(len(substring), int(len(substring)*0.78), -1):
        s = substring[:i]
        match = fmi.search(s)
        res = []
        for j in range(len(match)):
            match[j] = match[j][0]
            if match[j] not in unique:
                unique.add(match[j])
                res.append(match[j])
        if res:
            results[s] = sorted(res)
    
    return results
    
    # window = int(len(substring)*0.8)
    # while window < len(substring):
    #     i = 0

    #     while i+window <= len(substring):
    #         s = substring[i:i+window]
    #         perc = int((len(s) / len(substring)) * 100)
    #         match = fmi.search(s)
            
    #         if perc in results:
    #             results[perc].extend(match)
    #         else:
    #             results[perc] = match
            
    #         i += 1
    #     window += 1
    
    # for i in results:
    #     results[i].sort()
    
    # return results


@app.route('/', methods=['GET'])
def home():
    return 'Fuzzy DNA Search API'

@app.route('/search', methods=['GET', 'POST'])
def index():
    fmi = FMIndex()
    if request.method == 'GET':
        return 'send post request'
    else:
        print('request received')
        print('form:', request.form)

        print('file:', request.files['file'].read().decode())

        # read substring and dna file from request
        substring = request.form.get('substring')

        print('substring read', substring)
        T = request.files['file'].read().decode()
        print('file read')
        # filename = request.files['file'].filename
        

        fmi = FMIndex()
        
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
        
        stop = time.time()
        results['search time'] = stop-start
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
        start = time.time()
        results = fuzzy_search(substring, fmi)
        stop = time.time()
        results['search time'] = stop-start
        print('searching time:', stop-start)
        return results

if __name__ == '__main__':
    app.debug = True
    app.run()