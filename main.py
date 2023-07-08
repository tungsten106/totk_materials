import tkinter as tk
from tkinter import ttk
import pandas as pd

# 创建空的装备列表
selected_equipments = []


def clear_selected_listbox():
    selected_equipments = []
    result_text.delete(1.0, tk.END)
    selected_listbox.delete(0, tk.END)  # 删除所有选项


# 添加装备到列表
def add_equipment():
    (equip, level) = (combo_equipment.get(), combo_level.get())
    if (equip, level) not in selected_equipments:
        selected_equipments.append((equip, level))
        selected_listbox.insert(tk.END, (equip, level))


def calculate_materials():
    # 构建筛选条件
    conditions = pd.Series(False, index=equipment_data.index)
    for (equip, level) in selected_equipments:
        conditions = conditions | ((equipment_data['名称'] == equip) & (equipment_data['升级等级'] == level))
    selected_equipment = equipment_data[conditions]

    selected_materials = pd.DataFrame(columns=['材料名称', '需要的数量'])

    #     selected_materials = pd.DataFrame(columns=['材料名称', '需要的数量'])
    #     for _, row in selected_equipment.iterrows():
    #         material = row['材料名称']
    #         quantity = row['需要的数量']
    # #         selected_materials = selected_materials.append({'材料名称': material, '需要的数量': quantity},
    # #                                                            ignore_index=True)
    #         selected_materials =
    #     selected_materials
    selected_materials = selected_equipment.iloc[:, -2:]

    total_materials = selected_materials.groupby('材料名称')['需要的数量'].sum().reset_index()

    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, total_materials.to_string(index=False))


equipment_data = pd.read_csv('../../Documents/material_output.csv')


# 创建主窗口
window = tk.Tk()
window.title("装备材料计算器")

# 创建下拉选择框和标签
label_equipment = ttk.Label(window, text="装备名称:")
label_equipment.pack()
combo_equipment = ttk.Combobox(window, values=equipment_data['名称'].unique().tolist())
combo_equipment.pack()

label_level = ttk.Label(window, text="装备等级:")
label_level.pack()
combo_level = ttk.Combobox(window, values=equipment_data['升级等级'].unique().tolist())
combo_level.pack()

# 创建添加按钮
add_button = ttk.Button(window, text="添加", command=add_equipment)
add_button.pack()

# 创建选择列表框
selected_listbox = tk.Listbox(window)
selected_listbox.pack()

# 创建清空选项的按钮
clear_button = tk.Button(window, text='清空选项', command=clear_selected_listbox)
clear_button.pack()

# 创建计算按钮
calculate_button = ttk.Button(window, text="计算", command=calculate_materials)
calculate_button.pack()

# 创建结果文本框
result_text = tk.Text(window, height=10, width=30)
result_text.pack()

# 启动主循环
window.mainloop()
