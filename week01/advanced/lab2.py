import time

# Hàm tạo số ngẫu nhiên từ phần miligiây
def tao_so_ngau_nhien():
    mili_giay = int((time.time() * 1000) % 1000)
    return mili_giay if mili_giay != 0 else 1  # Đảm bảo không có số 0

def nhap_so_nguoi_dung():
    while True:
        try:
            so = int(input("Nhập một số nguyên dương từ 1 đến 999: "))
            if 1 <= so <= 999:
                return so
            else:
                print("Vui lòng nhập số trong khoảng từ 1 đến 999.")
        except ValueError:
            print("\nVui lòng nhập một số nguyên hợp lệ.")

def main():
    print("==== MINIGAME: ĐOÁN SỐ ====")
    dap_an = tao_so_ngau_nhien()
    dem_sai = 0

    while True:
        doan = nhap_so_nguoi_dung()

        if doan == dap_an:
            print(f"🎉 Bạn đã dự đoán chính xác số {dap_an}!")
            break
        else:
            dem_sai += 1

            # Gần đúng nếu cách biệt trong khoảng ±10
            if abs(doan - dap_an) <= 10:
                print("💡 Bạn đoán gần đúng rồi!")
            else:
                print(f"Sai rồi! Bạn đã trả lời sai {dem_sai} lần. \n")

            # Sau 5 lần sai thì đổi số mới
            if dem_sai >= 5:
                dap_an = tao_so_ngau_nhien()
                dem_sai = 0
                print("😥 Bạn đoán trật tất cả năm lần, kết quả đã thay đổi. Mời bạn đoán lại!")

if __name__ == "__main__":
    main()
