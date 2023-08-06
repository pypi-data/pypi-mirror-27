import zlib
import os

from moonreader_tools.conf import NOTE_EXTENSION


class FileReader(object):
    """
    A mixin class able to read simple and gzipped
    files
    """

    def read_file(self, fname) -> str:
        assert os.path.exists(fname), 'File {} does not exist'.format(fname)
        assert fname.endswith(NOTE_EXTENSION)

        book_extension = fname.split(".")[-2]
        if book_extension == "zip":
            book_extension = fname.split(".")[-3]
        with open(fname, 'rb') as book_notes_f:
            return self._read_file_obj(book_notes_f, book_extension)

    @classmethod
    def _read_file_obj(cls, flike_obj, ext):
        """Creates note object from file-like object"""
        content = flike_obj.read()
        if cls._is_zipped(content):
            content = cls._read_zipped_content(content)
        else:
            content = content
        if isinstance(content, bytes):
            content = content.decode('utf-8')
        return content

    @classmethod
    def _read_zipped_content(cls, str_content, file_type="fb2"):
        """Creates note object from zip-compressed string"""
        if not cls._is_zipped:
            raise ValueError("Given string is not zipped.")
        unpacked_str = cls._unpack_str(str_content)
        return unpacked_str

    @staticmethod
    def _unpack_str(zipped_str) -> str:
        """Decompresses zipped string"""
        return zlib.decompress(zipped_str)

    @staticmethod
    def _is_zipped(str_text: str) -> bool:
        """Checks whether given sequence is compressed with zip"""
        if len(str_text) < 2:
            return False
        return (str_text[0], str_text[1]) == (int('78', base=16), int('9c', base=16))
