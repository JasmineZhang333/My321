import sqlite3
import os

# 数据库文件路径
DB_PATH = os.path.join(os.path.dirname(__file__), 'classmates.db')

def batch_update_classmates(classmates_data):
    """
    批量更新同学数据
    :param classmates_data: 包含同学信息的列表
    :return: 更新结果统计
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    stats = {
        "updated": 0,
        "created": 0,
        "errors": 0,
        "error_details": []
    }
    
    try:
        for classmate in classmates_data:
            # 检查必要字段
            if not all(key in classmate for key in ['id', 'name', 'city', 'country', 'lat', 'lng']):
                stats["errors"] += 1
                stats["error_details"].append(f"数据缺少必要字段: {classmate}")
                continue
            
            # 检查ID是否存在
            cursor.execute('SELECT id FROM classmates WHERE id = ?', (classmate['id'],))
            exists = cursor.fetchone()
            
            if exists:
                # 更新现有记录
                cursor.execute('''
                UPDATE classmates
                SET name = ?, city = ?, country = ?, lat = ?, lng = ?
                WHERE id = ?
                ''', (
                    classmate["name"],
                    classmate["city"],
                    classmate["country"],
                    classmate["lat"],
                    classmate["lng"],
                    classmate["id"]
                ))
                stats["updated"] += 1
            else:
                # 插入新记录
                cursor.execute('''
                INSERT INTO classmates (id, name, city, country, lat, lng)
                VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    classmate["id"],
                    classmate["name"],
                    classmate["city"],
                    classmate["country"],
                    classmate["lat"],
                    classmate["lng"]
                ))
                stats["created"] += 1
        
        # 提交事务
        conn.commit()
    except Exception as e:
        # 回滚事务
        conn.rollback()
        stats["errors"] += 1
        stats["error_details"].append(str(e))
    finally:
        # 关闭连接
        conn.close()
    
    return stats