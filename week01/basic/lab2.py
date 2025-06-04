
s = input("Nhập chuỗi: ")
danh_sach_tu = s.split() #tách chuỗi -> từ
danh_sach_tu_dao_nguoc = list(reversed(danh_sach_tu)) #đảo ngược
chuoi_dao_nguoc = ' '.join(danh_sach_tu_dao_nguoc) #nối
print("Chuỗi sau khi đảo ngược từ:", chuoi_dao_nguoc)
