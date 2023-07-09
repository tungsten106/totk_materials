import tkinter as tk
from tkinter import ttk
import pandas as pd
import datetime

# 创建空的装备列表
selected_equipments = []


def clear_selected_listbox():
    global selected_equipments
    #     public selected_equipments
    selected_equipments = []
    result_text.delete(1.0, tk.END)
    selected_listbox.delete(0, tk.END)  # 删除所有选项


# 添加装备到列表
def add_equipment():
    global selected_equipments
    (equip, level) = (combo_equipment.get(), combo_level.get())
    if (equip, level) not in selected_equipments:
        selected_equipments.append((equip, level))
        selected_listbox.insert(tk.END, (equip, level))


def calculate_materials():
    global selected_equipments, total_materials
    # 构建筛选条件
    conditions = pd.Series(False, index=equipment_data.index)
    for (equip, level) in selected_equipments:
        conditions = conditions | ((equipment_data['名称'] == equip) & (equipment_data['升级等级'] == level))
    selected_equipment = equipment_data[conditions]

    #     selected_materials = pd.DataFrame(columns=['材料名称', '需要的数量'])
    selected_materials = selected_equipment.iloc[:, -2:]

    total_materials = selected_materials.groupby('材料名称')['需要的数量'].sum().reset_index()

    result_text.delete(1.0, tk.END)
    result_text.insert(tk.END, total_materials.to_string(index=False))


def save_instructions():
    global total_materials
    ts = datetime.datetime.now().timestamp()

    ts = datetime.datetime.now().timestamp()
    total_materials.to_csv(f"saved_materials_{str(ts).split('.')[1]}.csv")
    print("材料表已保存到csv文件")


equipment_data = pd.read_csv('material_output_2.csv')

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

# 创建保存按钮
save_button = tk.Button(window, text="保存到csv", command=save_instructions)
save_button.pack()

# 启动主循环
window.mainloop()
