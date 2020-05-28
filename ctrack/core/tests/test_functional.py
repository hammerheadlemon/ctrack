def test_can_get_homepage(browser):
    browser.get("http://localhost:8000")
    assert "ctrack" in browser.title
