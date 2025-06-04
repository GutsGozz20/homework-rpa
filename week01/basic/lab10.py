def doc_so_3_chu_so(n):
    numbers = ["không", "một", "hai", "ba", "bốn", "năm", "sáu", "bảy", "tám", "chín"]
    
    if len(n) != 3 or not n.isdigit():
        return "Vui lòng nhập số có đúng 3 chữ số."
    
    tram = int(n[0])
    chuc = int(n[1])
    don_vi = int(n[2])
    
    result = numbers[tram] + " trăm"
    
    if chuc == 0 and don_vi == 0:
        return result
    
    if chuc == 0:
        result += " lẻ"
    elif chuc == 1:
        result += " mười"
    else:
        result += " " + numbers[chuc] + " mươi"
    
    if don_vi == 0:
        return result
    elif don_vi == 1 and chuc > 1:
        result += " mốt"
    elif don_vi == 5 and chuc != 0:
        result += " lăm"
    else:
        result += " " + numbers[don_vi]
    
    return result

so_nhap = input("Nhập số có 3 chữ số: ")
print("Kết quả: ", doc_so_3_chu_so(so_nhap))
