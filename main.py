import tkinter as tk
from tkinter import messagebox, scrolledtext,filedialog
import json
from enum import Enum
from huffman_encode import encode_huffman as eh
from huffman_decode import decompress_huffman as dh

class ActionType(Enum):
    ENCODE = "Mã hoá"
    DECODE = "Giải mã"

# === Khởi tạo GUI ===
root = tk.Tk()
root.title("Huffman Tool")
root.geometry("950x600")
action_type = tk.StringVar()
action_type.set(ActionType.ENCODE.value)

selected_file:str|None = None

def update_action_type(act_type):
    action_type.set(act_type)
    print(act_type)

def select_file():
    if action_type.get()==ActionType.DECODE.value:
        file_path = filedialog.askopenfilename(
            title="Select File",
            filetypes=[("Huffman file","*.huff")]
        )
    else: file_path = filedialog.askopenfilename(
        title="Select File",
        filetypes=[("Any","*")]
    )
    if file_path:
        entry.config(state='normal')
        entry.delete(0,tk.END)
        entry.insert(0,file_path)
        entry.config(state='readonly')
        return file_path
    return None

def open_file():
    global selected_file
    selected_file = select_file()

# === Thực hiện hành động chính ===
def process_action():
    if not selected_file:
        messagebox.showerror("Lỗi", "Chưa chọn file.")
        return

    try:
        if action_type.get() == ActionType.ENCODE.value:
            [output_path,mapping_path] = eh(selected_file)
            with open(mapping_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                pretty_text = json.dumps(data, indent=4, ensure_ascii=False)
                custom_input.delete("1.0", tk.END)
                custom_input.insert(tk.END, pretty_text)
            log_text.config(state='normal')
            log_text.insert(tk.END,f"✅ Compressed file: {output_path}\n")
            log_text.insert(tk.END,f"✅ Huffman table: {mapping_path}\n")
            log_text.config(state='disabled')

        elif selected_file.endswith(".huff"):
            base = '.'.join(selected_file.split('.')[:-2])
            table_path = f"{base}_mapping.json"
            with open(table_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                pretty_text = json.dumps(data, indent=4, ensure_ascii=False)
                custom_input.delete("1.0", tk.END)
                custom_input.insert(tk.END, pretty_text)

            output_path = dh(selected_file, table_path)
            log_text.config(state='normal')
            log_text.insert(tk.END,f"✅ File đã giải mã: {output_path}\n")
            log_text.config(state='disabled')

    except Exception as e:
        log_text.insert(tk.END, f"❌ Lỗi xử lý: {e}\n")

# === Giao diện ===

# Cột trái
left_frame = tk.Frame(root, width=300)
left_frame.pack(side=tk.LEFT,fill=tk.Y, padx=10, pady=10)

tk.Label(left_frame, text="Chọn chức năng:").pack()
actions = [act.value for act in ActionType]
tk.OptionMenu(left_frame, action_type, *actions, command=update_action_type).pack(pady=5)

tk.Button(left_frame, text="Thực hiện", command=process_action).pack(pady=10)

# Cột phải
right_frame = tk.Frame(root)
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)


# Top frame chứa thanh chọn file
top_frame = tk.Frame(right_frame)
top_frame.pack(padx=10, pady=10)

entry = tk.Entry(top_frame,width=50)
entry.config(state='readonly')
entry.grid(column=0, row=0,padx=5)
tk.Button(top_frame, text="Chọn file:",command=open_file).grid(column=1,row=0,padx=5)

# Ghi chú giữa
middle_frame = tk.LabelFrame(right_frame, text="Bảng tần số")
middle_frame.pack(fill="both", expand=True, padx=5, pady=(0, 5))

custom_input = scrolledtext.ScrolledText(middle_frame, wrap=tk.WORD, height=6)
custom_input.pack(fill="both", expand=True)

# Log dưới
log_frame = tk.LabelFrame(right_frame, text="Log")
log_frame.pack(fill="both", expand=True, padx=5, pady=(0, 5))

log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, height=4)
log_text.pack(fill="both",expand=True)
log_text.config(state='disabled',bg=root.cget('bg'))


root.mainloop()
