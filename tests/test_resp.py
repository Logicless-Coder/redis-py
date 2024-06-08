from redis_py.main import RESP


class TestRESPDeserialization:
    resp = RESP()

    def test_null_bulk_string(self):
        raw = "$-1\r\n"
        command = self.resp.deserialize(raw)

        assert command is None

    def test_simple_string(self):
        raw = "+OK\r\n"
        command = self.resp.deserialize(raw)

        assert type(command) is str
        assert command == "OK"

    def test_simple_error(self):
        raw = "-Error message\r\n"
        command = self.resp.deserialize(raw)

        assert type(command) is str
        assert command == "Error message"

    def test_simple_string_2(self):
        raw = "+hello world\r\n"
        command = self.resp.deserialize(raw)

        assert type(command) is str
        assert command == "hello world"

    def test_empty_bulk_string(self):
        raw = "$0\r\n\r\n"
        command = self.resp.deserialize(raw)

        assert type(command) is str
        assert command == ""

    def test_array_single_string(self):
        raw = "*1\r\n$4\r\nping\r\n"
        command = self.resp.deserialize(raw)

        assert type(command) is list[str]
        assert len(command) == 1
        assert command[0] == "ping"
