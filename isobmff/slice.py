"""
File: isobmff/slice.py

Contains the Slice class, which represents a slice of a binary file
"""
import struct
import typing


class Slice:
    """
    This class provides a way to work with a specific portion of a binary file,
    such as an ISO Base Media File Format (ISOBMFF) file. It supports reading,
    decoding, and unpacking data from the file, as well as creating sub-slices
    and iterating over the data in the slice.

    One of the key features of this class is that it allows working with large
    binary files without loading the entire file into memory. This is especially
    useful when dealing with large media files, which can be several gigabytes
    in size. By using this class, you can read, decode, and unpack data from
    the file on an as-needed basis, reducing memory usage significantly.

    Parameters
    ----------
    handler : typing.BinaryIO
        The binary file handler.
    start : int, optional
        The start position of the slice in the file, by default 0
    stop : int, optional
        The stop position of the slice in the file, by default None
    step : int, optional
        The step size for iterating over the slice, by default None
    decode : str, optional
        The encoding to use when decoding the slice, by default None
    unpack : Union[str, bytes], optional
        The format string for struct.unpack to use when unpacking the slice, by default None

    Attributes
    ----------
    handler : typing.BinaryIO
        The binary file handler.
    start : int
        The start position of the slice in the file.
    stop : int
        The stop position of the slice in the file.
    step : int
        The step size for iterating over the slice
    _decode : tuple or dict
        The arguments for the decode method.
    _unpack : str
        The format string for struct.unpack.

    Examples
    --------
    >>> with open('file.bin', 'rb') as f:
    ...     s = Slice(f, 0, 10)
    ...     print(s.read())
    b'\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09'

    Notes
    -----
    The `decode` and `unpack` parameters are used to specify the formats for
    the `decode` and `unpack` methods, respectively. If these parameters are
    not specified, the corresponding methods will use their own parameters.
    """

    def __init__(
        self,
        handler: typing.BinaryIO,
        start: int = 0,
        stop: int = None,
        step: int = None,
        decode: str = None,
        unpack: typing.Union[str, bytes] = None,
    ):
        self.handler = handler
        self.start = start
        self.stop = stop
        self.step = step
        self._decode = (decode) if isinstance(decode, str) else decode
        self._unpack = unpack

    def read(self, start: int = None, stop: int = None) -> bytes:
        """
        Read data from the slice.

        Parameters
        ----------
        start : int, optional
            The start position to read from within the slice, by default None
        stop : int, optional
            The stop position to read up to within the slice, by default None

        Returns
        -------
        bytes
            The read data from the slice.

        Raises
        ------
        EOFError
            If the end of the file is reached.

        """
        if start:
            start = self.start + start
        else:
            start = self.start
        if stop:
            stop = self.start + stop
        else:
            if self.stop:
                stop = self.stop
            else:
                stop = -1

        if self.handler.tell() != start:
            self.handler.seek(start)
        data = self.handler.read((stop - start) if stop != -1 else -1)
        if not data:
            raise EOFError("Reached the end of the file.")
        return data

    def decode(self, *args, **kwargs) -> str:
        """
        Decode the slice using the specified encoding.

        Parameters
        ----------
        *args
            Positional arguments for the decode method.
        **kwargs
            Keyword arguments for the decode method.

        Returns
        -------
        str
            The decoded string.

        """
        if not len(args) and isinstance(self._decode, tuple):
            args = self._decode
        if not len(kwargs) and isinstance(self._decode, dict):
            kwargs = self._decode
        return self.read().decode(*args, **kwargs)

    def unpack(self, __format: typing.Union[str, bytes] = None):
        """
        Unpack the slice using the specified format string.

        Parameters
        ----------
        __format : Union[str, bytes], optional
            The format string for struct.unpack, by default None

        Returns
        -------
        tuple
            The unpacked values.

        """
        if not __format:
            __format = self._unpack
        return struct.unpack(__format, self.read())

    def iter_unpack(self, __format: typing.Union[str, bytes] = None):
        """
        Iterate over the slice, unpacking values based on the specified format string.

        Parameters
        ----------
        __format : Union[str, bytes], optional
            The format string for struct.iter_unpack, by default None

        Returns
        -------
        iterator
            An iterator of unpacked values.

        """
        if not __format:
            __format = self._unpack
        return struct.iter_unpack(__format, self.read())

    def subslice(self, start: int, stop: int = None, **kwargs):
        """
        Create a sub-slice of the current slice.

        Parameters
        ----------
        start : int
            The start position of the sub-slice.
        stop : int, optional
            The stop position of the sub-slice, by default None
        **kwargs
            Additional keyword arguments to pass to the sub-slice.

        Returns
        -------
        Slice
            The created sub-slice.

        """
        return Slice(
            self.handler,
            self.start + start,
            self.start + stop if stop else None,
            **kwargs,
        )

    def __repr__(self):
        return f"<{self.__class__.__name__}(start={self.start},stop={self.stop},step={self.step})>"


class CachedIterator:
    def __init__(self, slice: Slice, item_finder: typing.Callable, count:int = None):
        self.slice = slice
        self.item_finder = item_finder
        self.__cache = []
        self.__cache_iter = iter(self.__cache)
        self.__count = count
        self.__stop = False

    def __iter__(self):
        return self

    def __next__(self):
        """
        Uses the item_finder function to determine the what the next item
        object. The object must have a size property to determing the
        poistion of the item following it.

        Returns
        -------
        Any
            The next item in the slice.

        Raises
        ------
        StopIteration
            If there are no more items to get.

        """
        if not self.__stop:
            try:
                item = self.item_finder(self)
                if item.size is None or item.size == 0:
                    raise EOFError("Reached the end of the file.")
            except EOFError:
                self.__stop = True
                raise StopIteration

            self.slice = self.slice.subslice(item.size)
            self.__cache.append(item)
            if self.__count == len(self.__cache):
                self.__stop = True
            return item
        return next(self.__cache_iter)

    def __getitem__(self, index: int):
        if index >= 0:
            if index < len(self.__cache):
                return self.__cache[index]

            for _ in range(index - len(self.__cache) + 1):
                b = next(self)

            return b
        else:
            while not self.__stop:
                try:
                    next(self)
                except StopIteration:
                    break
            return self.__cache[index]