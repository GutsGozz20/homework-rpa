from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Khởi tạo trình duyệt
driver = webdriver.Chrome()
driver.get("https://thuvienphapluat.vn/ma-so-thue/tra-cuu-ma-so-thue-doanh-nghiep")

wait = WebDriverWait(driver, 10)
all_data = {}
page_number = 1
previous_first_row = ""

while True:
    print(f"📄 Đang lấy dữ liệu trang {page_number}...")

    # Đợi dữ liệu bảng xuất hiện
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, '//tbody//tr[contains(@class, "item_mst")]')))
    except TimeoutException:
        print("❌ Không thấy bảng dữ liệu, thoát.")
        break

    rows = driver.find_elements(By.XPATH, '//tbody//tr[contains(@class, "item_mst")]')
    data_output = []

    for row in rows:
        try:
            index = row.find_element(By.XPATH, './td[1]').text.strip()
            tax_code = row.find_element(By.XPATH, './td[2]').text.strip()
            name = row.find_element(By.XPATH, './td[3]').text.strip()
            date = row.find_element(By.XPATH, './td[4]').text.strip()
            data_output.append({
                "STT": index,
                "Mã số thuế": tax_code,
                "Tên doanh nghiệp": name,
                "Ngày cấp": date
            })
        except Exception as e:
            print(f"⚠️ Lỗi đọc dữ liệu dòng: {e}")

    # So sánh với trang trước để biết đã đến cuối
    current_first_row = data_output[0]["Mã số thuế"] if data_output else ""
    if current_first_row == previous_first_row:
        print("✅ Đã đến trang cuối cùng.")
        break

    previous_first_row = current_first_row
    all_data[f"Trang_{page_number}"] = pd.DataFrame(data_output)

    # Tìm và click nút Next
    try:
        next_btn = driver.find_element(By.XPATH, '//a[@aria-label="Next"]')
        if 'disabled' in next_btn.get_attribute('class'):
            print("✅ Nút Next đã bị disable. Đã đến trang cuối.")
            break
        next_btn.click()
        page_number += 1

        # Chờ dữ liệu mới khác trang trước
        for _ in range(10):
            time.sleep(1)
            new_rows = driver.find_elements(By.XPATH, '//tbody//tr[contains(@class, "item_mst")]')
            if not new_rows:
                continue
            new_first = new_rows[0].find_element(By.XPATH, './td[2]').text.strip()
            if new_first != previous_first_row:
                break
    except Exception as e:
        print(f"❌ Không click được Next: {e}")
        break

# Đóng trình duyệt
driver.quit()

# Ghi vào Excel (mỗi trang 1 sheet)
file_name = "Danh_sach_doanh_nghiep.xlsx"
with pd.ExcelWriter(file_name, engine="openpyxl") as writer:
    for sheet, df in all_data.items():
        df.to_excel(writer, sheet_name=sheet, index=False)

print(f"✅ Dữ liệu đã được lưu vào file: {file_name}")
