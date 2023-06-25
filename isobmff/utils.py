"""
File: isobmff/utils.py

Contains utility functions for the isobmff package
"""
import typing

try:
    import chardet

    def auto_decode(data: bytes) -> str:
        """
        Automatically decode the given byte data to a string using the detected encoding.

        Parameters
        ----------
        data : bytes
            The byte data to decode.

        Returns
        -------
        str
            The decoded string.
        """
        return data.decode(chardet.detect(data)["encoding"])

except:

    def auto_decode(data: bytes) -> str:
        """
        Manually decode the given byte data to a string using the detected encoding.

        Parameters
        ----------
        data : bytes
            The byte data to decode.

        Returns
        -------
        str
            The decoded string.
        """
        if data[0:3] == b"\xef\xbb\xbf":
            return data.decode("utf-8")
        elif data[0:2] == b"\xfe\xff":
            return data.decode("utf-16-be")
        elif data[0:2] == b"\xff\xfe":
            return data.decode("utf-16-le")
        elif data[0:4] == b"\x00\x00\xfe\xff":
            return data.decode("utf-32-be")
        elif data[0:4] == b"\xff\xfe\x00\x00":
            return data.decode("utf-32-le")
        return data.decode()


def iterate_bits(byte_data) -> typing.Generator:
    """
    Iterate over each bit in the given byte data.

    Parameters
    ----------
    byte_data : bytes
        The byte data to iterate over.

    Yields
    ------
    bool
        The next bit in the byte data.
    """
    for byte in byte_data:
        for i in range(8):
            yield bool((byte >> (7 - i)) & 1 == 1)


def iso639_2T_to_chars(data: bytes) -> str:
    """
    Convert ISO 639-2T language code to ASCII characters.

    Parameters
    ----------
    data : bytes
        The byte data representing the ISO 639-2T language code.

    Returns
    -------
    str
        The ASCII characters representing the language code.
    """
    # Unpack the two bytes into a 16-bit integer
    code = (data[0] << 8) | data[1]

    # Extract the three 5-bit integers
    char1 = (code >> 10) & 0x1F
    char2 = (code >> 5) & 0x1F
    char3 = code & 0x1F

    # Convert the packed values to ASCII characters
    return chr(char1 + 0x60) + chr(char2 + 0x60) + chr(char3 + 0x60)
