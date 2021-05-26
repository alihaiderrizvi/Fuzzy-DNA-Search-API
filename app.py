from flask import Flask, request, jsonify
from fm_index import FMIndex
from util import save_pickle, load_pickle
import time
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

def fuzzy_search(substring, fmi):
    
    '''
    Perform Fuzzy searching on FM Index and return indices.
    
    PARAMS:
    - fmi: FMIndex object
    - substring: Query string
    
    RETURNS:
    - Dictionary containing start and end indices for each score of the fuzzy search.
    
    '''
    
    results = {}
    unique = set()
    full_len = len(substring)
    
    for i in range(len(substring), int(len(substring)*0.78), -1):
        
        s = substring[:i]
        score = len(s)
        match = fmi.search(s) #query substring in Index
        res = [] # list to store indices of search
        
        for j in range(len(match)):
            match[j] = match[j][0]
            
            if match[j] not in unique:
                unique.add(match[j]) # to prevent overlapping, we store unique occurences and discard repeated occurences
                res.append([match[j], match[j]+full_len]) #save start and end indices of fuzzy substring
        
        if res:
            results[score] = sorted(res) # store key value pair
    
    return results


@app.route('/', methods=['GET'])
def home():
    return 'Fuzzy DNA Search API'

@app.route('/search', methods=['GET', 'POST'])
def index():
    
    if request.method == 'GET':
        return 'send post request'
    
    else:
        # print request content for logs
        print('request received')
        print('form:', request.form)
        print('files:', request.files)

        # read substring and dna file from request
        substring = request.form.get('substring')
        print('substring read', substring)

        T = request.files['file'].read().decode()
        print('file read')
        
        # create FM Index object
        fmi = FMIndex()
        
        print('encode text...')

        #build burrow's wheeler and suffix array
        start = time.time()
        bw, sa = fmi.encode(T)
        stop = time.time()
        
        print('suffix array build time:', stop-start)
        
        # find character count and ranks
        start = time.time()
        ranks, ch_count = fmi.rank_bwt(bw)
        stop = time.time()
        
        print('character count time:', stop-start)
        
        #save index
        save_pickle({'bwt': bw, 'sa': sa, 'text_len': len(T), 'ch_count': ch_count}, 'index.dict')
        fmi.ch_count = ch_count
        
        print('encode done!')

        start = time.time()
        results = fuzzy_search(substring, fmi) # query for fuzzy substrings
        stop = time.time()
        
        results[-1] = stop-start # save querying time
        
        print('Querying time:', stop-start) # print querying time for logs
        
        return jsonify(results)


@app.route('/preloaded', methods=['GET', 'POST'])
def preloaded():
    files = ['Candidatus Carsonella ruddii.dict', 'coronavirus 2 isolate.dict'] #preloaded index files
    
    if request.method == 'GET':
        return 'send post request'
    
    else:
        # print request content for logs
        print('form:', request.form)
        print('files:', request.files)
        
        #parse request
        marker = int(request.form.get('marker'))
        substring = str(request.form.get('substring'))
    
        if not (1 <= marker <= 2): # check if marker is in range
            return 'marker should be an int within the range 1-2 inclusive'
        
        ind = marker - 1
        file = load_pickle(files[ind]) # load corresponding index file

        #build FM Index object
        fmi = FMIndex()
        bw = file['bwt']
        fmi.set_dict(file)
        
        print('loaded index')
        
        start = time.time()
        results = fuzzy_search(substring, fmi) # query for fuzzy substrings
        stop = time.time()
        
        results[-1] = stop-start # save querying time
        print('searching time:', stop-start) # print querying time for logs
        
        return jsonify(results)

if __name__ == '__main__':
    app.debug = True
    app.run()
