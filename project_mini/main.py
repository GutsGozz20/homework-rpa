# from curses import echo
import os
from this import d
import time
import glob
import logging
import xmltodict
import pandas as pd
from selenium import webdriver
import xml.etree.ElementTree as ET
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
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
#FPT
def xu_ly_fpt(mst, ma_tra_cuu, url):
  """Xử lý URL FPT: cần cả Mã số thuế và Mã tra cứu."""
  if not mst or not ma_tra_cuu:
    return {'Loại': 'FPT', 'Trạng thái': 'Thiếu dữ liệu'}

  link_tra_cuu = f"{url}?mst={mst}&traCuu={ma_tra_cuu}"
  return {
    'Loại': 'FPT',
    'Mã số thuế': mst,
    'Mã tra cứu': ma_tra_cuu,
    'Link tra cứu': link_tra_cuu,
    'Trạng thái': 'Đã xử lý'
  }
  # MeInvoice
def xu_ly_meinvoice(ma_tra_cuu, url):
  """Xử lý URL MeInvoice: chỉ cần Mã tra cứu."""
  if not ma_tra_cuu:
    return {'Loại': 'MeInvoice', 'Trạng thái': 'Thiếu mã tra cứu'}

  link_tra_cuu = f"{url}?key={ma_tra_cuu}"
  return {
    'Loại': 'MeInvoice',
    'Mã số thuế': None,
    'Mã tra cứu': ma_tra_cuu,
    'Link tra cứu': link_tra_cuu,
    'Trạng thái': 'Đã xử lý'
  }
# eHoadon
def xu_ly_ehoadon(ma_tra_cuu):
  """Xử lý URL eHoadon: chỉ cần Mã tra cứu, không cần tạo link."""
  if not ma_tra_cuu:
    return {'Loại': 'eHoadon', 'Trạng thái': 'Thiếu mã tra cứu'}

  return {
    'Loại': 'eHoadon',
    'Mã số thuế': None,
    'Mã tra cứu': ma_tra_cuu,
    'Link tra cứu': '',  # Không cần tạo link
    'Trạng thái': 'Đã xử lý'
  }


def xu_ly_file_input(file_path):
  df = pd.read_excel(file_path, dtype={'Mã số thuế': str, 'Mã tra cứu': str}, engine='openpyxl')
  df = df[['Mã số thuế', 'Mã tra cứu', 'URL']].fillna('')
  
  ket_qua = []
  # bảng ánh xạ domain -> (hàm cần xử lý, cần_mst)
  url_handler = [
    ('tracuuhoadon.fpt.com.vn', lambda mst, matc, url: xu_ly_fpt(mst, matc, url), True),
    ('meinvoice.vn', lambda mst, matc, url: xu_ly_meinvoice(matc, url), False),
    ('van.ehoadon.vn', lambda mst, matc, url: xu_ly_ehoadon(matc), False)
  ]
  

  for _, row in df.iterrows():
    mst = str(row['Mã số thuế']).strip()
    matc = str(row['Mã tra cứu']).strip()
    url = str(row.get('URL', '')).strip().lower()

    for domain, handler, need_mst in url_handler:
      if domain in url:
        ket_qua.append(handler(mst, matc, url))
        break
    else:
      ket_qua.append({
        'Loại': 'Không xác định',
        'Mã số thuế': mst,
        'Mã tra cứu': matc,
        'Link tra cứu': '',
        'Trạng thái': 'URL không hợp lệ'
      })

  return ket_qua

