import os
import time
import logging
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def setup_logging(log_name='tra_cuu_hoadon.log'):
    """Cấu hình ghi nhật ký (log)"""
    log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), log_name)
    logging.basicConfig(
      level=logging.INFO,
      format='%(asctime)s - %(levelname)s - %(message)s',
      handlers=[
        logging.FileHandler(log_path, encoding='utf-8'),
        logging.StreamHandler()
      ]
    )


def open_chrome():
  """Mở trình duyệt chrome và cấu hình thư mục lưu PDF"""
  download_dir = os.path.dirname(os.path.abspath(__file__))  

  chrome_options = webdriver.ChromeOptions()
  prefs = {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "directory_upgrade": True,
    "plugins.always_open_pdf_externally": True  # không mở PDF mà tải về
  }
  chrome_options.add_experimental_option("prefs", prefs)

  driver = webdriver.Chrome(options=chrome_options)
  driver.get("https://www.meinvoice.vn/tra-cuu")
  logging.info("Đã mở trình duyệt và truy cập trang tra cứu hóa đơn.")
  return driver


def xu_ly_tra_cuu(driver, ma_tra_cuu):
  """xử lý mã tra cứu hóa đơn"""
  xpath = '//*[@id="txtCode"]'
  element_input = driver.find_element(By.XPATH, xpath)
  element_input.clear()
  element_input.send_keys(ma_tra_cuu)
  logging.info(f"Đã nhập mã tra cứu: {ma_tra_cuu}")


def xu_ly_tim_kiem_hoa_don(driver):
  """ xử lý tìm kiếm hóa đơn và xử lý lỗi nếu có"""
  btn_xpath = '//*[@id="btnSearchInvoice"]'
  WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, btn_xpath))
  ).click()
  logging.info("Đã nhấn nút Tìm kiếm.")

 
    
def kiem_tra_ket_qua_tra_cuu(driver):
  """Kiểm tra kết quả tra cứu"""
  try:
    error_xpath = '//*[@id="popup-invoicnotexist-content"]/div'
    error_element = WebDriverWait(driver, 5).until(
      EC.visibility_of_element_located((By.XPATH, error_xpath))
    )
    logging.warning(f"Lỗi tra cứu: {error_element.text}")
    return False
  except:
    logging.info("Không có lỗi tra cứu, tiếp tục.")
    return True


def xu_ly_tai_hoa_don(driver):
  """xử lý tải hóa đơn"""
  try:
    # Chờ overlay biến mất
    try:
      WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CLASS_NAME, "m-mask-modal"))
      )
    except Exception as e:
      logging.warning(f"Overlay không biến mất sau 10s, thử tiếp tục... {e}")

    # Bước 1: Click nút tải hóa đơn (nút tổng)
    btn_download_xpath = '//*[@id="popup-content-container"]/div[1]/div[2]/div[12]/div'
    btn_download = WebDriverWait(driver, 10).until(
      EC.element_to_be_clickable((By.XPATH, btn_download_xpath))
    )
    btn_download.click()
    
    logging.info("Đã nhấn nút tải hóa đơn.")

    # Bước 2: Chờ popup hiện nút tải PDF
    btn_pdf_xpath = '//*[@id="popup-content-container"]/div[1]/div[2]/div[12]/div/div/div[1]'
    WebDriverWait(driver, 10).until(
      EC.element_to_be_clickable((By.XPATH, btn_pdf_xpath))
    )

    # Bước 3: Click nút tải PDF
    btn_pdf = driver.find_element(By.XPATH, btn_pdf_xpath)
    btn_pdf.click()
    time.sleep(2)
    logging.info("Đã nhấn nút tải PDF.")
  except Exception as e:
    logging.error(f"Lỗi khi tải hóa đơn: {e}")
    raise


def xu_ly_dong_trinh_duyet(driver):
  driver.quit()
  logging.info("Trình duyệt đã đóng. Bye Bye!!!")

def main():
  """Handle tra cứu hóa đơn
  1. Access the electronic invoice lookup website of meinvoice.vn.
  Open the browser; configure Selenium to download files

  2. Enter the invoice lookup code into the corresponding input field.
  Function to input the lookup code

  3. Perform the search action
  Function to execute the search

  4. Handle the search results, including identifying the invoice and providing download options.
  Result handling function: success or failure (if-else)

  5. Download the electronic invoice (in PDF format) to the local system.
  Download the invoice: successful lookup"""


  setup_logging() 
  # Đọc tất cả các mã tra cứu từ file misa.xlsx
  misa_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'misa.xlsx')
  try:
    df = pd.read_excel(misa_path)
    ma_tra_cuus = df.iloc[:, 0].dropna().tolist()  # Lấy cột đầu tiên
  except Exception as e:
    logging.error(f"Không đọc được file misa.xlsx: {e}")
    return

  driver = open_chrome()
  for ma_tra_cuu in ma_tra_cuus:
    try:
      driver.get("https://www.meinvoice.vn/tra-cuu")  # Load lại trang
      xu_ly_tra_cuu(driver, ma_tra_cuu)
      xu_ly_tim_kiem_hoa_don(driver)
      if kiem_tra_ket_qua_tra_cuu(driver):
        xu_ly_tai_hoa_don(driver)
        time.sleep(3)
    except Exception as e:
        logging.error(f"Lỗi không xác định với mã {ma_tra_cuu}: {e}")

  xu_ly_dong_trinh_duyet(driver)

main()    