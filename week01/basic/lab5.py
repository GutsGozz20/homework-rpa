def kiem_tra_va_tach_so(s):
    so_list = []  
    for ky_tu in s:
        if ky_tu.isdigit():   
            so_list.append(ky_tu) 
    if len(so_list) > 0:
        return True, so_list   
    else:
        return False, []      

chuoi = input("Nhập chuỗi: ")
co_so, danh_sach_so = kiem_tra_va_tach_so(chuoi)

if co_so:
    print("Chuỗi có ký tự số:", danh_sach_so)
else:
    print("Chuỗi không có ký tự số.")