def open_chrome(url, download_dir):
  """Mở Chrome và truy cập trang web tra cứu tương ứng với URL đầu vào"""
  if not os.path.exists(download_dir):
    os.makedirs(download_dir)
    
  chrome_options = Options()
  chrome_options.add_experimental_option("prefs", {
    "download.default_directory": download_dir,
    "download.prompt_for_download": False,
    "directory_upgrade": True,
    "safebrowsing.enabled": True
  })
  chrome_options.add_argument("--disable-notifications")
  chrome_options.add_argument("--start-maximized")
  driver = webdriver.Chrome(options=chrome_options)
  
  # Chuẩn hóa URL đầu vào
  normalized_url = url.strip().lower()

  if "tracuuhoadon.fpt.com.vn" in normalized_url:
    driver.get("https://tracuuhoadon.fpt.com.vn/search.html")

  elif "meinvoice.vn" in normalized_url:
    driver.get("https://www.meinvoice.vn/tra-cuu/")

  elif "van.ehoadon.vn" in normalized_url:
    driver.get("https://van.ehoadon.vn/TCHD?MTC=")  

  else:
    driver.quit()
    raise ValueError(f" URL không được hỗ trợ: {url}")

  return driver

# nhập mã tra cứu, mã số thuế FPT
def xu_ly_tra_cuu_fpt(driver, mst, ma_tra_cuu):
  logging.warning(f"Chuẩn bị nhập MST: {mst}, Mã tra cứu: {ma_tra_cuu}")
  wait = WebDriverWait(driver, 10)
  input_mst = wait.until(EC.presence_of_element_located((
    By.XPATH, '//input[@placeholder="MST bên bán"]'
  )))
  input_mst.clear()
  input_mst.send_keys(mst)

  input_ma_tra_cuu = wait.until(EC.presence_of_element_located((
    By.XPATH, '//input[@placeholder="Mã tra cứu hóa đơn"]'
  )))
  input_ma_tra_cuu.clear()
  input_ma_tra_cuu.send_keys(ma_tra_cuu)
  logging.info(f"Đã nhập mã tra cứu: {ma_tra_cuu} và mã số thuế: {mst}")

  # driver.find_element(By.ID, "mst").send_keys(mst)
  #   driver.find_element(By.ID, "maTraCuu").send_keys(ma_tra_cuu)

def xu_ly_tim_kiem_hoa_don_fpt(driver):
  """ xử lý tìm kiếm hóa đơn và xử lý lỗi nếu có"""
  btn_xpath_fpt = '/html/body/div[3]/div/div/div[3]/div/div[1]/div/div[4]/div[2]/div/button'

  WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, btn_xpath_fpt))
  ).click()
  logging.info("Đã nhấn nút Tra cứu.")

# hàm kết quả tra cứu fpt
def kiem_tra_ket_qua_tra_cuu_fpt(driver):
  """Kiểm tra kết quả tra cứu"""
  try:
    error_xpath_mst = '/html/body/div[3]/div/div/div[3]/div/div[1]/div/div[2]/div[2]'
    error_element = WebDriverWait(driver, 5).until(
      EC.visibility_of_element_located((By.XPATH, error_xpath_mst))
    )
    error_text = error_element.text.strip()

    if "Không tìm thấy hóa đơn" in error_text:
      logging.warning("Mã tra cứu không đúng: Không tìm thấy hóa đơn.")
    elif "MST" in error_text or "mã số thuế" in error_text.lower():
      logging.warning(f"Lỗi mã số thuế: {error_text}")
    else:
      logging.warning(f"Lỗi không xác định: {error_text}")
    return False

  except:
    logging.info("Tra cứu thành công - Không có lỗi hiển thị- tiếp tục hehe.")
    return True

  # xử lý tải hóa đơn (file xml)
def xu_ly_tai_hoa_don_fpt(driver):
  """Xử lý tải hóa đơn XML trên trang FPT"""

  try:
    # Chờ overlay (nếu có) biến mất
    try:
      WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.CLASS_NAME, "m-mask-modal"))
      )
    except Exception as e:
      logging.warning(f"Overlay không biến mất sau 10s, tiếp tục... {e}")

    # Tìm và click nút tải hóa đơn
    btn_download_xpath_fpt = '/html/body/div[3]/div/div/div[3]/div/div[1]/div/div[4]/div[2]/div/button'
    logging.warning("Chuẩn bị tìm và click nút tải XML")
    btn_download = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, btn_download_xpath_fpt))
    )
    btn_download.click()
    logging.info("Đã nhấn nút tải XML.") 
  except Exception as e:
    logging.error(f'Lỗi khi tải hóa đơn FPT: {e}')
    raise

