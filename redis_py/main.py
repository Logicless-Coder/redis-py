from collections.abc import Iterator
from rich import print


class RESP:
    CRLF = "\r\n"
    INTEGER_BYTE = ":"
    SIMPLE_STRING_BYTE = "+"
    SIMPLE_ERROR_BYTE = "-"
    BULK_STRING_BYTE = "$"
    ARRAY_BYTE = "*"

    def deserialize(self, raw: str) -> str | int | None | list[str | int | None]:
        raw_items = raw.split(self.CRLF).__iter__()

        for item in raw_items:
            return self._deserialize_item(item, raw_items)

    def _deserialize_item(
        self, item: str, items: Iterator[str]
    ) -> str | int | None | list[str | int | None]:
        if item.startswith(self.SIMPLE_STRING_BYTE):
            return item.removeprefix(self.SIMPLE_STRING_BYTE)
        elif item.startswith(self.SIMPLE_ERROR_BYTE):
            return item.removeprefix(self.SIMPLE_ERROR_BYTE)
        elif item.startswith(self.INTEGER_BYTE):
            return int(item.removeprefix(self.INTEGER_BYTE))
        elif item.startswith(self.BULK_STRING_BYTE):
            length = int(item.removeprefix(self.BULK_STRING_BYTE))
            next_item = next(items)
            if length < len(next_item):
                return None
            else:
                return next_item[:length]
        elif item.startswith(self.ARRAY_BYTE):
            length = int(item.removeprefix(self.ARRAY_BYTE))
            print(f"{length=}")
            array = []
            for _ in range(length):
                next_item = next(items)
                print(f"{next_item=}")
                x = self._deserialize_item(next_item, items)
                print(f"{x=}")
                array.append(x)
            return array
        else:
            raise NotImplementedError
