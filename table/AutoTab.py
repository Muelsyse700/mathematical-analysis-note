import os
import shutil
import csv
import hashlib

# ---------- 路径设置 ----------
base_dir = os.path.dirname(os.path.abspath(__file__))
input_dir = os.path.join(base_dir, "Input")
output_dir = os.path.join(base_dir, "Output")

os.makedirs(output_dir, exist_ok=True)

# ---------- 找到唯一 CSV ----------
csv_files = [f for f in os.listdir(input_dir) if f.endswith(".csv")]
if len(csv_files) != 1:
    raise ValueError("Input 文件夹中必须有且仅有一个 CSV 文件！")

csv_file = csv_files[0]
csv_path = os.path.join(input_dir, csv_file)
table_name = os.path.splitext(csv_file)[0]


# ---------- 生成哈希值 ----------
def stable_hash(name, length=6):
    h = hashlib.md5(name.encode("utf-8")).hexdigest()
    return h[:length]


hash_code = stable_hash(table_name)
label_name = hash_code

# ---------- 读取 CSV ----------
with open(csv_path, "r", encoding="utf-8") as f:
    reader = list(csv.reader(f))
header = reader[0]
rows = reader[1:]


# ---------- 转义特殊字符 ----------
def escape_latex(s):
    s = str(s)
    replacements = {
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\^{}",
        "\\": r"\textbackslash{}",
    }
    for old, new in replacements.items():
        s = s.replace(old, new)
    return s


# ---------- 计算列宽比例 ----------
def str_width(s):
    w = 0
    for ch in str(s):
        w += 2 if ord(ch) > 127 else 1
    return w


col_widths = []
for col_i in range(len(header)):
    max_len = str_width(header[col_i])
    for row in rows:
        if col_i < len(row):
            max_len = max(max_len, str_width(row[col_i]))
    col_widths.append(max_len)

total = sum(col_widths)
col_ratios = [round(w / total, 2) for w in col_widths]

# ---------- 列格式 ----------
col_formats = [f">{{\\hsize={r}\\hsize}}Z" for r in col_ratios]
col_format = " ".join(col_formats)

# ---------- 构造 LaTeX 代码 ----------
latex_lines = []
latex_lines.append(f"% Auto-generated from {csv_file}")
latex_lines.append(f"\\begin{{xltabular}}{{\\textwidth}}{{@{{}} {col_format} @{{}}}}")
latex_lines.append(f"\\caption{{{table_name}}} \\label{{tab:{label_name}}} \\\\")
latex_lines.append("\\toprule[0.08em]")
latex_lines.append(
    " & ".join([f"\\textbf{{{escape_latex(col)}}}" for col in header]) + " \\\\"
)
latex_lines.append("\\midrule[0.05em]")
latex_lines.append("\\endfirsthead")
latex_lines.append(
    f"\\multicolumn{{{len(header)}}}{{c}}{{表\\thetable \\quad {escape_latex(table_name)}（续）}} \\\\"
)
latex_lines.append("\\toprule[0.08em]")
latex_lines.append(
    " & ".join([f"\\textbf{{{escape_latex(col)}}}" for col in header]) + " \\\\"
)
latex_lines.append("\\midrule[0.05em]")
latex_lines.append("\\endhead")
latex_lines.append("\\midrule[0.05em]")
latex_lines.append(f"\\multicolumn{{{len(header)}}}{{r@{{}}}}{{（接下表）}} \\\\")
latex_lines.append("\\endfoot")
latex_lines.append("\\bottomrule[0.08em]")
latex_lines.append("\\endlastfoot")

for row in rows:
    line = " & ".join([escape_latex(cell) for cell in row]) + " \\\\"
    latex_lines.append(line)

latex_lines.append("\\end{xltabular}")

latex_content = "\n".join(latex_lines)

# ---------- 生成 Output 子文件夹 ----------
output_subdir = os.path.join(output_dir, label_name)
os.makedirs(output_subdir, exist_ok=True)

# ---------- 移动 CSV ----------
shutil.move(csv_path, os.path.join(output_subdir, csv_file))

# ---------- 写入 TEX ----------
output_tex_path = os.path.join(output_subdir, f"{label_name}.tex")
with open(output_tex_path, "w", encoding="utf-8") as f:
    f.write(latex_content)


# ---------- 更新索引文件 ----------
index_file = os.path.join(base_dir, "tables_index.txt")
input_line = f"\\input{{table/Output/{label_name}/{label_name}.tex}} % 表：{table_name}"

# 读取原索引内容
existing_lines = []
if os.path.exists(index_file):
    with open(index_file, "r", encoding="utf-8") as f:
        existing_lines = f.read().splitlines()

# 检查是否已存在相同条目
if input_line not in existing_lines:
    with open(index_file, "a", encoding="utf-8") as f:
        f.write(input_line + "\n")
        f.write(f"\\cref{{tab:{label_name}}}\n\n")
    print(f"✅ 已生成 LaTeX 表格：{output_tex_path}")
    print(f"✅ 已更新索引文件：{index_file}")
else:
    print(f"🔄 已覆盖同名表格，已更新对应的 LaTeX 表格：{output_tex_path}")
    print(f"🔄 索引文件无需更改：{index_file}")

# ---------- 输出命令 ----------
print(f"⭐ label: tab:{label_name}", end="\n")
print(f"♾️在文档中拷贝以下命令以插入或引用该表格：")
print(f"\\input{{table/Output/{label_name}/{label_name}.tex}} % 表：{table_name}")
print(f"\\cref{{tab:{label_name}}}\n")
