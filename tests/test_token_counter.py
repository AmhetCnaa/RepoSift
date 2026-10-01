from reposift.token_counter import count_file_tokens, count_tokens


def test_count_tokens():
    text = "Hello, world! This is a test."
    tokens = count_tokens(text)
    assert tokens > 0
    assert tokens < 20

def test_count_file_tokens(tmp_path):
    f = tmp_path / "test.txt"
    f.write_text("Hello, world!")
    tokens = count_file_tokens(f)
    assert tokens > 0
