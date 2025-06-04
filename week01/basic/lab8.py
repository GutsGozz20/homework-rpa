def xen_ke_hoa_thuong(s):
    ket_qua = ""
    for i in range(len(s)):
        ket_qua += s[i].upper() if i % 2 == 0 else s[i].lower()
    return ket_qua

chuoi = input("Nhập chuỗi: ")
print("Kết quả: ", xen_ke_hoa_thuong(chuoi))
