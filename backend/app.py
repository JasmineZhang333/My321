from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import os
import json

# 初始化Flask应用
app = Flask(__name__)
CORS(app)  # 启用CORS支持跨域请求

# 数据库文件路径
DB_PATH = os.path.join(os.path.dirname(__file__), 'classmates.db')

# 初始化数据库
def init_db():
    # 检查数据库文件是否存在
    db_exists = os.path.exists(DB_PATH)
    
    # 连接到SQLite数据库
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 如果数据库不存在，创建表并插入初始数据
    if not db_exists:
        # 创建表
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
        initial_data = [
            {
                "id": 1,
                "name": "曹雅云",
                "location": {
                    "lat": 39.9042,
                    "lng": 116.4074
                },
                "city": "北京",
                "country": "中国"
            },
            {
                "id": 49,
                "name": "周一琦",
                "location": {
                    "lat": 22.5431,
                    "lng": 114.0579
                },
                "city": "深圳",
                "country": "中国"
            }
        ]
        
        for classmate in initial_data:
            cursor.execute('''
            INSERT INTO classmates (id, name, city, country, lat, lng)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                classmate["id"],
                classmate["name"],
                classmate["city"],
                classmate["country"],
                classmate["location"]["lat"],
                classmate["location"]["lng"]
            ))
        
        # 提交事务
        conn.commit()
    
    # 关闭连接
    conn.close()

# 将数据库记录转换为API响应格式
def format_classmate(row):
    return {
        "id": row[0],
        "name": row[1],
        "city": row[2],
        "country": row[3],
        "location": {
            "lat": row[4],
            "lng": row[5]
        }
    }

# API路由：获取所有同学信息
@app.route('/api/classmates', methods=['GET'])
def get_classmates():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, city, country, lat, lng FROM classmates')
    classmates = [format_classmate(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(classmates)

# API路由：获取单个同学信息
@app.route('/api/classmates/<int:classmate_id>', methods=['GET'])
def get_classmate(classmate_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, city, country, lat, lng FROM classmates WHERE id = ?', (classmate_id,))
    classmate = cursor.fetchone()
    conn.close()
    
    if classmate:
        return jsonify(format_classmate(classmate))
    else:
        return jsonify({"error": "同学不存在"}), 404

# API路由：添加新同学
@app.route('/api/classmates', methods=['POST'])
def add_classmate():
    data = request.json
    
    # 验证请求数据
    if not all(key in data for key in ['name', 'city', 'country', 'location']):
        return jsonify({"error": "缺少必要字段"}), 400
    
    if not all(key in data['location'] for key in ['lat', 'lng']):
        return jsonify({"error": "位置信息不完整"}), 400
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 插入新记录
    cursor.execute('''
    INSERT INTO classmates (name, city, country, lat, lng)
    VALUES (?, ?, ?, ?, ?)
    ''', (
        data["name"],
        data["city"],
        data["country"],
        data["location"]["lat"],
        data["location"]["lng"]
    ))
    
    # 获取新插入记录的ID
    new_id = cursor.lastrowid
    conn.commit()
    
    # 获取新插入的记录
    cursor.execute('SELECT id, name, city, country, lat, lng FROM classmates WHERE id = ?', (new_id,))
    new_classmate = cursor.fetchone()
    conn.close()
    
    return jsonify(format_classmate(new_classmate)), 201

# API路由：更新同学信息
@app.route('/api/classmates/<int:classmate_id>', methods=['PUT'])
def update_classmate(classmate_id):
    data = request.json
    
    # 验证请求数据
    if not all(key in data for key in ['name', 'city', 'country', 'location']):
        return jsonify({"error": "缺少必要字段"}), 400
    
    if not all(key in data['location'] for key in ['lat', 'lng']):
        return jsonify({"error": "位置信息不完整"}), 400
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 检查记录是否存在
    cursor.execute('SELECT id FROM classmates WHERE id = ?', (classmate_id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({"error": "同学不存在"}), 404
    
    # 更新记录
    cursor.execute('''
    UPDATE classmates
    SET name = ?, city = ?, country = ?, lat = ?, lng = ?
    WHERE id = ?
    ''', (
        data["name"],
        data["city"],
        data["country"],
        data["location"]["lat"],
        data["location"]["lng"],
        classmate_id
    ))
    conn.commit()
    
    # 获取更新后的记录
    cursor.execute('SELECT id, name, city, country, lat, lng FROM classmates WHERE id = ?', (classmate_id,))
    updated_classmate = cursor.fetchone()
    conn.close()
    
    return jsonify(format_classmate(updated_classmate))

# API路由：删除同学信息
@app.route('/api/classmates/<int:classmate_id>', methods=['DELETE'])
def delete_classmate(classmate_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # 检查记录是否存在
    cursor.execute('SELECT id FROM classmates WHERE id = ?', (classmate_id,))
    if not cursor.fetchone():
        conn.close()
        return jsonify({"error": "同学不存在"}), 404
    
    # 删除记录
    cursor.execute('DELETE FROM classmates WHERE id = ?', (classmate_id,))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "删除成功"})

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
    app.run(debug=True)