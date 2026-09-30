import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        help="Браузер для запуска тестов: chrome или firefox",
    )
    parser.addoption(
        "--url",
        action="store",
        default="https://www.saucedemo.com/",
        help="Базовый URL приложения",
    )


@pytest.fixture(scope="session")
def base_url(request):
    return request.config.getoption("--url")


@pytest.fixture
def driver(request):
    browser_name = request.config.getoption("--browser").lower()

    if browser_name == "chrome":
        options = ChromeOptions()
        options.add_argument("--start-maximized")
        driver_instance = webdriver.Chrome(options=options)
    elif browser_name == "firefox":
        options = FirefoxOptions()
        driver_instance = webdriver.Firefox(options=options)
        driver_instance.maximize_window()
    else:
        raise pytest.UsageError(
            f"Браузер '{browser_name}' не поддерживается. Доступны: chrome, firefox"
        )

    driver_instance.implicitly_wait(10)
    yield driver_instance
    driver_instance.quit()
