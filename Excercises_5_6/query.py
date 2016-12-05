from elasticsearch import Elasticsearch


es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
index = 'gazetaru'
home_page = 'https://www.gazeta.ru'


def find_query(query, index=index):
    entries = []
    res = es.search(index=index, q=query)
    for item in res['hits']['hits']:
        entries.append(dict(hub=item['_type'], id=item['_id'], title=item['_source']['title'],
             text=item['_source']['text'][:200]+'...', url=home_page+item['_source']['url']))
    return entries
