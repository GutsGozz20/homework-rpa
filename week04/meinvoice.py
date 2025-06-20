from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def open_chrome():
  """Mở trình duyệt chrome"""
  driver = webdriver.Chrome()
  driver.get('https://www.meinvoice.vn/tra-cuu')
  return driver

def xu_ly_tra_cuu(driver):
  """xử lý nhập mã tra cứu"""
  xpath = '//*[@id="txtCode"]' 
  element_input = driver.find_element(By.XPATH, xpath)
  str_hoa_don = 'B1HEIRR8N0WP'
  element_input.send_keys(str_hoa_don)
  print()

def xu_ly_tim_kiem_hoa_don(driver):
  """ xử lý tìm kiếm hóa đơn"""
  btn_submit_xpath = '//*[@id="btnSearchInvoice"]'
  btn_submit = driver.find_element(By.XPATH, btn_submit_xpath)
  btn_submit.click()

 
def xu_ly_tai_hoa_don(driver):
  """xử lý tải hóa đơn"""
  # Chờ overlay biến mất
  try:
    WebDriverWait(driver, 10).until(
      EC.invisibility_of_element_located((By.CLASS_NAME, "m-mask-modal"))
    )
  except:
    print("Overlay không biến mất sau 10s, thử tiếp tục...")

  # Bước 1: Click nút tải hóa đơn (nút tổng)
  btn_download_xpath = '//*[@id="popup-content-container"]/div[1]/div[2]/div[12]/div'
  btn_download = driver.find_element(By.XPATH, btn_download_xpath)
  btn_download.click()

  # Bước 2: Chờ popup hiện nút tải PDF
  btn_pdf_xpath = '//*[@id="popup-content-container"]/div[1]/div[2]/div[12]/div/div/div[1]'
  WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, btn_pdf_xpath))
  )

  # Bước 3: Click nút tải PDF
  btn_pdf = driver.find_element(By.XPATH, btn_pdf_xpath)
  btn_pdf.click()
  
def xu_ly_dong_trinh_duyet(driver):
  driver.quit()
  print("Trình duyệt đã đóng. Bye Bye!!!")

def main():
  """Handle tra cứu hóa đơn"""
  driver = open_chrome()

  xu_ly_tra_cuu(driver)
  
  xu_ly_tim_kiem_hoa_don(driver)

  xu_ly_tai_hoa_don(driver)
  time.sleep(5)  # chờ tải về

  xu_ly_dong_trinh_duyet(driver)

main()