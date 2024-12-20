import pytest
import re
import subprocess

def test_print_help():
    result = subprocess.run(['python', 'util.py', '-h'], capture_output=True, text=True)
    assert "Usage: ./util.py [OPTION]... [FILE]" in result.stdout

def test_first_lines():
    result = subprocess.run(['python', 'util.py', '--first', '10', 'test_0.log'], capture_output=True, text=True)
    lines = result.stdout.splitlines()
    assert len(lines) == 10

def test_last_lines():
    result = subprocess.run(['python', 'util.py', '-l', '5', 'test_1.log'], capture_output=True, text=True)
    lines = result.stdout.splitlines()
    assert len(lines) == 5

def test_timestamps():
    result = subprocess.run(['python', 'util.py', '--timestamps', 'test_2.log'], capture_output=True, text=True)
    lines = result.stdout.splitlines()
    assert all(re.search(r"\b([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]\b", line) for line in lines)

def test_ipv4():
    result = subprocess.run(['python', 'util.py', '--ipv4', 'test_3.log'], capture_output=True, text=True)
    lines = result.stdout.splitlines()
    assert all(re.search(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', line) for line in lines)

def test_ipv6():
    result = subprocess.run(['python', 'util.py', '--ipv6', 'test_4.log'], capture_output=True, text=True)
    lines = result.stdout.splitlines()
    assert all(re.search(r'\b(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b', line) for line in lines)

def test_ipv4_last_50():
    result = subprocess.run(['python', 'util.py', '--ipv4', '--last', '50', 'test_5.log'], capture_output=True, text=True)
    lines = result.stdout.splitlines()
    assert len(lines) <= 50 and all(re.search(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', line) for line in lines)
