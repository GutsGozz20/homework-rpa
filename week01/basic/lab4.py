# Nhập chuỗi từ người dùng
s = input("Nhập chuỗi: ")

char_count = {}

for char in s:
    if char in char_count:
        char_count[char] += 1
    else:
        char_count[char] = 1

print("Số lần xuất hiện của từng ký tự:")
for char in char_count:
    print(f"'{char}': {char_count[char]}")
