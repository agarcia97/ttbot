# Palm Beach County Golf Tee-Time Booking

This project automates booking tee times on Palm Beach County’s golf website using Python and Selenium. It simulates human-like interactions (typing, mouse movement) to help avoid detection.

## Features
- Customize tee times, number of players, dates, etc. before running.
- Uses undetected_chromedriver for stealth web automation.
- Randomizes mouse movements, keystrokes, and user agents.

## Getting Started
1. **Install Dependencies**
   ```
   pip install undetected_chromedriver selenium selenium_stealth pyautogui
   ```
   If on macOS:
   ```
   brew install git-lfs git-filter-repo git-lfs
   brew install git-lfs
   git lfs install
   ```

2. **Edit Configuration**
   Open the script and adjust:
   ```
   possible_tee_times = ["9:27am", "9:36am", "9:45am", "9:54am"]
   login_email = "your_email@example.com"
   login_password = "your_password"
   booking_date = "MM-DD-YYYY"
   number_of_players = 2
   number_of_holes = 18
   ```

3. **Run the Script**
   ```
   python book_tee_time.py
   ```

## Future Plans
- Build a simple user interface so you can configure and launch bookings without the command line.
