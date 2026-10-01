from reposift.scanner import is_text_file, load_ignore_patterns, scan_repository


def test_is_text_file(tmp_path):
    text_file = tmp_path / "test.txt"
    text_file.write_text("Hello, world!")
    assert is_text_file(text_file) is True

    bin_file = tmp_path / "test.bin"
    bin_file.write_bytes(b"\x00\x01\x02")
    assert is_text_file(bin_file) is False

def test_load_ignore_patterns(tmp_path):
    gitignore = tmp_path / ".gitignore"
    gitignore.write_text("node_modules/\n*.log\n")
    
    patterns = load_ignore_patterns(tmp_path)
    assert "node_modules/" in patterns
    assert "*.log" in patterns
    # Assert defaults are there
    assert ".git/" in patterns

def test_scan_repository(tmp_path):
    # Create some files
    (tmp_path / "src").mkdir()
    (tmp_path / "src" / "main.py").write_text("print('hello')")
    
    (tmp_path / "node_modules").mkdir()
    (tmp_path / "node_modules" / "test.js").write_text("console.log('hi')")
    
    (tmp_path / "test.log").write_text("error")
    
    # Custom ignore
    (tmp_path / ".gitignore").write_text("*.log\n")
    
    files = scan_repository(tmp_path)
    filenames = [f.name for f in files]
    
    assert "main.py" in filenames
    assert "test.js" not in filenames
    assert "test.log" not in filenames
