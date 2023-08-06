from .base_accessor import BaseNoteAccessor


class FB2Accessor(BaseNoteAccessor):
    def __init__(self):
        pass

    def note_to_string(self, note):
        """Build string representation used by the e-book reader"""
        result = ""

        # TODO: analyze how to treat not delimeters
        # result += "#\n"
        result += "{}\n".format(self.note_id)
        result += "{}\n".format(self.title)
        result += "{}\n".format(self.path)
        result += "{}\n".format(self.path_lower)

        # Fields with unknown purpose
        result += "{}\n".format(self.last_chapter)
        result += "{}\n".format(self.last_split_index)
        result += "{}\n".format(self.last_position)
        result += "{}\n".format(self.highlight_length)

        result += self._color + "\n"
        result += self._timestamp + "\n"

        result += "\n"
        result += "\n"

        result += self.text + "\n"
        result += "\n".join(self._number_to_binary_list(self.modifier))
        return result
