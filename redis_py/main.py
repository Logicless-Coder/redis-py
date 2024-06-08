from rich import print


class RESP:
    CRLF = "\r\n"
    INTEGER_BYTE = ":"
    SIMPLE_STRING_BYTE = "+"
    SIMPLE_ERROR_BYTE = "-"
    BULK_STRING_BYTE = "$"
    ARRAY_BYTE = "*"

    NULL_BULK_STRING = "$-1\r\n"

    def deserialize(self, raw: str) -> str | int | None | list[str | int | None]:
        if raw == self.NULL_BULK_STRING:
            return None

        if raw.startswith(self.INTEGER_BYTE):
            return self._deserialize_integer(raw)
        elif raw.startswith(self.SIMPLE_STRING_BYTE):
            return self._deserialize_simple_string(raw)
        elif raw.startswith(self.SIMPLE_ERROR_BYTE):
            return self._deserialize_simple_error(raw)
        elif raw.startswith(self.BULK_STRING_BYTE):
            return self._deserialize_bulk_string(raw)
        elif raw.startswith(self.ARRAY_BYTE):
            return self._deserialize_array(raw)

    def _deserialize_integer(self, raw: str) -> int:
        print("trying:", raw)
        try:
            return int(raw.removeprefix(self.INTEGER_BYTE).removesuffix(self.CRLF))
        except Exception as e:
            return 0

    def _deserialize_simple_string(self, raw: str) -> str:
        return raw.removeprefix(self.SIMPLE_STRING_BYTE).removesuffix(self.CRLF)

    def _deserialize_simple_error(self, raw: str) -> str:
        return raw.removeprefix(self.SIMPLE_ERROR_BYTE).removesuffix(self.CRLF)

    def _deserialize_bulk_string(self, raw: str) -> str:
        raw = raw.removeprefix(self.BULK_STRING_BYTE).removesuffix(self.CRLF)

        raw_parts = raw.split(self.CRLF, maxsplit=1)
        length = int(raw_parts[0])

        return raw_parts[1][:length]

    def _deserialize_array(self, raw: str) -> list[str | int | None]:
        raw = raw.removeprefix(self.ARRAY_BYTE).removesuffix(self.CRLF)

        raw_parts = raw.split(self.CRLF, maxsplit=1)
        length, raw = int(raw_parts[0]), raw_parts[1]

        array = []
        while len(raw) > 0:
            typ = raw[0]
            end = raw.find("\r\n")
            item = None
            if typ == self.INTEGER_BYTE:
                item = self._deserialize_integer(raw[:end])
            elif typ == self.SIMPLE_STRING_BYTE:
                item = self._deserialize_simple_string(raw[:end])
            elif typ == self.SIMPLE_ERROR_BYTE:
                item = self._deserialize_simple_error(raw[:end])
            elif typ == self.BULK_STRING_BYTE:
                end = raw[end + 1 :].find("\r\n")
                item = self._deserialize_bulk_string(raw[:end])
            elif typ == self.ARRAY_BYTE:
                end = raw[end + 1 :].find("\r\n")
                item = self._deserialize_array(raw[:end])

            raw = raw[end + 2:].removeprefix("\r\n")
            print(raw, item)
            array.append(item)

        return array
