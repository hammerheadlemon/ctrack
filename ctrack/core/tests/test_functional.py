import pytest
from selenium import webdriver


@pytest.fixture
def browser():
    b = webdriver.Firefox()
    yield b
    b.quit()


def test_can_get_homepage(browser):
    browser.get("http://localhost:8000")
    assert "ctrack" in browser.title
