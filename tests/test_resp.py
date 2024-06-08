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

        assert isinstance(command, list)
        assert len(command) == 1
        assert command[0] == "ping"

    def test_array_double_string(self):
        raw = "*2\r\n$4\r\necho\r\n$11\r\nhello world\r\n"
        command = self.resp.deserialize(raw)

        assert isinstance(command, list)
        assert len(command) == 2
        assert command[0] == "echo"
        assert command[1] == "hello world"

    def test_array_double_string_2(self):
        raw = "*2\r\n$3\r\nget\r\n$3\r\nkey\r\n"
        command = self.resp.deserialize(raw)

        assert isinstance(command, list)
        assert len(command) == 2
        assert command[0] == "get"
        assert command[1] == "key"


class TestRESPSerialization:
    resp = RESP()

    def test_null_bulk_string(self):
        command = None
        raw = self.resp.serialize(command)

        assert raw == "$-1\r\n"

    def test_simple_string(self):
        command = "OK"
        raw = self.resp.serialize(command)

        assert raw == "+OK\r\n"

    def test_simple_error(self):
        command = "Error message"
        raw = self.resp.serialize(command, error=True)

        assert raw == "-Error message\r\n"

    def test_simple_string_2(self):
        command = "hello world"
        raw = self.resp.serialize(command)

        assert raw == "+hello world\r\n"

    def test_empty_bulk_string(self):
        command = ""
        raw = self.resp.serialize(command, bulk=True)

        assert raw == "$0\r\n\r\n"

    def test_array_single_string(self):
        command = ["ping"]
        raw = self.resp.serialize(command, bulk=True)

        assert raw == "*1\r\n$4\r\nping\r\n"

    def test_array_double_string(self):
        command = ["echo", "hello world"]
        raw = self.resp.serialize(command, bulk=True)

        assert raw == "*2\r\n$4\r\necho\r\n$11\r\nhello world\r\n"

    def test_array_double_string_2(self):
        command = ["get", "key"]
        raw = self.resp.serialize(command, bulk=True)

        assert raw == "*2\r\n$3\r\nget\r\n$3\r\nkey\r\n"
