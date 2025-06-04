# def viet_hoa_dau_tu(s):
#     return ' '.join(word.capitalize() for word in s.split())

# chuoi = input("Nhập chuỗi: ")
# print("Kết quả:", viet_hoa_dau_tu(chuoi))

#cach khac
def chuan_hoa_chuoi(s):
    words = s.split()                
    words_capitalized = [word.capitalize() for word in words]  # Viết hoa chữ cái đầu mỗi từ
    return " ".join(words_capitalized) 

chuoi = input("Nhập chuỗi: ")
ket_qua = chuan_hoa_chuoi(chuoi)
print("Chuỗi sau khi chuẩn hóa:", ket_qua)