# __________MISA (meinvoice)________

def xu_ly_tra_cuu_meinvoice(driver, ma_tra_cuu):
  """xử lý mã tra cứu hóa đơn"""
  try:
    xpath = '//*[@id="txtCode"]'
    element_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )
    element_input.clear()
    element_input.send_keys(ma_tra_cuu)
    logging.info(f"Đã nhập mã tra cứu: {ma_tra_cuu}")
    return True
  except Exception as e:
    logging.error(f"Lỗi khi nhập mã tra cứu MeInvoice: {e}")
    return False

def xu_ly_tim_kiem_hoa_don_meinvoice(driver):
  """ xử lý tìm kiếm hóa đơn"""
  btn_xpath = '//*[@id="btnSearchInvoice"]'
  WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, btn_xpath))
  ).click()
  logging.info("Đã nhấn nút Tìm kiếm.")
  return True

def kiem_tra_ket_qua_tra_cuu_meinvoice(driver):
  """Kiểm tra kết quả tra cứu"""
  try:
    error_xpath = '//*[@id="popup-invoicnotexist-content"]' 
    error_element = WebDriverWait(driver, 5).until(
      EC.visibility_of_element_located((By.XPATH, error_xpath))
    )
    logging.warning(f"Lỗi tra cứu: {error_element.text}")
    return False
  except:
    logging.info("Không có lỗi tra cứu, tiếp tục.")
    return True

def xu_ly_tai_hoa_don_meinvoice(driver,download_dir):
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

    # Bước 2: Chờ popup hiện nút tải XML
  
    btn_xml_xpath = '//*[@id="popup-content-container"]/div[1]/div[2]/div[12]/div/div/div[2]'
    WebDriverWait(driver, 10).until(
      EC.element_to_be_clickable((By.XPATH, btn_xml_xpath))
    )

    # Bước 3: Click nút tải XML
    btn_xml= driver.find_element(By.XPATH, btn_xml_xpath)
    btn_xml.click()
    time.sleep(2)
    logging.info("Đã nhấn nút tải XML.")
    wait_for_downloads(download_dir) # chờ file tải xong
    # Bước 4: Kiểm tra có file XML trong thư mục
    xml_files = glob.glob(os.path.join(download_dir, "*.xml"))
    if not xml_files:
      logging.warning("Không tìm thấy file XML sau khi tải.")
    else:
      logging.info(f"Đã tải thành công file: {os.path.basename(xml_files[-1])}")
  except Exception as e:
    logging.error(f"Lỗi khi tải hóa đơn MeInvoice: {e}")
    raise

# __________EHOADON________
def xu_ly_tra_cuu_ehoadon(driver, ma_tra_cuu):
  """xử lý mã tra cứu hóa đơn"""
  try: 
    xpath = '//*[@id="txtInvoiceCode"]'
    element_input = WebDriverWait(driver, 10).until(
      EC.presence_of_element_located((By.XPATH, xpath))
    )
    element_input.clear()
    element_input.send_keys(ma_tra_cuu)
    logging.info(f"Đã nhập mã tra cứu: {ma_tra_cuu}")
    return True
  except Exception as e:
    logging.error(f"Lỗi khi nhập mã tra cứu eHoadon: {e}")
    return False

def xu_ly_tim_kiem_hoa_don_ehoadon(driver):
  """xử lý tìm kiếm hóa đơn"""
  btn_xpath_ehoadon = '//*[@id="Button1"]'
  WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, btn_xpath_ehoadon))
  ).click()
  logging.info("Đã nhấn nút Tra cứu.")
  return True
      
