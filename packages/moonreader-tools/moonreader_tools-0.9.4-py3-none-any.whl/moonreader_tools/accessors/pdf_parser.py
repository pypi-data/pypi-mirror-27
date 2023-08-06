import os

from moonreader_tools.books import Book
from moonreader_tools.conf import NOTE_EXTENSION, STAT_EXTENSION
from moonreader_tools.accessors.base_accessor import BaseBookParser
from moonreader_tools.accessors.stat_accessor import StatsAccessor
from moonreader_tools.accessors.pdf_accessor import PDFFileNoteReader


class PDFParser(BaseBookParser):

    _SUPPORTED_EXTENSIONS = ('.pdf', )

    def __init__(self,
                 stat_accessor=StatsAccessor(),
                 note_reader=PDFFileNoteReader()):
        self.stat_accessor = stat_accessor
        self.note_reader = note_reader

    def persist_book(self, book: Book,
                     ext: str,
                     output_dir: str):
        """
        """
        pass

    def read_book(self,
                  directory: str,
                  book_name: str) -> Book:
        """
        Attempts to read the book
        in the given dir with the specified name

        :param book_name: name of the book file together
        with the extension (e.g. my_dear_book.fb2)
        """
        if not book_name.endswith(self._SUPPORTED_EXTENSIONS):
            raise ValueError('Book %s is not supported by parser. '
                             'Supported params are %s',
                             book_name, ", ".join(self._SUPPORTED_EXTENSIONS))
        notes_path = os.path.join(directory, book_name + NOTE_EXTENSION)
        stats_path = os.path.join(directory, book_name + STAT_EXTENSION)

        stats = self.stat_accessor.stats_from_file(stats_path)
        notes = self.note_reader.notes_from_file(notes_path)
        return Book(book_name, stats=stats, notes=notes)
