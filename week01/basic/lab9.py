def kiem_tra_doi_xung(s):
    start = 0                  # Vị trí bắt đầu
    end = len(s) - 1           # Vị trí cuối cùng
    
    while start < end:
        if s[start] != s[end]:
            return False        # Nếu 2 ký tự không bằng nhau thì không đối xứng
        start += 1
        end -= 1
    
    return True                 # Nếu kiểm tra hết thì chuỗi đối xứng

chuoi = input("Nhập chuỗi: ")
if kiem_tra_doi_xung(chuoi):
    print("Chuỗi đối xứng.")
else:
    print("Chuỗi không đối xứng.")
