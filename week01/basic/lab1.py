# def normalize_string(s):
#     # Tách chuỗi thành danh sách các từ
#     word_list = s.split()
#     # Viết hoa chữ cái đầu và chữ thường các ký tự còn lại của từng từ
#     normalized_words = [word.capitalize() for word in word_list]
#     # Ghép lại thành chuỗi hoàn chỉnh
#     return ' '.join(normalized_words)

# input_string = input("Enter a string: ")
# normalized_string = normalize_string(input_string)
# print("Normalized string:", normalized_string)

#cách 2
s = input("Enter a string: ")
print("Normalized string:", s.title())
