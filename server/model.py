# הפקודות האלו מייבאות את הספריות הנחוצות לניהול הנתונים, לחיזוי ולתהליך הלמידה העמוקה.
import numpy as np
import seaborn as sns
from keras import preprocessing
from keras.preprocessing.image import load_img, img_to_array
from keras.src.legacy.preprocessing.image import ImageDataGenerator
from keras.layers import Dense, Input, Dropout, Flatten, Conv2D, BatchNormalization, Activation, MaxPooling2D
from keras.models import Model, Sequential
from keras.optimizers import Adam
from keras.callbacks import ModelCheckpoint, EarlyStopping
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import itertools
import os
# הגדרת משתנים עבור הנתיבים והפרמטרים הנחוצים לעיבוד התמונות.
base_path = r'./DB/'
pic_size = 75
batch_size = 16


# לולאת for זו ממספרת את מספר התמונות בסט האימון לכל קטגוריה.
for expression in os.listdir(base_path + "train"):
    print(str(len(os.listdir(base_path + "train/" + expression))) + " " + expression + " images")

# יצירת מחוללי נתונים עבור סט האימון והאימות.
datagen_train = ImageDataGenerator()
datagen_validation = ImageDataGenerator()
# קוד זה מגדיר גנרטורים שיכולים להפיק דגמים ממחלקות אימון ובדיקה עבור מודל רשת הנוירונים .
train_generator = datagen_train.flow_from_directory(base_path + "train",
                                                    # גודל תמונה המקורית שיש להקטין אותה (במידה ונדרש) לפני האימון.
                                                    target_size=(pic_size, pic_size),
                                                    # מצב הצבעים של התמונות - במקרה זה, כחום-לבן.
                                                    color_mode="grayscale",
                                                    # גודל הדגמים בכל סדרת.
                                                    batch_size=batch_size,
                                                    # מצב התוויות - במקרה זה, מדובר בתוויות קטגוריות.
                                                    class_mode='categorical',
                                                   # האם לערבב את התמונות בסדרה או לא, באימון ובבדיקה בהתאמה.
                                                    shuffle=True)

validation_generator = datagen_validation.flow_from_directory(base_path + "validation",
                                                              target_size=(pic_size, pic_size),
                                                              color_mode="grayscale",
                                                              batch_size=batch_size,
                                                              class_mode='categorical',
                                                              shuffle=False)

step_size_train = len(train_generator)
step_size_valid = len(validation_generator)
# הגדרת ארכיטקטורת הרשת הנוירונים הפרופילית (CNN) עם שכבות ה-Convolutional ושכבות ה-Fully Connected.
# Define the CNN architecture
nb_classes = 6
 # מציין את גודל הקלט של התמונות הנכנסות לרשת. התמונות נכנסות בגודל 75x75 פיקסלים ועם מצב צבעים של כחום-לבן (1 ערוץ).
input_shape = (75, 75, 1)
# מציין את כך שהמודל הוא מודל סידרתי של שכבות נוירונים.
model = Sequential()
# מוסיף שכבת קלט למודל, המקבלת את התמונות בגודל שהוגדר ב- input_shape.
model.add(Input(shape=input_shape))

# 1st Convolution Layer
#  זהו שכבת הסריקה הראשונה ברשת הנוירונים, המשמשת לזיהוי תכונות מקומיות בתמונות. במקרה זה, משתמשים ב־64 מסננים בגודל 3x3 כדי לסרוק את התמונה. ה־padding המוגדר כ"same" מבצע פילווין כך שגודל התמונה אחרי הסריקה יהיה זהה לגודל המקורי של התמונה.
model.add(Conv2D(64, (3, 3), padding='same'))
#הפעלת פונקציית ה־ReLU (Rectified Linear Unit) אחרי כל שכבת סריקה.
model.add(Activation('relu'))
#עוד שכבת סריקה בעיקרה דומה לשכבה הקודמת.
model.add(Conv2D(64, (3, 3), padding='same'))
#בסך הכול, ברגע שאנו מתאמים את התמונות בסריקה הראשונה, המשקלים של הנוירונים יכולים להיות יחסית לא תואמים. המטרה של Batch Normalization היא להביא את התפלגות הפלט של כל שכבה לסטטיסטיקה סטנדרטית, בכך מקנה לרשת יכולת ללמוד יעיל יותר.
model.add(BatchNormalization())
#שוב, פעולת ReLU מתבצעת לאחר Batch Normalization.
model.add(Activation('relu'))
#Max pooling הוא סוג של שכבת פולינג שמטרתה להפחית את מספר הפרמטרים בתמונה ולהקטין את העומק שלה. במקרה זה, אנו מבצעים Max Pooling בחלון של 2x2. הפונקציה בסך הכול מחליטה עבור כל חלון המקסימום על פיו נבצע הפולינג איזה ערך נשמור מביניהם.
model.add(MaxPooling2D(pool_size=(2, 2)))
#ה־Dropout הוא מנגנון שימושי למניעת התעלמות מפרמטרים ספציפיים בזמן האימון. בכל פעם שהוא מופעל, מספר קבוע של נוירונים (במקרה זה 25%) מנוטרלים באופן רנדומלי. זה עוזר למנוע עבודה יתר על המידה ומעניק לרשת את היכולת להתמודד עם דאגות מקשות כגון התאמה יציבה לנתונים חדשים.
model.add(Dropout(0.25))

