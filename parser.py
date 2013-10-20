import codecs
try:
    from pymongo import MongoClient
except ImportError:
    pass

def load_cedict(load_to_mongo=False):
    f = codecs.open('data/cedict_ts.u8', 'r', 'utf8')

    c = 0

    new_words = []
    for line in f:
        if line.startswith('#'):
            continue
        trad, simp = line.split(' ')[:2]
        pinyin = line[line.find('[')+1:line.find(']')]
        eng = line[line.find('/') + 1:line.rfind('/')]

        word = {'simplified': simp,
                'traditional': trad, 
                'english': eng, 
                'pinyin': pinyin}

        new_words.append(word)

    f.close()

    if load_to_mongo:
        client = MongoClient('localhost', 27017)
        db = client['cedict']
        words = db['entries']
        words.insert(new_words)
    
    return new_words

if __name__ == '__main__':
    print "Loading words..."

    words = load_cedict(load_to_mongo=False)

    print "Done! Loaded %d words." % len(words)