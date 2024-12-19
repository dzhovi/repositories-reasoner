# File: tests/test_main.py
from src.main import print_hi


def test_print_hi(capsys):
    print_hi("Test")
    captured = capsys.readouterr()
    assert captured.out == "Hi, Test\n"
