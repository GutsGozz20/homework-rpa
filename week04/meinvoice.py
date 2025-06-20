from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import logging

# Thiết lập logging
log_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tra_cuu_hoadon.log')
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


def xu_ly_tra_cuu(driver):
  """xử lý nhập mã tra cứu"""
  xpath = '//*[@id="txtCode"]' 
  element_input = driver.find_element(By.XPATH, xpath)
  str_hoa_don = 'B1HEIRR8N0WP'
  # str_hoa_don = 'B1HEIRR8N0WP1'
  element_input.send_keys(str_hoa_don)
  logging.info(f"Đã nhập mã tra cứu: {str_hoa_don}")


def xu_ly_tim_kiem_hoa_don(driver):
  """ xử lý tìm kiếm hóa đơn và xử lý lỗi nếu có"""
  btn_xpath = '//*[@id="btnSearchInvoice"]'
  WebDriverWait(driver, 10).until(
      EC.element_to_be_clickable((By.XPATH, btn_xpath))
  ).click()
  logging.info("Đã nhấn nút Tìm kiếm.")

  # Đợi kết quả hoặc thông báo lỗi
  time.sleep(2)
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
        logging.info("Đã nhấn nút tải PDF.")
    except Exception as e:
        logging.error(f"Lỗi khi tải hóa đơn: {e}")
        raise

def xu_ly_dong_trinh_duyet(driver):
  driver.quit()
  logging.info("Trình duyệt đã đóng. Bye Bye!!!")

def main():
  """Handle tra cứu hóa đơn"""
  driver = open_chrome()
  try:
    xu_ly_tra_cuu(driver)
    if xu_ly_tim_kiem_hoa_don(driver):
      xu_ly_tai_hoa_don(driver)
      time.sleep(3)
  except Exception as e:
    logging.error(f"Lỗi không xác định: {e}")
  finally:
    xu_ly_dong_trinh_duyet(driver)

main()


    # 1. Truy cập trang web tra cứu hóa đơn điện tử của meinvoice.vn.
    #    Mở trình duyệt; cấu hình download file selenium

    # 2. Nhập mã tra cứu hóa đơn vào trường tương ứng.
    #    hàm nhập mã tra cứu

    # 3. Thực hiện hành động tìm kiếm
    #    hàm thực hiện tìm kiếm

    # 4. Xử lý kết quả tìm kiếm, bao gồm việc nhận diện hóa đơn và tùy chọn tải xuống.
    #    hàm Xử lý kết quả: thành công hoặc thất bại (if else)

    # 5. Tải hóa đơn điện tử (dạng PDF) về hệ thống cục bộ.
    #    Tải hóa đơn: tra cứu thành công