def kiem_tra_ket_qua_tra_cuu_ehoadon(driver):
  """Kiểm tra kết quả tra cứu"""
  try:
    error_path_ehoadon = '//*[@id="Bkav_alert_dialog"]/div/div[1]/div[2]'
    error_element_ehoadon = WebDriverWait(driver, 5).until(
      EC.visibility_of_element_located((By.XPATH, error_path_ehoadon))
    )
    logging.warning(f"Lỗi tra cứu: {error_element_ehoadon.text}")
    return False
  except:
    logging.info("Không có lỗi tra cứu, tiếp tục.")
    return True

def xu_ly_tai_hoa_don_ehoadon(driver, download_dir):
    """Xử lý tải hóa đơn ehoadon"""
    try:
      #switch sang frameframe
      element_frame_xpath_ehoadon = '//*[@id="frameViewInvoice"]'
      element_frame_ehoadon = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, element_frame_xpath_ehoadon))
      )
      driver.switch_to.frame(element_frame_ehoadon)
      

      # Bước 1: click nút tổng 
      btn_download_xpath_ehoadon = '//input[@id="btnDownload"]'
      btn_download_ehoadon = WebDriverWait(driver, 20).until(
          EC.element_to_be_clickable((By.XPATH, btn_download_xpath_ehoadon))
      )
      btn_download_ehoadon.click()
      logging.info("Đã nhấn nút tải hóa đơn ehoadon.")

      # Bước 2: chờ popup xuất hiện và click nút tải XML
      btn_xml_xpath_ehoadon = '//a[@id="LinkDownXML"]'
      btn_xml_ehoadon = WebDriverWait(driver, 20).until(
          EC.element_to_be_clickable((By.XPATH, btn_xml_xpath_ehoadon))
      )
      btn_xml_ehoadon.click()
      logging.info("Đã nhấn nút tải XML ehoadon.")

      time.sleep(2)
      wait_for_downloads(download_dir) # chờ file tải xong
      # Bước 4: Kiểm tra có file XML trong thư mục
      xml_files = glob.glob(os.path.join(download_dir, "*.xml"))
      if not xml_files:
        logging.warning("Không tìm thấy file XML sau khi tải.")
      else:
        logging.info(f"Đã tải thành công file: {os.path.basename(xml_files[-1])}")
    except Exception as e:
      logging.error(f"Lỗi khi tải hóa đơn eHoadon: {e}")
      raise


# chờ file tải xong
def wait_for_downloads(download_dir, timeout=30):
    seconds = 0
    while any(fname.endswith('.crdownload') for fname in os.listdir(download_dir)):
        time.sleep(1)
        seconds += 1
        if seconds > timeout:
            break
def xu_ly_dong_trinh_duyet(driver):
  driver.quit()
  logging.info("--- Kết thúc. Bye Bye!!!!---")

def xu_ly_doc_file_xml(xml_path):
  """Đọc nội dung file XML hóa đơn"""
  try:
    with open(xml_path, 'r', encoding='utf-8') as file:
      data_dict = xmltodict.parse(file.read())
    print(data_dict.keys())
    return data_dict
  except Exception as e:
    logging.error(f"Lỗi khi đọc file XML: {e}")
    return None

