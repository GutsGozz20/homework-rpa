
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd

# Khởi tạo trình duyệt
driver = webdriver.Chrome()
driver.get("https://thuvienphapluat.vn/ma-so-thue/tra-cuu-ma-so-thue-doanh-nghiep")
time.sleep(3)

# Dữ liệu lưu theo trang
all_data = {}

page_number = 1
while True:
    print(f"Đang thu thập dữ liệu trang {page_number}...")

    data_output = []

    # Lấy tất cả các dòng kết quả
    element_rows = '//tbody//tr[contains(@class, "item_mst")]'
    full_rows = driver.find_elements(By.XPATH, element_rows)

    # Gộp dữ liệu từ mỗi dòng
    for row in full_rows:
        try:
            index = row.find_element(By.XPATH, './/td[1]').text.strip()
            tax_code = row.find_element(By.XPATH, './/td[2]').text.strip()
            name = row.find_element(By.XPATH, './/td[3]').text.strip()
            date = row.find_element(By.XPATH, './/td[4]').text.strip()
            data_output.append({
                "STT": index,
                "Mã số thuế": tax_code,
                "Tên doanh nghiệp": name,
                "Ngày cấp": date,
            })
        except Exception as e:
            print(f"Lỗi ở trang {page_number}: {e}")
            continue

    # Lưu vào dict sheet
    df = pd.DataFrame(data_output)
    all_data[f"Trang_{page_number}"] = df

    # Tìm nút Next
    try:
        next_button = driver.find_element(By.XPATH, '//a[@aria-label="Next"]')
        if "disabled" in next_button.get_attribute("class"):
            print("Đã đến trang cuối cùng.")
            break
        next_button.click()
        page_number += 1
        time.sleep(2)
    except NoSuchElementException:
        print("Không tìm thấy nút Next. Kết thúc.")
        break

# Đóng trình duyệt
driver.quit()

# Lưu vào Excel, mỗi trang là 1 sheet
output_file = "Enterprise_MultiSheet.xlsx"
with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    for sheet, df in all_data.items():
        df.to_excel(writer, sheet_name=sheet, index=False)

print(f"✅ Đã lưu tất cả dữ liệu vào {output_file}")
