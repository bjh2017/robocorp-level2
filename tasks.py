from robocorp.tasks import task
from robocorp import browser
import csv

from RPA.HTTP import HTTP
from RPA.PDF import PDF
from RPA.Tables import Tables
from RPA.Archive import Archive

@task
def order_robots_from_RobotSpareBin():
    """
    Orders robots from RobotSpareBin Industries Inc.
    Saves the order HTML receipt as a PDF file.
    Saves the screenshot of the ordered robot.
    Embeds the screenshot of the robot to the PDF receipt.
    Creates ZIP archive of the receipts and the images.
    """
    browser.configure(
        slowmo=100,
    )
    download_oreders_csv_file()
    open_robot_order_website()
    log_in()
    navigate_to_orders_tab()
    fill_order_form_with_csv_data()
    archive_receipts()
    log_out()
    
def open_robot_order_website():
    browser.goto("https://robotsparebinindustries.com/")

def log_in():
    page = browser.page()
    page.fill("#username", "maria")
    page.fill("#password", "thoushallnotpass")
    page.click("button:text('Log in')")

def download_oreders_csv_file():
    http = HTTP()
    http.download(url="https://robotsparebinindustries.com/orders.csv", overwrite=True)

def navigate_to_orders_tab():
    page = browser.page()
    page.click("a:text('Order your robot!')")
    page.click("button:text('OK')")

def fill_and_submit_order_form(order):
    page = browser.page()
    page.select_option("#head", str(order['Head']))
    radio_body_id = "#id-body-" + order['Body']
    page.click(radio_body_id)
    page.fill("input[type='number']", order['Legs'])
    page.fill("#address", order['Address'])
    page.click("#order")

    while True:
        if page.is_visible(".alert.alert-danger"):
            page.click("#order")
        else: 
            break

def fill_order_form_with_csv_data():
    with open("orders.csv", newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        
        for row in reader:
            fill_and_submit_order_form(row)
            screenshot_robot(row['Order number'])
            store_receipt_as_pdf(row['Order number'])
            new_order()
            close_annoying_modal()

def embed_screenshot_to_receipt(screenshot, pdf_file):
    """"""

def close_annoying_modal():
    page = browser.page()
    page.click("button:text('OK')")
    

def new_order():
    page = browser.page()
    page.click("#order-another")
    
def screenshot_robot(order):
    path = "output/orders/order-" + order + ".png"
    page = browser.page()
    page.screenshot(path=path)

def store_receipt_as_pdf(order):
    page = browser.page()
    receipt = page.locator("#receipt").inner_html()

    path = "output/pdf-orders/order-" + order + ".pdf"
    pdf = PDF()
    pdf.html_to_pdf(receipt, path)

def archive_receipts():
    """"""
    lib = Archive()
    lib.archive_folder_with_zip('./output/pdf-orders', 'receipts.zip', recursive=True)
    files = lib.list_archive('receipts.zip')
    for file in files:
        print(file)

def log_out():
    page = browser.page()
    page.click("#logout")