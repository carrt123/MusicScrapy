import sqlite3

conn = sqlite3.connect("../instance/development.db")
cursor = conn.cursor()

# 查询所有表
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# 打印所有表名
for table in tables:
    print(table[0])

# 插入数据
# singer_sql = "INSERT INTO singer (id, name, region, gender) VALUES (0, 'Taylor Swift', 30, 1);"
# cursor.execute(singer_sql)
#
# # 提交事务
# conn.commit()

# 查询歌手表并打印数据
# cursor.execute("SELECT * FROM singer;")
# print("Inserted Data:", cursor.fetchall())

# 删除刚才插入的数据
# delete_sql = "DELETE FROM singer WHERE id = 0;"
# cursor.execute(delete_sql)
#
# # 提交删除事务
# conn.commit()

# 再次查询歌手表以验证删除
# cursor.execute("DELETE FROM singer;")
# print("Data After Deletion:", cursor.fetchall())

query_sql = "SELECT id, mid FROM singer order by id desc limit 10;"
cursor.execute(query_sql)
for row in cursor.fetchall():
    print(row)
    print(row[1])
# 关闭连接
cursor.close()
conn.close()
