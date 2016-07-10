import storageutil
kafka = storageutil.getdb_factory("queue_zhixing", type='kafka', host="web14", port=51092)
print kafka.get()
print kafka.size()
