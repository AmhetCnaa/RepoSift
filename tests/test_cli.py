import sys
from unittest.mock import patch

import pytest

from reposift.cli import main


def test_cli_help(capsys):
    with patch.object(sys, 'argv', ['reposift', '--help']):
        with pytest.raises(SystemExit) as e:
            main()
        assert e.value.code == 0
        
    captured = capsys.readouterr()
    assert "reposift" in captured.out
    
def test_cli_json_output(capsys, tmp_path):
    (tmp_path / "test.py").write_text("print('hello')")
    with patch.object(sys, 'argv', ['reposift', str(tmp_path), '--json']):
        main()
        
    captured = capsys.readouterr()
    assert "total_files" in captured.out
    assert "test.py" in captured.out
