s = input("Nhập chuỗi: ").lower().replace(" ", "")

char_count = {}

for char in s:
    if char in char_count:
        char_count[char] += 1
    else:
        char_count[char] = 1

max_count = max(char_count.values())

print(f"Các ký tự xuất hiện nhiều nhất ({max_count} lần):")
for char in char_count:
    if char_count[char] == max_count:
        print(f"'{char}'")
