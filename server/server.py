from flask import Flask, request, jsonify
from flask_cors import CORS
from images import image_processing
import uuid
import base64
from keras.src.saving import load_model
from keras.preprocessing import image
import numpy as np
import os
import subprocess

current_dir = os.getcwd()

app = Flask(__name__)

#טעינת המודל
model_Full = load_model('./5ages_model.h5')

# טעינת המחלקה לעיבוד התמונה
image_processor = image_processing()

#   הפונקציה שמקבלת את התמונה מהריאקט ושולחת אותה לעיבוד
# ואז שולחת אותה למודל ומחזירה לריאקט מערך תמונות לגילאים
@app.route('/image', methods=['POST', 'GET'])
def home():
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        image = request.files['file']
        image_processor.delete_all_files_in_folder('image')
        unique_id = uuid.uuid4()
        image.save(f"image/image_{unique_id}.jpg")
        new_path = f"image/image_{unique_id}.jpg"
        image_processor.imagePath = new_path
        image_processor.delete_all_files_in_folder('output')
        image_processor.delete_all_files_in_folder('output1')
        image_processor.delete_all_files_in_folder('outputgray')
        subprocess.run(["python", "images.py"])
        if image_processor.picture_cutting() == 0:
            return "error"
        else:
            image_processor.gray_images(f"output1", f"outputgray")


            return send_image()
    else:
         return "not post"

def send_image():
    base64_images_name = []
    base64_images = []
    agesTree = []
    images_name = []
    ages = []

    i = 0
    image_folder = 'output1'
    image_folder_for_model = 'outputgray'
    for img in os.listdir(image_folder_for_model):
        images_name.append(img)
        print(img)
        image_path = os.path.join(image_folder_for_model, img)
        img = image.load_img(image_path, target_size=(75, 75), color_mode='grayscale')
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)

        prediction_Full = model_Full.predict(img_array)
        prediction_index = np.argmax(prediction_Full)

        print(prediction_index)
        class_names = {0: "elderly", 1: "adult", 2: "young", 3: "teenager", 4: "child", 5: "baby"}


        predicted_label = class_names[prediction_index]
        print(predicted_label)
        ages.append(f"{prediction_index}")


    for img in os.listdir(image_folder):
        i += 1
        image_path = os.path.join(image_folder, img)
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode('utf-8')
            base64_images.append(base64_image)
            base64_images_name.append(img)

    for j in range(i):
        agesTree.append((base64_images[j] ,ages[j]))
    return jsonify(agesTree)

if __name__ == "__main__":
    CORS(app)
    app.run(debug=True)
