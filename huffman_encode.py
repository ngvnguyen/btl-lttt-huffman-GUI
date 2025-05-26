import os
import json
import heapq

def encode_huffman(filepath):
    hc = HuffmanCoding(filepath)
    return hc.compress()

class HuffmanCoding:
    def __init__(self, path):
        self.path = path
        self.codes = {}
        self.reverse_mapping = {}

    class HeapNode:
        def __init__(self, byte, freq):
            self.byte = byte
            self.freq = freq
            self.left = None
            self.right = None

        def __lt__(self, other):
            return self.freq < other.freq

    def make_frequency_dict(self, data):
        freq = {}
        for b in data:
            freq[b] = freq.get(b, 0) + 1
        return freq

    def build_heap(self, frequency):
        heap = []
        for byte, freq in frequency.items():
            node = self.HeapNode(byte, freq)
            heapq.heappush(heap, node)
        return heap

    def merge_nodes(self, heap):
        while len(heap) > 1:
            node1 = heapq.heappop(heap)
            node2 = heapq.heappop(heap)
            merged = self.HeapNode(None, node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2
            heapq.heappush(heap, merged)
        return heap[0]

    def make_codes_helper(self, node, current_code):
        if node is None:
            return
        if node.byte is not None:
            self.codes[node.byte] = current_code
            self.reverse_mapping[current_code] = node.byte
            return
        self.make_codes_helper(node.left, current_code + "0")
        self.make_codes_helper(node.right, current_code + "1")

    def make_codes(self, root):
        self.make_codes_helper(root, "")

    def get_encoded_text(self, data):
        return ''.join(self.codes[byte] for byte in data)

    def pad_encoded_text(self, encoded_text):
        extra_padding = 8 - len(encoded_text) % 8
        encoded_text += "0" * extra_padding
        padded_info = "{0:08b}".format(extra_padding)
        return padded_info + encoded_text

    def get_byte_array(self, padded_encoded_text):
        return bytearray(
            int(padded_encoded_text[i:i+8], 2)
            for i in range(0, len(padded_encoded_text), 8)
        )

    def compress(self):
        filename, ext = os.path.splitext(self.path)
        output_path = filename +ext + ".huff"
        mapping_path = filename + "_mapping.json"

        with open(self.path, 'rb') as file:
            data = file.read()

        freq = self.make_frequency_dict(data)
        heap = self.build_heap(freq)
        root = self.merge_nodes(heap)
        self.make_codes(root)

        # convert encoded text
        encoded_text = self.get_encoded_text(data)
        padded_encoded_text = self.pad_encoded_text(encoded_text)
        byte_array = self.get_byte_array(padded_encoded_text)

        # save compressed data
        with open(output_path, 'wb') as output:
            output.write(byte_array)

        # save mapping to json
        json_mapping = {code: byte for code, byte in self.reverse_mapping.items()}
        with open(mapping_path, 'w') as f:
            json.dump(json_mapping, f)

        return [output_path, mapping_path]