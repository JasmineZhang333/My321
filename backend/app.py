from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import os
import json

# 初始化Flask应用
# Flask是一个轻量级的Python Web框架，用于构建Web应用
app = Flask(__name__)
# 启用CORS(跨域资源共享)支持，允许前端(不同域名)访问后端API
CORS(app)  

# 数据库文件路径
# os.path.dirname(__file__)获取当前脚本所在的目录
# os.path.join()将目录和文件名拼接成完整的路径
DB_PATH = os.path.join(os.path.dirname(__file__), 'classmates.db')

# 初始化数据库
def init_db():
    # 检查数据库文件是否存在
    # os.path.exists()函数用于检查文件或目录是否存在
    db_exists = os.path.exists(DB_PATH)
    
    # 连接到SQLite数据库
    # sqlite3.connect()函数用于创建数据库连接
    # 如果数据库文件不存在，会自动创建一个新的数据库文件
    conn = sqlite3.connect(DB_PATH)
    # 创建游标对象，用于执行SQL语句
    cursor = conn.cursor()
    
    # 如果数据库不存在，创建表并插入初始数据
    if not db_exists:
        # 创建表
        # 使用三引号(''')可以编写多行字符串，这里用于编写SQL语句
        # CREATE TABLE语句用于创建数据库表
        # id: 自增主键，用于唯一标识每条记录
        # name: 同学姓名，文本类型，不允许为空
        # city: 城市，文本类型，不允许为空
        # country: 国家，文本类型，不允许为空
        # lat: 纬度，浮点数类型，不允许为空
        # lng: 经度，浮点数类型，不允许为空
        cursor.execute('''
        CREATE TABLE classmates (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            city TEXT NOT NULL,
            country TEXT NOT NULL,
            lat REAL NOT NULL,
            lng REAL NOT NULL
        )
        ''')
        
        # 插入初始数据
        # 这里定义了两条初始记录，包含同学的基本信息和位置信息
        initial_data = [
            {
                "id": 1,
                "name": "曹雅云",
                "location": {
                    "lat": 39.9042,  # 北京的纬度
                    "lng": 116.4074  # 北京的经度
                },
                "city": "北京",
                "country": "中国"
            },
            {
                "id": 49,
                "name": "周一琦",
                "location": {
                    "lat": 22.5431,  # 深圳的纬度
                    "lng": 114.0579  # 深圳的经度
                },
                "city": "深圳",
                "country": "中国"
            }
        ]
        
        # 遍历初始数据，将每条记录插入到数据库中
        for classmate in initial_data:
            # INSERT INTO语句用于向表中插入数据
            # VALUES (?, ?, ?, ?, ?, ?)中的问号是占位符，防止SQL注入攻击
            cursor.execute('''
            INSERT INTO classmates (id, name, city, country, lat, lng)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                classmate["id"],              # 同学ID
                classmate["name"],            # 同学姓名
                classmate["city"],            # 城市
                classmate["country"],          # 国家
                classmate["location"]["lat"],  # 纬度
                classmate["location"]["lng"]   # 经度
            ))
        
        # 提交事务
        # 在SQLite中，所有更改都在事务中进行，需要调用commit()方法才能保存更改
        conn.commit()
    
    # 关闭数据库连接
    # 使用完数据库后，应该关闭连接以释放资源
    conn.close()

# 将数据库记录转换为API响应格式
# 这个函数将数据库查询结果(元组)转换为前端需要的JSON格式
def format_classmate(row):
    return {
        "id": row[0],        # 同学ID
        "name": row[1],      # 同学姓名
        "city": row[2],      # 城市
        "country": row[3],   # 国家
        "location": {        # 位置信息，包含经纬度
            "lat": row[4],   # 纬度
            "lng": row[5]    # 经度
        }
    }

# API路由：获取所有同学信息
# @app.route装饰器定义了API的URL路径和允许的HTTP方法
# '/api/classmates'是API的URL路径，methods=['GET']表示这个API只接受GET请求
@app.route('/api/classmates', methods=['GET'])
def get_classmates():
    # 连接到SQLite数据库
    conn = sqlite3.connect(DB_PATH)
    # 创建游标对象
    cursor = conn.cursor()
    # 执行SQL查询，获取所有同学的信息
    cursor.execute('SELECT id, name, city, country, lat, lng FROM classmates')
    # 使用列表推导式将查询结果转换为JSON格式
    # cursor.fetchall()获取所有查询结果
    # format_classmate()函数将每行数据转换为前端需要的格式
    classmates = [format_classmate(row) for row in cursor.fetchall()]
    # 关闭数据库连接
    conn.close()
    # 使用jsonify()函数将Python列表转换为JSON响应返回给前端
    return jsonify(classmates)

# API路由：获取单个同学信息
# '<int:classmate_id>'是URL参数，用于指定要获取的同学ID
# int:表示这个参数应该是整数类型
@app.route('/api/classmates/<int:classmate_id>', methods=['GET'])
def get_classmate(classmate_id):
    # 连接到SQLite数据库
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # 执行SQL查询，使用参数化查询防止SQL注入
    # WHERE id = ? 是条件语句，问号是参数占位符
    # (classmate_id,) 是传递给占位符的参数，注意逗号是必须的，表示这是一个元组
    cursor.execute('SELECT id, name, city, country, lat, lng FROM classmates WHERE id = ?', (classmate_id,))
    # 获取查询结果的第一行，如果没有结果则返回None
    classmate = cursor.fetchone()
    conn.close()
    
    # 如果找到了对应ID的同学
    if classmate:
        # 将数据库记录转换为JSON格式并返回
        return jsonify(format_classmate(classmate))
    else:
        # 如果没有找到，返回404错误和错误信息
        # 404是HTTP状态码，表示"未找到"
        return jsonify({"error": "同学不存在"}), 404

# API路由：添加新同学
# POST方法用于创建新资源
@app.route('/api/classmates', methods=['POST'])
def add_classmate():
    # 获取请求中的JSON数据
    # request.json包含了前端发送的JSON数据
    data = request.json
    
    # 验证请求数据是否包含所有必要字段
    # all()函数检查所有条件是否都为True
    if not all(key in data for key in ['name', 'city', 'country', 'location']):
        # 如果缺少必要字段，返回400错误(Bad Request)
        return jsonify({"error": "缺少必要字段"}), 400
    
    # 验证位置信息是否完整
    if not all(key in data['location'] for key in ['lat', 'lng']):
        # 如果位置信息不完整，返回400错误
        return jsonify({"error": "位置信息不完整"}), 400
    
    # 连接到SQLite数据库
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 插入新记录
    # 使用参数化查询防止SQL注入
    cursor.execute('''
    INSERT INTO classmates (name, city, country, lat, lng)
    VALUES (?, ?, ?, ?, ?)
    ''', (
        data["name"],              # 同学姓名
        data["city"],              # 城市
        data["country"],           # 国家
        data["location"]["lat"],   # 纬度
        data["location"]["lng"]    # 经度
    ))
    
    # 获取新插入记录的ID
    # lastrowid属性包含最后插入行的行ID
    new_id = cursor.lastrowid
    # 提交事务，保存更改
    conn.commit()
    
    # 获取新插入的记录，以便返回给前端
    cursor.execute('SELECT id, name, city, country, lat, lng FROM classmates WHERE id = ?', (new_id,))
    new_classmate = cursor.fetchone()
    # 关闭数据库连接
    conn.close()
    
    # 返回新创建的同学信息和201状态码(Created)
    # 201状态码表示资源已成功创建
    return jsonify(format_classmate(new_classmate)), 201

# API路由：更新同学信息
# PUT方法用于更新已存在的资源
# '<int:classmate_id>'是URL参数，用于指定要更新的同学ID
@app.route('/api/classmates/<int:classmate_id>', methods=['PUT'])
def update_classmate(classmate_id):
    # 获取请求中的JSON数据
    data = request.json
    
    # 验证请求数据是否包含所有必要字段
    if not all(key in data for key in ['name', 'city', 'country', 'location']):
        # 如果缺少必要字段，返回400错误(Bad Request)
        return jsonify({"error": "缺少必要字段"}), 400
    
    # 验证位置信息是否完整
    if not all(key in data['location'] for key in ['lat', 'lng']):
        # 如果位置信息不完整，返回400错误
        return jsonify({"error": "位置信息不完整"}), 400
    
    # 连接到SQLite数据库
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 检查记录是否存在
    # 在更新前先检查同学ID是否存在于数据库中
    cursor.execute('SELECT id FROM classmates WHERE id = ?', (classmate_id,))
    if not cursor.fetchone():
        # 如果同学ID不存在，关闭连接并返回404错误
        conn.close()
        return jsonify({"error": "同学不存在"}), 404
    
    # 更新记录
    # UPDATE语句用于修改已存在的记录
    cursor.execute('''
    UPDATE classmates
    SET name = ?, city = ?, country = ?, lat = ?, lng = ?
    WHERE id = ?
    ''', (
        data["name"],              # 同学姓名
        data["city"],              # 城市
        data["country"],           # 国家
        data["location"]["lat"],   # 纬度
        data["location"]["lng"],   # 经度
        classmate_id               # 同学ID
    ))
    # 提交事务，保存更改
    conn.commit()
    
    # 获取更新后的记录，以便返回给前端
    cursor.execute('SELECT id, name, city, country, lat, lng FROM classmates WHERE id = ?', (classmate_id,))
    updated_classmate = cursor.fetchone()
    # 关闭数据库连接
    conn.close()
    
    # 返回更新后的同学信息
    return jsonify(format_classmate(updated_classmate))

# API路由：删除同学信息
# DELETE方法用于删除资源
# '<int:classmate_id>'是URL参数，用于指定要删除的同学ID
@app.route('/api/classmates/<int:classmate_id>', methods=['DELETE'])
def delete_classmate(classmate_id):
    # 连接到SQLite数据库
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 检查记录是否存在
    # 在删除前先检查同学ID是否存在于数据库中
    cursor.execute('SELECT id FROM classmates WHERE id = ?', (classmate_id,))
    if not cursor.fetchone():
        # 如果同学ID不存在，关闭连接并返回404错误
        conn.close()
        return jsonify({"error": "同学不存在"}), 404
    
    # 删除记录
    # DELETE语句用于删除数据库中的记录
    cursor.execute('DELETE FROM classmates WHERE id = ?', (classmate_id,))
    # 提交事务，保存更改
    conn.commit()
    # 关闭数据库连接
    conn.close()
    
    # 返回成功消息
    return jsonify({"message": "删除成功"})

# API路由：批量更新同学信息
# 这个API用于一次性更新多个同学的信息，通常用于批量导入数据
@app.route('/api/classmates/batch', methods=['POST'])
def batch_update_classmates():
    # 获取请求中的JSON数据
    data = request.json
    
    # 验证数据是否为列表格式
    if not isinstance(data, list):
        # 如果不是列表格式，返回400错误
        return jsonify({"error": "请求数据必须是数组格式"}), 400
    
    # 处理数据格式，将不同格式的输入统一转换为标准格式
    formatted_data = []
    for item in data:
        # 验证必要字段是否存在
        if not all(key in item for key in ['id', 'name', 'city', 'country']):
            # 如果缺少必要字段，返回400错误
            return jsonify({"error": f"数据缺少必要字段: {item}"}), 400
        
        # 验证位置信息，支持两种格式：
        # 1. 位置信息在location对象中
        # 2. 位置信息直接在item对象中
        if 'location' in item and all(key in item['location'] for key in ['lat', 'lng']):
            # 格式1：位置信息在location对象中
            lat = item['location']['lat']
            lng = item['location']['lng']
        elif all(key in item for key in ['lat', 'lng']):
            # 格式2：位置信息直接在item对象中
            lat = item['lat']
            lng = item['lng']
        else:
            # 如果位置信息不完整，返回400错误
            return jsonify({"error": f"位置信息不完整: {item}"}), 400
        
        # 将数据添加到格式化数据列表中
        formatted_data.append({
            "id": item["id"],        # 同学ID
            "name": item["name"],    # 同学姓名
            "city": item["city"],    # 城市
            "country": item["country"],  # 国家
            "lat": lat,              # 纬度
            "lng": lng               # 经度
        })
    
    # 导入批量更新模块
    # 为了保持代码结构清晰，批量更新的具体实现被放在单独的模块中
    from batch_update import batch_update_classmates as update_func
    
    # 执行批量更新
    result = update_func(formatted_data)
    
    # 返回更新结果
    return jsonify(result)

# API路由：获取统计信息
@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 按国家统计
    cursor.execute('SELECT country, COUNT(*) FROM classmates GROUP BY country')
    country_stats = {row[0]: row[1] for row in cursor.fetchall()}
    
    # 按城市统计
    cursor.execute('SELECT city, COUNT(*) FROM classmates GROUP BY city')
    city_stats = {row[0]: row[1] for row in cursor.fetchall()}
    
    conn.close()
    
    return jsonify({
        "country_stats": country_stats,
        "city_stats": city_stats,
        "total": sum(country_stats.values())
    })

# 初始化数据库并启动应用
if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5001)