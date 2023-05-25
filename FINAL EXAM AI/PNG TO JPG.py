from PIL import Image
import os

# đường dẫn thư mục chứa ảnh
folder_path = "C:\Wis\AI\data\TEXT DOCUMENT\VIETNAMESE"

# danh sách các tệp tin ảnh trong thư mục
image_files = os.listdir(folder_path)

# sắp xếp các tệp tin theo thứ tự
image_files = sorted(image_files)

# vòng lặp để đổi tên ảnh và đổi định dạng ảnh
for i, file_name in enumerate(image_files):
    # đường dẫn đầy đủ của tệp tin ảnh
    full_path = os.path.join(folder_path, file_name)

    # kiểm tra nếu là tệp tin PNG
    if file_name.endswith('.png'):
        # mở ảnh
        img = Image.open(full_path)

        # đổi tên ảnh và định dạng ảnh
        new_file_name = "VIETNAMESE" + str(i) + ".jpg"
        new_full_path = os.path.join(folder_path, new_file_name)

        # chuyển đổi định dạng ảnh sang JPEG và lưu lại
        img.convert('RGB').save(new_full_path, "JPEG")

        # đóng ảnh
        img.close()