model.add(Conv2D(128, (3, 3), padding='same'))
model.add(Activation('relu'))
model.add(Conv2D(128, (3, 3), padding='same'))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))


model.add(Conv2D(256, (3, 3), padding='same'))
model.add(Activation('relu'))
model.add(Conv2D(256, (3, 3), padding='same'))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(Conv2D(256, (3, 3), padding='same'))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))


model.add(Conv2D(512, (3, 3), padding='same'))
model.add(Activation('relu'))
model.add(Conv2D(512, (3, 3), padding='same'))
model.add(BatchNormalization())
model.add(Activation('relu'))
model.add(Conv2D(512, (3, 3), padding='same'))
model.add(BatchNormalization())
model.add(Activation('relu'))


model.add(MaxPooling2D(pool_size=(2, 2)))



# Flatten Layer
model.add(Flatten())

# Fully Connected Layer 1
model.add(Dense(4096))
model.add(Activation('relu'))
model.add(Dropout(0.25))

model.add(Dense(4096))
model.add(Activation('relu'))
model.add(Dropout(0.25))

model.add(Dense(4096))
model.add(Activation('relu'))
model.add(Dropout(0.25))


# Fully Connected Layer 2

# Output Layer
model.add(Dense(nb_classes, activation='softmax'))

# Compile the model
# קימופילציה של המודל עם אופטימיזציה מסוג Adam ופונקציית האבדות הקטגוריאלית הצופה.
#אנו יוצרים אופטימיזר מסוג Adam ומגדירים לו קצב למידה (learning rate) בגודל 0.0001. אופטימיזר הוא אלגוריתם שמשמש לכיוון ולשיפור המשקלים של הרשת הנוירונים בתהליך האימון.
opt = Adam(learning_rate=0.0001)
model.compile(optimizer=opt, loss='categorical_crossentropy', metrics=['accuracy'])
#הפונקציה שמוגדרת כפונקציית ההפסד במודל  היא 'categorical_crossentropy'. זו פונקציית ההפסד המשמשת בעיקר בבעיות של זיהוי קטגוריות מרובות, כמו זיהוי אובייקטים בתמונות.
# Define callbacks
epochs = 15
checkpoint = ModelCheckpoint("model_weights.keras", monitor='val_accuracy', verbose=1, save_best_only=True, mode='max')
early_stopping = EarlyStopping(monitor='val_loss', patience=7, verbose=1, mode='auto')


# הכשרת המודל באמצעות נתוני האימון והאימות.
# Train the model
history = model.fit(train_generator,
                    steps_per_epoch=step_size_train,
                    epochs=epochs,
                    validation_data=validation_generator,
                    validation_steps=step_size_valid

                    )
# שמירת המודל לשימוש עתידי.
model.save('5ages_model.h5')
# #הצגת היסטוריית האימון .
# Plot the evolution of Loss and Accuracy on the train and validation sets
plt.figure(figsize=(20, 10))
plt.subplot(1, 2, 1)
plt.suptitle('Optimizer : Adam', fontsize=10)
plt.ylabel('Loss', fontsize=16)
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.legend(loc='upper right')

plt.subplot(1, 2, 2)
plt.ylabel('Accuracy', fontsize=16)
plt.plot(history.history['accuracy'], label='Training Accuracy')
plt.plot(history.history['val_accuracy'], label='Validation Accuracy')
plt.legend(loc='lower right')
plt.show()

# Compute predictions
predictions = model.predict(validation_generator)
y_pred = [np.argmax(probas) for probas in predictions]
y_test = validation_generator.classes
class_names = list(validation_generator.class_indices.keys())

# Plot confusion matrixs
def plot_confusion_matrix(cm, classes, title='Confusion matrix', cmap=plt.cm.Blues):
    sorted_indices = np.argsort(classes)
    sorted_classes = np.array(classes)[sorted_indices]
    cm = cm[sorted_indices, :][:, sorted_indices]
    cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    plt.figure(figsize=(10, 10))
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    plt.colorbar()
    tick_marks = np.arange(len(sorted_classes))
    plt.xticks(tick_marks, sorted_classes, rotation=45)
    plt.yticks(tick_marks, sorted_classes)

    fmt = '.2f'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")

    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.tight_layout()

cnf_matrix = confusion_matrix(y_test, y_pred)
plot_confusion_matrix(cnf_matrix, classes=class_names, title='Normalized confusion matrix')
plt.show()
