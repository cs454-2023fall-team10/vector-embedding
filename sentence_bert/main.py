from sentence_transformers import SentenceTransformer, util
import numpy as np

corpus = ["배포 시스템 관련 문의", "DevOps 요청 사항 작성", "VPN 요청 사항", "DevOps팀 연결"]

model = SentenceTransformer('./result.pt')

corpus_embeddings = model.encode(corpus)

query = "제품의 실시간 서비스 중단 문제로 어려움을 겪고 있으며, 빠른 대응이 필요합니다"

top_k = len(corpus)
query_embedding = model.encode(query)
cos_scores = util.pytorch_cos_sim(query_embedding, corpus_embeddings)[0]
cos_scores = cos_scores.cpu()
top_results = np.argpartition(-cos_scores, range(top_k))[0:top_k]

for idx in top_results:
  print(corpus[idx].strip(), "(Score: %.4f)" % (cos_scores[idx]))