def xu_ly_trich_xuat_thong_tin(root_dict, loai):
    """Trích xuất thông tin từ file XML theo từng loại"""

    def get_text(data, path):
        keys = [k for k in path.strip().split('/') if k and k != '.']
        for k in keys:
            if isinstance(data, dict) and k in data:
                data = data[k]
            else:
                return ''
        return data.strip() if isinstance(data, str) else ''

    if loai == 'FPT':
      #lấy phần gốc từ xml :
        dlhdon_fpt = root_dict['TDiep']['DLieu']['HDon']['DLHDon']
        return {
            'Số hóa đơn': get_text(dlhdon_fpt, 'TTChung/SHDon'),
            'Đơn vị bán hàng': get_text(dlhdon_fpt, 'NDHDon/NBan/Ten'),
            'Mã số thuế bán': get_text(dlhdon_fpt, 'NDHDon/NBan/MST'),
            'Địa chỉ bán': get_text(dlhdon_fpt, 'NDHDon/NBan/DChi'),
            'Số tài khoản bán': '',  # Không tồn tại trong XML
            'Họ tên người mua hàng': get_text(dlhdon_fpt, 'NDHDon/NMua/HVTNMHang'),
            'Địa chỉ mua': get_text(dlhdon_fpt, 'NDHDon/NMua/DChi'),
            'Mã số thuế mua': get_text(dlhdon_fpt, 'NDHDon/NMua/MST')
        }
    elif loai == 'MeInvoice':
        dlhdon_meinvoice = root_dict['HDon']['DLHDon']
        return {
            'Số hóa đơn': get_text(dlhdon_meinvoice, 'TTChung/SHDon'),
            'Đơn vị bán hàng': get_text(dlhdon_meinvoice, 'NDHDon/NBan/Ten'),
            'Mã số thuế bán': get_text(dlhdon_meinvoice, 'NDHDon/NBan/MST'),
            'Địa chỉ bán': get_text(dlhdon_meinvoice, 'NDHDon/NBan/DChi'),
            'Số tài khoản bán': get_text(dlhdon_meinvoice, 'NDHDon/NBan/STKNHang'),  
            'Họ tên người mua hàng': get_text(dlhdon_meinvoice, 'NDHDon/NMua/Ten'),
            'Địa chỉ mua': get_text(dlhdon_meinvoice, 'NDHDon/NMua/DChi'),
            'Mã số thuế mua': get_text(dlhdon_meinvoice, 'NDHDon/NMua/MST')
        }
    elif loai == 'eHoadon':
        dlhdon_ehoadon = root_dict['HDon']['DLHDon']
        return {
            "Số hóa đơn": get_text(dlhdon_ehoadon, "TTChung/SHDon"),
            "Đơn vị bán hàng": get_text(dlhdon_ehoadon, "NDHDon/NBan/Ten"),
            "Mã số thuế bán": get_text(dlhdon_ehoadon, "NDHDon/NBan/MST"),
            "Địa chỉ bán": get_text(dlhdon_ehoadon, "NDHDon/NBan/DChi"),
            "Số tài khoản bán": '',
            "Họ tên người mua hàng": get_text(dlhdon_ehoadon, "NDHDon/NMua/Ten"),
            "Địa chỉ mua": get_text(dlhdon_ehoadon, "NDHDon/NMua/DChi"),
            "Mã số thuế mua": get_text(dlhdon_ehoadon, "NDHDon/NMua/MST")
        }
    else:
        # Trường hợp không xác định
        return {k: "" for k in [
            'Số hóa đơn', 'Đơn vị bán hàng', 'Mã số thuế bán', 'Địa chỉ bán',
            'Số tài khoản bán', 'Họ tên người mua hàng', 'Địa chỉ mua', 'Mã số thuế mua'
        ]}

