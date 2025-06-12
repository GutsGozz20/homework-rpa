from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time

# Danh sách tài khoản mẫu từ trang web
usernames = [
    "standard_user", "locked_out_user", "problem_user",
    "performance_glitch_user", "error_user", "visual_user"
]
password = "secret_sauce"

# Khởi tạo trình duyệt
driver = webdriver.Chrome()
driver.get("https://www.saucedemo.com/")
time.sleep(2)

# Đăng nhập từng tài khoản
for user in usernames:
    driver.get("https://www.saucedemo.com/")
    driver.find_element(By.ID, "user-name").clear()
    driver.find_element(By.ID, "password").clear()
    
    driver.find_element(By.ID, "user-name").send_keys(user)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "login-button").click()
    time.sleep(2)
    
    # Kiểm tra đăng nhập thành công (nếu có sản phẩm)
    if "inventory" in driver.current_url:
        names = driver.find_elements(By.CLASS_NAME, "inventory_item_name")
        prices = driver.find_elements(By.CLASS_NAME, "inventory_item_price")

        data = []
        for n, p in zip(names, prices):
            data.append({"Username": user, "Product Name": n.text, "Price": p.text})

        # Lưu vào Excel (thêm từng user vào sheet riêng)
        df = pd.DataFrame(data) #data là một danh sách các dictionary, mỗi dictionary chứa thông tin sản phẩm của một tài khoản
        #Lưu vào Excel (thêm từng user vào sheet riêng)
        with pd.ExcelWriter("products.xlsx", engine="openpyxl", mode="a" if user != usernames[0] else "w") as writer:
            df.to_excel(writer, index=False, sheet_name=user)
    else:
        print(f"[!] Tài khoản '{user}' đăng nhập thất bại!")

driver.quit()
