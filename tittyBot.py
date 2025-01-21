import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium_stealth import stealth
import pyautogui
import random
import time

# Configuration
possible_tee_times = ["9:27am", "9:36am", "9:45am", "9:54am"]
login_email = "ahgarcia@protonmail.com"
login_password = "golf1234"
booking_date = "05-24-2024"
number_of_players = 2  # Set players here
number_of_holes = 18  # Set holes here
user_agents = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'
]

# Start WebDriver
options = uc.ChromeOptions()
options.add_argument('--window-size=1920,1080')
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-notifications')
options.add_argument('--blink-settings=imagesEnabled=false')
options.add_argument('--start-maximized')
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument(f'--user-agent={random.choice(user_agents)}')
options.add_argument('--accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
options.add_argument('--accept-language=en-US,en;q=0.5')
options.add_argument('--referer=https://foreupsoftware.com/')
options.add_argument('--disable-web-security')

# Start undetected_chromedriver
driver = uc.Chrome(options=options)
driver.implicitly_wait(10)

# Apply stealth
stealth(driver,
    languages=["en-US", "en"],
    vendor="Google Inc.",
    platform="Win32",
    webgl_vendor="Intel Inc.",
    renderer="Intel Iris OpenGL Engine",
    fix_hairline=True,
)

# Go undercover
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})")
driver.execute_script("Object.defineProperty(navigator, 'platform', {get: () => 'Win32'})")

# Change geolocation
driver.execute_cdp_cmd("Page.setGeolocationOverride", {
    "latitude": random.uniform(25.0, 49.0),
    "longitude": random.uniform(-125.0, -66.9),
    "accuracy": 100
})

def human_like_typing(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.1, 0.3))

def human_like_mouse_move(element):
    location = element.location
    size = element.size
    x, y = location['x'] + size['width'] / 2, location['y'] + size['height'] / 2
    pyautogui.moveTo(x + random.uniform(-5, 5), y + random.uniform(-5, 5), random.uniform(0.5, 2))

def click_element(driver, element):
    try:
        human_like_mouse_move(element)
        pyautogui.click()
        print("Clicked using pyautogui.")
    except Exception as e:
        print(f"pyautogui click failed: {e}")
    for _ in range(3):
        try:
            element.click()
            print("Clicked using direct click.")
            break
        except Exception as e:
            print(f"Attempt failed: {e}")
            time.sleep(random.uniform(0.5, 2))

def save_screenshot_and_source(driver, name):
    driver.save_screenshot(f'{name}.png')
    with open(f'{name}.html', 'w') as f:
        f.write(driver.page_source)

def random_interaction(driver):
    elements = driver.find_elements(By.CSS_SELECTOR, 'a, button, input')
    if elements:
        element = random.choice(elements)
        human_like_mouse_move(element)
        pyautogui.click()

def random_delay():
    time.sleep(random.uniform(0.5, 2))

try:
    driver.get("https://foreupsoftware.com/index.php/booking/21263/7480#/teetimes")
    save_screenshot_and_source(driver, 'initial_load')

    random_interaction(driver)
    random_delay()

    try:
        fp_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Frequent Player Card Tee Times')]"))
        )
        click_element(driver, fp_button)
        print("Clicked Frequent Player Card Tee Times button.")
    except Exception as e:
        save_screenshot_and_source(driver, 'fp_button_exception')
        print(f"Exception while clicking Frequent Player Card Tee Times button: {e}")
        raise

    random_interaction(driver)
    random_delay()

    try:
        login_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Log In')]"))
        )
        click_element(driver, login_button)
        print("Clicked Log In button.")
    except Exception as e:
        save_screenshot_and_source(driver, 'login_button_exception')
        print(f"Exception while clicking Log In button: {e}")
        raise

    email_input = driver.find_element(By.ID, "login_email")
    password_input = driver.find_element(By.ID, "login_password")
    login_button = driver.find_element(By.CLASS_NAME, "btn.btn-primary.login.col-xs-12.col-md-2")
    
    human_like_typing(email_input, login_email)
    human_like_typing(password_input, login_password)
    click_element(driver, login_button)
    print("Logged in successfully.")
    save_screenshot_and_source(driver, 'after_login')

    random_interaction(driver)
    random_delay()

    date_selector = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.ID, "date-field"))
    )
    driver.execute_script("arguments[0].value = ''", date_selector)
    human_like_typing(date_selector, booking_date)
    date_selector.send_keys(Keys.ENTER)
    print(f"Entered booking date: {booking_date}")
    save_screenshot_and_source(driver, 'after_date_entry')

    random_interaction(driver)
    random_delay()

    WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "time.time-tile"))
    )

    time_slots = driver.find_elements(By.CLASS_NAME, "time.time-tile")

    for slot in time_slots:
        slot_time = slot.find_element(By.CLASS_NAME, "booking-start-time-label").text.strip()
        if slot_time in possible_tee_times:
            player_span = slot.find_element(By.CLASS_NAME, "booking-slot-players.js-booking-slot-players span")
            player_count = int(player_span.text.strip())
            if player_count >= number_of_players:
                click_element(driver, slot)
                print(f"Booked tee time at {slot_time} for {number_of_players} or more players.")
                save_screenshot_and_source(driver, f'booked_{slot_time.replace(":", "")}')

                WebDriverWait(driver, 20).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, "modal-content.time-details"))
                )

                holes_button = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class, 'js-booking-holes')]//a[@data-value='{number_of_holes}']"))
                )
                click_element(driver, holes_button)
                print(f"Selected {number_of_holes} holes.")
                save_screenshot_and_source(driver, 'after_selecting_holes')

                players_button = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class, 'js-booking-players')]//a[@data-value='{number_of_players}']"))
                )
                click_element(driver, players_button)
                print(f"Selected {number_of_players} players.")
                save_screenshot_and_source(driver, 'after_selecting_players')

                book_time_button = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Book Time')]"))
                )

                click_element(driver, book_time_button)
                save_screenshot_and_source(driver, 'after_clicking_book_time')

                continue_button = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Continue')]"))
                )

                click_element(driver, continue_button)
                print("Clicked 'Continue' button.")
                save_screenshot_and_source(driver, 'after_clicking_continue')

                final_book_time_button = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Book Time')]"))
                )

                click_element(driver, final_book_time_button)
                print("Clicked final 'Book Time' button.")
                save_screenshot_and_source(driver, 'final_book_time_button')

                time.sleep(2)
                save_screenshot_and_source(driver, 'final_state_after_booking')

                break

finally:
    save_screenshot_and_source(driver, 'final_state')
    print("Booking script completed. Inspect the browser window.")
    driver.quit()
