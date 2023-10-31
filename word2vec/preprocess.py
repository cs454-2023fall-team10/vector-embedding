# -*- coding: utf-8 -*-
import os
import re
import multiprocessing

from konlpy.tag import Okt

# tag reference: http://semanticweb.kaist.ac.kr/research/morph/\n,


def extract_keywords(okt, text):
    results=[]
    lines=text.split("\n")
    for line in lines:
        #형태소 분석하기 -- (3)
        #단어의 기본형 사용
        malist = okt.pos(line, norm=True, stem=True)
        r = []
        for word in malist:
            if not word[1] in ["Josa", "Eomi", "Punctuation"]:
                r.append(word[0])
        rl = (" ".join(r)).strip()
        results.append(rl)

    return results

def worker(data):
    okt=Okt()
    remove_special_char = re.compile(r'[^가-힣^A-z^0-9^.^,^?^!^ ]') # 한글, 영어, 기본 기호를 제외한 문자들

    path, file_name = data
    print('process file: {}'.format(file_name))
    with open(os.path.join(path, file_name), 'rt', encoding='utf-8') as input:
        with open(os.path.join(os.getcwd(), 'preprocess/', file_name), 'wt', encoding='utf-8') as output:
            # step1에 있는, plain text를 읽어는다
            i = 0
            for input_line in input:
                if not input_line:
                    break
                # print('run start=',i)
                # 진행률을 출력하기 위한 부분
                i += 1
                if i % 1000 == 0:
                    print('[{}] {} finished'.format(file_name, i))

                # 특수 문자 제거 후 품사 분석 진행, 파일에 기록
                # print('for =',1)
                text = remove_special_char.sub(' ', input_line)
                chk = text.replace(' ','')
                # text = text.replace('\n','')
                # print('for =',2,' / han=',han,' / text=',text,' /len(text)=',len(text))
                if len(chk) == 0:
                    continue
                keyword = extract_keywords(okt, text)
                # print('for =',3)
                output.write(' '.join(keyword))
                # print('for =',4)
                output.write('\n')
                # print('run end=',i)


if __name__ == '__main__':
    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    print('loading multiprocessing pool...')

    data = []
    for path, dirs, files in os.walk('/home/babamba/vector_embedding/word2vec/parsed_data'):
        print(path, dirs, files)
        for file_name in files:
            data.append( (path, file_name) )
        worker(data[-1])
    pool.map(worker, data)
    pool.close()
    pool.join()
    print('End!')