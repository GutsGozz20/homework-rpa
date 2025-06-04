import math

def is_perfect_square(n):
    return int(math.sqrt(n))**2 == n

def nhap_so_nguyen(prompt):
    while True:
        try:
            n = int(input(prompt))
            return n
        except ValueError:
            print("Vui lòng nhập một số nguyên hợp lệ.")

def main():
    while True:
        a = nhap_so_nguyen("Nhập số nguyên a: ")
        b = nhap_so_nguyen("Nhập số nguyên b: ")
        if a < b:
            break
        else:
            print("Giá trị a phải nhỏ hơn b. Vui lòng nhập lại.")

    ket_qua = []
    for i in range(a, b + 1):
        if i % 3 == 0 and not is_perfect_square(i):
            ket_qua.append(str(i))
    
    print("Kết quả:", ",".join(ket_qua))

if __name__ == "__main__":
    main()
