from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

driver = webdriver.Chrome()  # Khởi động trình duyệt Chrome
driver.get("https://thuvienphapluat.vn/ma-so-thue/tra-cuu-ma-so-thue-doanh-nghiep")  # Mở trang web
time.sleep(3)

#lấy tất cả thông tin
element_rows = '//tbody//tr[contains(@class, "item_mst")]'
full_rows = driver.find_elements(By.XPATH,element_rows)

#gom dữ liệu
data_output = []
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
        print(f"Lỗi: {e}")
        continue



# Lưu dữ liệu vào file Excel
df = pd.DataFrame(data_output)
df.to_excel("Enterprise.xlsx", index=False)
print("luu file Enterprise.xlsx")

time.sleep(1000)








