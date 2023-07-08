import pandas as pd
from flask import Flask, render_template, request

app = Flask(__name__)

# 加载装备数据
equipment_data = pd.read_csv('../../Documents/material_output.csv')

# 创建空的装备列表
selected_equipments = []


@app.route('/')
def index():
    # 渲染首页模板
    return render_template('index.html', equipments=equipment_data['名称'].unique().tolist(),
                           levels=equipment_data['升级等级'].unique().tolist(),
                           selected_equipments=selected_equipments)


@app.route('/add_equipment', methods=['POST'])
def add_equipment():
    equip = request.form.get('equipment')
    level = request.form.get('level')
    if (equip, level) not in selected_equipments:
        selected_equipments.append((equip, level))
    return ''


@app.route('/clear_selected')
def clear_selected():
    selected_equipments.clear()
    return ''


@app.route('/calculate_materials')
def calculate_materials():
    # 构建筛选条件
    conditions = pd.Series(False, index=equipment_data.index)
    for (equip, level) in selected_equipments:
        conditions = conditions | ((equipment_data['名称'] == equip) & (equipment_data['升级等级'] == level))
    selected_equipment = equipment_data[conditions]

    selected_materials = selected_equipment[['材料名称', '需要的数量']].copy()
    total_materials = selected_materials.groupby('材料名称')['需要的数量'].sum().reset_index()

    return total_materials.to_string(index=False)


if __name__ == '__main__':
    app.run(debug=True)
