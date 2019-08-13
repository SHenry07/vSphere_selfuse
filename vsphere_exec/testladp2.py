from ldap3 import Server, Connection, ALL

host = "ldap://192.168.100.16"
server = Server(host,port=389, use_ssl=False, get_info=ALL)

conn = Connection(server,"sunheng@banksteeltech.local","yunsiwole.",auto_bind=True)


res = conn.search('dc=banksteeltech,dc=local', '(objectclass=user)',attributes=['objectclass'])


print(res) # search是否成功（True，False）
print(conn.result) # 查询失败的原因
print(conn.entries)