# Product Price Monitor

[![forthebadge](http://forthebadge.com/images/badges/made-with-python.svg)](http://forthebadge.com)

A Python program that allows you to monitor the prices of products from various online stores and receive real-time notifications on discounts. The program provides a user-friendly GUI where you can add product URLs, set the monitoring interval, and specify a discount percentage. 

## Key Features

- **Real-time Monitoring**: Continuously tracks the prices of the specified products and provides immediate updates on any changes.
- **Discord Notifications**: Receive notifications through Discord webhooks, ensuring you stay updated on your chosen platform.
- **Import Product URLs**: Easily import a list of product URLs from a TXT file, simplifying the process of adding multiple products for monitoring.
- **Discount Alerts**: Set a discount percentage and receive alerts when a product's price drops below the specified percentage.

## Usage

1. Clone the repository or download the code to your local machine.
2. Install the required libraries using pip: `pip install requests beautifulsoup4 tkinter`.
3. Run the Python script: `python discountdedect.py`.
4. Enter your Discord webhook URL in the designated field to receive notifications.
5. Add product URLs manually or import them from a TXT file.
6. Set the monitoring interval in minutes to determine how often the program checks for price changes.
7. Optionally, enter a discount percentage to be alerted when a product's price drops below the specified percentage.
8. Click "Start Monitoring" to begin tracking the product prices.

Stay informed about price changes and discounts with this Product Price Monitor, making online shopping smarter and more efficient!

## Warning
This program is only working for Trendyol for now. I want to update it more to be used with another sites.
