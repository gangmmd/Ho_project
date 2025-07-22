import tkinter as tk
from tkinter import messagebox

def simplify_logic():
    try:
        
        truth_table = truth_table_entry.get()
        
        
        truth_values = [int(x) for x in truth_table.split(",")]
        
        
        num_vars = 0
        while 2 ** num_vars < len(truth_values):
            num_vars += 1

        if 2 ** num_vars != len(truth_values):
            raise ValueError("تعداد مقادیر جدول حقیقت باید توان 2 باشد.")

        
        kmap = create_karnaugh_map(truth_values, num_vars)

        
        simplified_expression = simplify_kmap(kmap, num_vars)
        
        
        result_label.config(text=f"عبارت ساده‌شده: {simplified_expression}")
    except Exception as e:
        messagebox.showerror("Error", f"خطا در پردازش: {e}")

def create_karnaugh_map(truth_values, num_vars):
    """ایجاد جدول کارنو بر اساس مقادیر جدول حقیقت و تعداد متغیرها"""
    rows = 2 ** (num_vars // 2)
    cols = 2 ** (num_vars - num_vars // 2)
    kmap = [[0] * cols for _ in range(rows)]

    gray_code = lambda n: n ^ (n >> 1)

    for i, value in enumerate(truth_values):
        row = gray_code((i >> (num_vars - num_vars // 2)) & (rows - 1))
        col = gray_code(i & (cols - 1))
        kmap[row][col] = value

    return kmap

def simplify_kmap(kmap, num_vars):
    """ساده‌سازی جدول کارنو و تولید عبارت منطقی ساده‌شده"""
    rows, cols = len(kmap), len(kmap[0])
    visited = [[False] * cols for _ in range(rows)]
    groups = []

    def expand_group(start_row, start_col):
        """ایجاد یک گروه از سلول‌های مجاور دارای مقدار 1"""
        queue = [(start_row, start_col)]
        group = []

        while queue:
            row, col = queue.pop(0)
            if visited[row][col]:
                continue

            visited[row][col] = True
            group.append((row, col))

            
            for d_row, d_col in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                n_row = (row + d_row) % rows
                n_col = (col + d_col) % cols

                if kmap[n_row][n_col] == 1 and not visited[n_row][n_col]:
                    queue.append((n_row, n_col))

        return group

    def group_to_expression(group):
        """تبدیل گروه به یک عبارت منطقی"""
        row_bits = [None] * (num_vars // 2)
        col_bits = [None] * (num_vars - num_vars // 2)

        for row, col in group:
            binary_row = f"{row:0{num_vars // 2}b}"
            binary_col = f"{col:0{num_vars - num_vars // 2}b}"

            for i, bit in enumerate(binary_row):
                if row_bits[i] is None:
                    row_bits[i] = bit
                elif row_bits[i] != bit:
                    row_bits[i] = "-"

            for i, bit in enumerate(binary_col):
                if col_bits[i] is None:
                    col_bits[i] = bit
                elif col_bits[i] != bit:
                    col_bits[i] = "-"

        expression = []
        for i, bit in enumerate(row_bits + col_bits):
            if bit == "1":
                expression.append(f"X{i}")
            elif bit == "0":
                expression.append(f"!X{i}")

        return "".join(expression)

    
    for row in range(rows):
        for col in range(cols):
            if kmap[row][col] == 1 and not visited[row][col]:
                group = expand_group(row, col)
                groups.append(group)

    
    if not groups:
        return "0"

    
    minimized_groups = []
    covered = set()

    for group in groups:
        if not any(cell in covered for cell in group):
            minimized_groups.append(group)
            covered.update(group)

    
    expressions = [group_to_expression(group) for group in minimized_groups]

    
    unique_expressions = list(set(expressions))

    return " + ".join(unique_expressions)


root = tk.Tk()
root.title("ساده‌ساز مدار منطقی - جدول کارنو")
root.geometry("500x300")


title_label = tk.Label(root, text="ساده‌ ساز مدار منطقی با جدول کارنو", font=("Arial", 14), pady=10)
title_label.pack()


input_frame = tk.Frame(root)
input_frame.pack(pady=10)

truth_table_label = tk.Label(input_frame, text="جدول حقیقت (مقادیر 0 و 1, جدا شده با کاما):", font=("Arial", 12))
truth_table_label.pack(side=tk.LEFT, padx=5)

truth_table_entry = tk.Entry(input_frame, width=30, font=("Arial", 12))
truth_table_entry.pack(side=tk.LEFT, padx=5)


simplify_button = tk.Button(root, text="ساده‌سازی", font=("Arial", 12), command=simplify_logic)
simplify_button.pack(pady=10)


result_label = tk.Label(root, text="", font=("Arial", 12), fg="green")
result_label.pack(pady=20)


root.mainloop()
