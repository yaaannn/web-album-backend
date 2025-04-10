import sqlite3

# 为db.sqlite3添加一条管理员数据


def add_admin_data():
    # 连接数据库
    conn = sqlite3.connect("db.sqlite3")
    cursor = conn.cursor()
    # 插入数据，INSERT INTO a_admin (id, username, password, email, jwt_version, is_freeze) VALUES (1,'admin','admin123','example@example.com',0,false);
    cursor.execute(
        """INSERT INTO a_admin (id, username, password, email, jwt_version, is_freeze) VALUES (1,'admin','admin123','example@example.com',0,false);"""
    )
    # 提交事务
    conn.commit()
    # 关闭连接
    cursor.close()
    conn.close()
    print("添加管理员数据成功")


if __name__ == "__main__":
    add_admin_data()
