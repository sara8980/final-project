import cv2
import glob
import os
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

#מחלקה לעיבוד התמונה
class image_processing:

    current_dir = os.getcwd()
    flag = True
    flag2 = True
    imagePath = r"C:\hhh\93.png"
    i = 1

    def picture_cutting(self):
        # הפונקציה משתמשת במודל בינה מלאכותית לזיהוי פרצופים
        # ואז שולחת לפונקציה שתחתוך תמונות לפי הפרצופים שזיהתה
        cascader_file = r"..\haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(cascader_file)
        image = cv2.imread(self.imagePath)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Detect faces in the image
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            flags=cv2.CASCADE_SCALE_IMAGE,
            minSize=(30, 30)
        )

        print("Found {0} faces!".format(len(faces)))
        self.real_face(image, faces)
        return len(faces)

    def real_face(self, image, faces):
        # הפונקציה יוצרת תמונות של פרצופים לפי מה שהםונקציה הקודמת זיהתה
        # הפונקציה עוברת על התמונות שהיא יצרה כדי לזהות שוב את הפרצופים ולמחוק תמונות לא קשורות
        if self.flag2:
            self.flag2 = False
            # Draw a rectangle around the faces
            for (x, y, w, h) in faces:
                cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
                img1 = image[y:y+h, x:x+w]
                cv2.imwrite(f"output/img{self.i}.jpg", img1)
                image_processing.i += 1

        else:
            for (x, y, w, h) in faces:
                cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
                img1 = image[y:y+h, x:x+w]
                cv2.imwrite(f"output1/img{self.i}.jpg", img1)
                image_processing.i += 1


        if self.flag:
            self.flag = False

            outputImages = os.listdir(f'output')

            images = [img for img in outputImages]
            for img in images:
                self.imagePath = f'output/{img}'
                self.picture_cutting()

    def delete_all_files_in_folder(self, folder_path):
        # הפונקציה מוחקת את כל התמונות מהתקיה שהיא קיבלה
        # משמשת כדי למחוק את התמונות של הפרצופים מהשימוש הקודם
        # Get a list of all files in the folder
        files = glob.glob(os.path.join(folder_path, '*'))

        for file in files:
            try:
                # Ensure we are deleting only files
                if os.path.isfile(file):
                    os.remove(file)
                    print(f"Deleted file: {file}")
            except Exception as e:
                print(f"Error deleting file {file}: {e}")

    def gray_images(self, input_folder, output_folder):
        # הפונקציה עוברת על התמונות של הפרצופים ועושה אותם שחור לבן
        # הפונקציה שולחת אחר כך את התמונות לפונקציה שמשנה את גודלם
        # Create the output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # List all files in the input folder
        files = os.listdir(input_folder)

        # Loop through each file
        for file in files:
            # Check if the file is an image (you may want to improve this check)
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.jpeg')):
                # Open the image
                with Image.open(os.path.join(input_folder, file)) as img:
                    # Convert image to RGB mode if it's in Palette mode
                    if img.mode == 'P' or img.mode == 'RGBA':
                        img = img.convert('RGB')

                        # המרת התמונה לצבעי שחור לבן
                    gray_img = self.gray_conversion(np.array(img))
                    # plt.imshow(gray_img, cmap='gray')
                    # plt.show()

                    # Save the image to the output folder
                    Image.fromarray(gray_img).save(os.path.join(output_folder, file))

                    self.resize_images(rf"outputgray", rf"outputgray")

    def gray_conversion(self, image):
        gray_value = 0.33 * image[:, :, 0] + 0.33 * image[:, :, 1] + 0.33 * image[:, :, 2]
        gray_img = gray_value.astype(np.uint8)
        return gray_img


    def resize_images(self, input_folder, output_folder, new_size=(75, 75)):
        #הפונקציה משנה את הגודל של התמונות לגודל 75*75
        # Create the output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        # List all files in the input folder
        files = os.listdir(input_folder)

        # Loop through each file
        for file in files:
            # Check if the file is an image (you may want to improve this check)
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.jpeg')):
                # Open the image
                with Image.open(os.path.join(input_folder, file)) as img:
                    # Convert image to RGB mode if it's in Palette mode
                    if img.mode == 'P' or img.mode == 'RGBA':
                        img = img.convert('RGB')

                    # Resize the image
                    resized_img = img.resize(new_size)

                    # Save the resized image to the output folder
                    resized_img.save(os.path.join(output_folder, file))


