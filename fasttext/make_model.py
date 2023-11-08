import multiprocessing
import os
import gensim
import load_data, preprocess

class SentenceLoader(object):
    def __init__(self, source_dir):
        self.source_dir = source_dir

    def __iter__(self):
        for path, dirs, files in os.walk(self.source_dir):
            for file in files:
                with open(os.path.join(path, file), 'rt', encoding='utf-8') as f:
                    for line in f:
                        yield line.replace('\\n', '').replace(',', '').split(' ')

def make_model() :
    sentences_vocab = SentenceLoader(os.path.join(os.getcwd(), 'preprocess/'))
    sentences_train = SentenceLoader(os.path.join(os.getcwd(), 'preprocess/'))

    print('### sentence loader loaded.')

    config = {
        'min_count': 5,  # 등장 횟수가 5 이하인 단어는 무시
        'size': 350,     # 300차원짜리 벡터스페이스에 embedding
        #'vector_size': 350,     # 300차원짜리 벡터스페이스에 embedding
        'sg': 1,         # 0이면 CBOW, 1이면 skip-gram을 사용한다
        'batch_words': 10000,  # 사전을 구축할때 한번에 읽을 단어 수
        'iter': 10,      # 보통 딥러닝에서 말하는 epoch과 비슷한, 반복 횟수
        #'epochs': 10,      # 보통 딥러닝에서 말하는 epoch과 비슷한, 반복 횟수
        'workers': multiprocessing.cpu_count(),
    }

    model = gensim.models.FastText(**config) # Word2vec 모델 생성
    model.build_vocab(sentences_vocab)        # corpus 개수를 셈
    print('model.corpus_count: {}'.format(model.corpus_count))
    model.train(sentences_train, total_examples=model.corpus_count, epochs=config['iter']) # Word2Vec training
    # model.train(sentences_train, total_examples=model.corpus_count, epochs=config['epochs']) # Word2Vec training
    model.save(os.path.join(os.getcwd(), 'models/model'))                       # 모델을 'model' 파일에 저장

if __name__ == "__main__" :
    filename = 'kowiki-20231020-pages-articles-multistream.xml.bz2'
    total_worker = 8
    load_data.load_data(filename, total_worker)
    preprocess.preprocess(filename, total_worker)
    make_model()