def main():
  setup_logging() 
  file_path = "input.xlsx" 

  script_dir = os.path.dirname(os.path.abspath(__file__))
  download_dir = os.path.join(script_dir, "downloads")

  # Xóa các file xml cũ trong thư mục downloads để bắt đầu phiên làm việc mới
  if os.path.exists(download_dir):
    xml_file_dict = glob.glob(os.path.join(download_dir, "*.xml"))
    for f in xml_file_dict:
      try:
        os.remove(f)
      except OSError as e:
        logging.error(f"Error removing file {f}: {e}")
  
  df_input = pd.read_excel(file_path, dtype={'Mã số thuế': str, 'Mã tra cứu': str})
  ket_qua = xu_ly_file_input(file_path)
  extracted_data = []
  default_info = {k: "" for k in [
    'Số hóa đơn', 'Đơn vị bán hàng', 'Mã số thuế bán', 'Địa chỉ bán',
    'Số tài khoản bán', 'Họ tên người mua hàng', 'Địa chỉ mua', 'Mã số thuế mua'
  ]}

  try:
    driver = open_chrome('https://tracuuhoadon.fpt.com.vn/search.html', download_dir=download_dir)
  except ValueError as e:
    logging.error(f"Không thể khởi động trình duyệt: {e}")
    return

  for item in ket_qua:
    info = default_info.copy()
    ma_tra_cuu_item = item.get('Mã tra cứu', 'unknown')

    try:
      loai = item.get('Loại')
      files_before = set(os.listdir(download_dir))
      download_success = False

      if loai == 'FPT':
        logging.warning("---Tra cứu hóa đơn FPT ---")
        mst = item.get('Mã số thuế')
        driver.get("https://tracuuhoadon.fpt.com.vn/search.html")
        xu_ly_tra_cuu_fpt(driver, mst, ma_tra_cuu_item)
        xu_ly_tim_kiem_hoa_don_fpt(driver)
        if kiem_tra_ket_qua_tra_cuu_fpt(driver):
            xu_ly_tai_hoa_don_fpt(driver)
            wait_for_downloads(download_dir)
            download_success = True

      elif loai == 'MeInvoice':
        logging.warning("--- Tra cứu hóa đơn MeInvoice ---")
        driver.get("https://www.meinvoice.vn/tra-cuu/")
        if xu_ly_tra_cuu_meinvoice(driver, ma_tra_cuu_item):
          if xu_ly_tim_kiem_hoa_don_meinvoice(driver):
            if kiem_tra_ket_qua_tra_cuu_meinvoice(driver):
              xu_ly_tai_hoa_don_meinvoice(driver, download_dir)
              wait_for_downloads(download_dir)
              download_success = True

      elif loai == 'eHoadon': 
        logging.warning("--- Tra cứu hóa đơn eHoadon---")
        driver.get("https://van.ehoadon.vn/TCHD?MTC=")
        if xu_ly_tra_cuu_ehoadon(driver, ma_tra_cuu_item):
          xu_ly_tim_kiem_hoa_don_ehoadon(driver)
          if kiem_tra_ket_qua_tra_cuu_ehoadon(driver):
            xu_ly_tai_hoa_don_ehoadon(driver, download_dir)
            wait_for_downloads(download_dir)
            download_success = True
      
      if download_success:
        time.sleep(1) 
        files_after = set(os.listdir(download_dir))
        new_files = [f for f in (files_after - files_before) if f.lower().endswith('.xml')]

        if new_files:
          new_file_name = new_files[0]
          new_file_path = os.path.join(download_dir, new_file_name)
          logging.info(f"Đang xử lý file mới: {new_file_name}")
          root = xu_ly_doc_file_xml(new_file_path)
          if root is not None:
            info = xu_ly_trich_xuat_thong_tin(root, loai)
          
          # Đổi tên file đã xử lý để tránh trùng lặp
          processed_filename = f"processed_{ma_tra_cuu_item}_{new_file_name}"
          try:
              os.rename(new_file_path, os.path.join(download_dir, processed_filename))
          except OSError as e:
              logging.error(f"Không thể đổi tên file {new_file_name}: {e}")
      else:
        logging.warning(f"Không có file XML nào được tải về cho mã: {ma_tra_cuu_item}")

    except Exception as e:
      logging.error(f"Lỗi khi xử lý item với mã tra cứu {ma_tra_cuu_item}: {e}")
            
    extracted_data.append(info)

  xu_ly_dong_trinh_duyet(driver) 

    # --- Tạo file output cuối cùng ---
  if extracted_data:
    df_xml = pd.DataFrame(extracted_data)
    df_output = pd.concat([df_input.reset_index(drop=True), df_xml.reset_index(drop=True)], axis=1)
    output_filename = "output.xlsx"
    try:
      df_output.to_excel(output_filename, index=False)
      logging.info(f"Đã lưu kết quả vào {output_filename}")
    except Exception as e:
      logging.error(f"Không thể lưu file output: {e}")
  else:
    logging.warning("Không có dữ liệu nào được trích xuất.")


if __name__=="__main__":
  main()