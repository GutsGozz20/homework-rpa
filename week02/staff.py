import pandas as pd
import numpy as np

# Tạo bảng Nhân viên
nhan_vien = pd.DataFrame({
    'ID': [101, 102, 103, 104, 105, 106],
    'Name': ['An', 'Bình', 'Cường', 'Dương', np.nan, 'Hạnh'],
    'Age': [25, np.nan, 30, 22, 28, 35],
    'Department': ['HR', 'IT', 'IT', 'Finance', 'HR', np.nan],
    'Salary': [700, 800, 750, np.nan, 710, 770]
})

# Tạo bảng Phòng ban
phong_ban = pd.DataFrame({
    'Department': ['HR', 'IT', 'Finance', 'Marketing'],
    'Manager': ['Trang', 'Khoa', 'Minh', 'Lan']
})

# 1. Kiểm tra các ô dữ liệu bị thiếu
print("Các ô bị thiếu:")
print(nhan_vien.isnull())

# 2. Xoá dòng có hơn 2 giá trị bị thiếu
nhan_vien = nhan_vien[nhan_vien.isnull().sum(axis=1) <= 2]

# 3. Điền giá trị thiếu
nhan_vien['Name'] = nhan_vien['Name'].fillna("Chưa rõ")
nhan_vien['Age'] = nhan_vien['Age'].fillna(nhan_vien['Age'].mean())
nhan_vien['Department'] = nhan_vien['Department'].fillna("Unknown")
nhan_vien['Salary'] = nhan_vien['Salary'].ffill()


# 4. Chuyển kiểu dữ liệu Age và Salary sang int
nhan_vien['Age'] = nhan_vien['Age'].astype(int)
nhan_vien['Salary'] = nhan_vien['Salary'].astype(int)

# 5. Tạo cột Salary_after_tax
nhan_vien['Salary_after_tax'] = nhan_vien['Salary'] * 0.9

# 6. Lọc nhân viên phòng IT và có tuổi > 25
loc_nhan_vien = nhan_vien[(nhan_vien['Department'] == 'IT') & (nhan_vien['Age'] > 25)]
print("\nNhân viên phòng IT và tuổi > 25:")
print(loc_nhan_vien)

# 7. Sắp xếp theo Salary_after_tax giảm dần
nhan_vien_sorted = nhan_vien.sort_values(by='Salary_after_tax', ascending=False)
print("\nBảng nhân viên sắp xếp theo Salary_after_tax giảm dần:")
print(nhan_vien_sorted)

# 8. Nhóm theo Department và tính lương trung bình
mean_salary_by_dept = nhan_vien.groupby('Department')['Salary'].mean().reset_index()
print("\nLương trung bình theo phòng ban:")
print(mean_salary_by_dept)

# 9. Dùng merge để nối với bảng phòng ban
nhan_vien_merged = pd.merge(nhan_vien, phong_ban, on='Department', how='left')
print("\nBảng nhân viên kèm thông tin Manager:")
print(nhan_vien_merged)

# 10. Tạo 2 nhân viên mới và dùng concat để thêm vào
nhan_vien_moi = pd.DataFrame({
    'ID': [107, 108],
    'Name': ['Hòa', 'Kiên'],
    'Age': [26, 29],
    'Department': ['Marketing', 'HR'],
    'Salary': [760, 730]
})

# Tính thêm cột Salary_after_tax cho nhân viên mới
nhan_vien_moi['Salary_after_tax'] = nhan_vien_moi['Salary'] * 0.9

# Nối vào bảng nhân viên cũ
nhan_vien_full = pd.concat([nhan_vien, nhan_vien_moi], ignore_index=True)
print("\nBảng Nhân viên sau khi thêm nhân viên mới:")
print(nhan_vien_full)
