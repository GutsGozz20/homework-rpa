import pandas as pd

# Tạo DataFrame với thông tin 10 sinh viên
data = {
    'Name': ['An', 'Bình', 'Chi', 'Dũng', 'Hà', 'Khôi', 'Lan', 'Minh', 'Ngọc', 'Phúc'],
    'Age': [20, 21, 19, 22, 20, 23, 21, 22, 20, 19],
    'Gender': ['Male', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male', 'Female', 'Male'],
    'Score': [7.5, 8.0, 4.5, 6.0, 9.0, 3.5, 5.0, 2.0, 6.5, 8.5]
}

df_students = pd.DataFrame(data)

# Hiển thị toàn bộ dữ liệu
print("Toàn bộ dữ liệu:")
print(df_students)

# Hiển thị 3 dòng đầu tiên
print("\n3 dòng đầu tiên:")
print(df_students.head(3))

# Hiển thị theo index=2 và cột Name
print("\nIndex = 2, cột Name:")
print(df_students.loc[2, 'Name'])

# Hiển thị theo index=10 và cột Age (index 10 không tồn tại)
print("\nIndex = 10, cột Age:")
if 10 in df_students.index:
    print(df_students.loc[10, 'Age'])
else:
    print("Index 10 không tồn tại.")

# Hiển thị các cột Name và Score
print("\nCác cột Name và Score:")
print(df_students[['Name', 'Score']])

# Thêm cột Pass: True nếu Score >= 5, ngược lại False
df_students['Pass'] = df_students['Score'] >= 5
print("\nThêm cột Pass:")
print(df_students)

# Sắp xếp danh sách sinh viên theo Score giảm dần
df_sorted = df_students.sort_values(by='Score', ascending=False)
print("\nSắp xếp theo Score giảm dần:")
print(df_sorted) 