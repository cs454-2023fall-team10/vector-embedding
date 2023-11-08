# https://question99.tistory.com/111
import bz2
import os, re

file_name = "kowiki-20231020-pages-articles-multistream.xml.bz2"
# # bz2 파일 읽기
# with open(os.path.join(os.getcwd(), 'data', file_name), "rb") as f:
#     data = f.read()
#     decom_data = bz2.decompress(data).decode()
#     print(decom_data[:500])  # 내용 확인 하기

# # text 파일로 저장
# f = open(os.path.join(os.getcwd(), 'step01', file_name), 'w', encoding='UTF-8')
# f.write(decom_data)
# f.close()

def list_wiki(dirname):
    filepaths = []
    filenames = os.listdir(dirname)
    for filename in filenames:
        filepath = os.path.join(dirname, filename)

        if os.path.isdir(filepath):
            # 재귀 함수
            filepaths.extend(list_wiki(filepath))
        else:
            find = re.findall(r"wiki_[0-9][0-9]", filepath)
            if 0 < len(find):
                filepaths.append(filepath)
    return sorted(filepaths)

def load_data(file_name, total_worker) :
    filepaths = list_wiki('data/text')
    total_files = len(filepaths)
    total_worker = 8
    files_per_worker = total_files // total_worker

    count = 0
    for i in range(total_worker) :
        outfile = open(os.path.join(os.getcwd(), 'parsed_data', file_name + '_' + str(i) + '.txt'), "w")
        for j in range(files_per_worker) :
            with open(filepaths[count]) as infile:
                contents = infile.read()
                outfile.write(contents)
                count += 1