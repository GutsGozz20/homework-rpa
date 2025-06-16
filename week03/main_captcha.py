from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from PIL import Image
import pytesseract

# Configure Tesseract path
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def open_chrome():
  """Mở trình duyệt chrome"""
  driver = webdriver.Chrome()
  driver.get('https://www.csgt.vn/tra-cuu-phuong-tien-vi-pham.html')
  return driver

def xu_ly_bien_kiem_soat(driver):
  """xử lý nhập biển số"""
  # Xử lý alert nếu có
  try:
    alert = driver.switch_to.alert
    alert.accept()
  except:
    pass

  xpath = '//*[@id="formBSX"]/div[2]/div[1]/input'
  element_input = driver.find_element(By.XPATH, xpath)
  str_bien_so = '43D146872'
  element_input.send_keys(str_bien_so)
  print()

def xu_ly_loai_phuong_tien(driver):
  """xử lý nhập loại phương tiện"""
  #click vào option loại phương tiện
  xpath_option = '//*[@id="formBSX"]/div[2]/div[2]/select'
  element_option = driver.find_element(By.XPATH, xpath_option)
  element_option.click()
 
  #chọn option
  #lấy ra danh sách options
  xpath_options = '//*[@id="formBSX"]/div[2]/div[2]/select/option'
  option_elements = driver.find_elements(By.XPATH, xpath_options)
  for i_element in option_elements:
    str_option = str(i_element.text)
    if str_option == 'Xe máy':
      #click vào option xe máy
      i_element.click()
      break

def xu_ly_captcha(driver):
  """xử lý captcha image"""
  # Wait for captcha image to be present
  wait = WebDriverWait(driver, 10)  # Wait up to 10 seconds
  element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="imgCaptcha"]')))
  
  #1. save thẻ img sang hình ảnh
  element.screenshot('captcha.png')

  #2. Sử dụng thư viện để trích xuất sang text
  img = Image.open('captcha.png')
  captcha_text = pytesseract.image_to_string(img).strip()
  print("Captcha OCR:", captcha_text)

  #3. Tương tác với thẻ input captcha: nhập captcha
  try:
    input_captcha = driver.find_element(By.XPATH, '//*[@id="formBSX"]/div[2]/div[3]/div/input')
    print("Tìm thấy ô nhập captcha!")
  except Exception as e:
    print("Không tìm thấy ô nhập captcha:", e)
    return
  input_captcha.send_keys(captcha_text)

  #4. submit tra cứu
  btn_submit = driver.find_element(By.XPATH, '//*[@id="formBSX"]/div[2]/input[1]')
  btn_submit.click()

def kiem_tra_ket_qua(driver):
  """kiểm tra kết quả captcha"""
  time.sleep(3)  # Chờ load kết quả
  #1. trích xuất kết quả

  #2. in ra lỗi phạt nguội hoặc không có lỗi
  try:
    result_element = driver.find_element(By.XPATH, '//*[@id="formBSX"]/div[2]/input[1]')
    print("Kết quả tra cứu:", result_element.text)
  except:
    print("Không tìm thấy kết quả hoặc captcha sai.")


def main():
  """handel tra cứu phạt nguội"""
  driver = open_chrome()

  xu_ly_bien_kiem_soat(driver)

  xu_ly_loai_phuong_tien(driver)

  xu_ly_captcha(driver)

  kiem_tra_ket_qua(driver)


main()