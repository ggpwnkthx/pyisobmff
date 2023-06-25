"""
File: isobmff/utils.py

Contains utility functions for the isobmff package
"""


def iterate_chunks_of_bits(data, chunk_size):
    current_index = 0
    current_bits = 0

    while current_index < len(data):
        remaining_bits = 8 - current_bits
        bits_to_take = min(chunk_size, remaining_bits)

        current_byte = data[current_index]
        current_byte >>= remaining_bits - bits_to_take
        current_byte &= (1 << bits_to_take) - 1

        current_bits += bits_to_take
        if current_bits == 8:
            current_index += 1
            current_bits = 0

        yield current_byte

    if current_bits > 0:
        yield current_byte



def iterate_bits(byte_data):
    for byte in byte_data:
        for i in range(8):
            yield bool((byte >> (7 - i)) & 1 == 1)

def iso639_2T_to_chars(data:bytes):
    # Unpack the two bytes into a 16-bit integer
    code = (data[0] << 8) | data[1]
    
    # Extract the three 5-bit integers
    char1 = (code >> 10) & 0x1F
    char2 = (code >> 5) & 0x1F
    char3 = code & 0x1F
    
    # Convert the packed values to ASCII characters
    return chr(char1 + 0x60) + chr(char2 + 0x60) + chr(char3 + 0x60)