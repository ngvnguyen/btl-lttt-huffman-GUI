import json
import os

def decompress_huffman(huff_path: str, mapping_path: str):
    # Đọc bảng mã giải nén từ file JSON
    with open(mapping_path, 'r') as f:
        code_map = json.load(f)  # {bit_string: byte_value}

    # Đọc dữ liệu từ file .huff (đã nén theo Huffman)
    with open(huff_path, 'rb') as f:
        compressed_bytes = f.read()

    # Chuyển byte → chuỗi bit
    bit_string = ''.join(f'{byte:08b}' for byte in compressed_bytes)

    # Lấy byte padding_length
    padding_length = int(bit_string[:8],2)
    bit_string = bit_string[8:]
    if padding_length>0:
        bit_string = bit_string[:-padding_length] # Bỏ padding ở cuối

    # Giải mã chuỗi bit thành dãy byte gốc
    decoded_bytes = bytearray()
    current_code = ""

    for bit in bit_string:
        current_code += bit
        if current_code in code_map:
            decoded_bytes.append(code_map[current_code])
            current_code = ""


    original_ext = os.path.basename(huff_path).split('.')[-2]  # ví dụ: 'jpg' trong 'a.jpg.huff'
    base = '.'.join(huff_path.split('.')[:-2])  # 'a'
    output_path = f"{base}_restored.{original_ext}"

    # Ghi file kết quả ra đĩa
    with open(output_path, 'wb') as out_file:
        out_file.write(decoded_bytes)
    return output_path
