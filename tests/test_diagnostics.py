from chronilog import diagnostics

def test_diagnostics_structure():
    result = diagnostics.run_diagnostics()
    assert isinstance(result, dict)
    assert "log_path" in result
    assert "log_level" in result
    assert "file_writeable" in result
    assert "logger_attached" in result
    assert "errors" in result