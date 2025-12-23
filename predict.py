import tensorflow as tf
import numpy as np
import cv2

model = tf.keras.models.load_model("model/handwriting_model.h5")

def predict_letter(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    img = cv2.resize(img, (28, 28))
    img = img / 255.0
    img = img.reshape(1, 28, 28)

    prediction = model.predict(img)
    letter_index = np.argmax(prediction)

    return chr(letter_index + ord('A'))

# TEST
if __name__ == "__main__":
    print(predict_letter("sample.png"))
