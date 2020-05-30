def test_can_get_homepage_for_signing(browser, live_server):
    browser.get(live_server + "/")
    assert "Sign In" in browser.title
