def cat_ho_ten(full_name):
    full_name = full_name.strip()
    parts = full_name.split()
    
    ten = parts[-1]
    
    ho_lot = ""
    for i in range(len(parts)-1):
        ho_lot += parts[i] + " "
    ho_lot = ho_lot.strip()
    
    return ho_lot, ten


ho_ten = input("Nhập họ tên: ")
ho_lot, ten = cat_ho_ten(ho_ten)

print("Họ và tên lót:", ho_lot)
print("Tên:", ten)
