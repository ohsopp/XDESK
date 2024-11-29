import argparse
import os
import shutil

import cv2
import numpy as np
import torch
from torchvision import transforms

from face_detection.scrfd.detector import SCRFD
from face_recognition.arcface.model import iresnet_inference
from face_recognition.arcface.utils import read_features

# Check if CUDA is available and set the device accordingly
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Initialize the face detector
detector = SCRFD(model_file="face_detection/scrfd/weights/scrfd_2.5g_bnkps.onnx")

# Initialize the face recognizer
recognizer = iresnet_inference(
    model_name="r100", path="face_recognition/arcface/weights/arcface_r100.pth", device=device)

@torch.no_grad()
def get_feature(face_image):
    """
    Extract facial features from an image using the face recognition model.

    Args:
        face_image (numpy.ndarray): Input facial image.

    Returns:
        numpy.ndarray: Extracted facial features.
    """
    # Define a series of image preprocessing steps
    face_preprocess = transforms.Compose(
        [
            transforms.ToTensor(),
            transforms.Resize((112, 112)),
            transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
        ]
    )

    # Convert the image to RGB format
    face_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2RGB)

    # Apply the defined preprocessing to the image
    face_image = face_preprocess(face_image).unsqueeze(0).to(device)

    # Use the model to obtain facial features
    emb_img_face = recognizer(face_image)[0].cpu().numpy()

    # Normalize the features
    images_emb = emb_img_face / np.linalg.norm(emb_img_face)
    return images_emb

def add_persons(add_persons_dir, features_path, faces_save_dir):
    """
    Add a new person to the face recognition database.

    Args:
        add_persons_dir (str): Directory containing images of the new person.
        features_path (str): Path to save face features.
    """
    # Initialize lists to store names and features of added images
    images_name = []
    images_emb = []

    # Read the folder with images of the new person, extract faces, and save them
    for name_person in os.listdir(add_persons_dir):
        person_image_path = os.path.join(add_persons_dir, name_person)

        # Create a directory to save the faces of the person
        person_face_path = os.path.join(faces_save_dir, name_person)
        os.makedirs(person_face_path, exist_ok=True)
        
        for image_name in os.listdir(person_image_path):
            if image_name.endswith(("jpg")):
                input_image = cv2.imread(os.path.join(person_image_path, image_name))

                # Detect faces and landmarks using the face detector
                bboxes, landmarks = detector.detect(image=input_image)

                # Extract faces
                for i in range(len(bboxes)):
                    # Get the number of files in the person's path
                    number_files = len(os.listdir(person_face_path))

                    # Get the location of the face
                    x1, y1, x2, y2, score = bboxes[i]

                    # Extract the face from the image
                    face_image = input_image[y1:y2, x1:x2]

                    # Path to save the face
                    path_save_face = os.path.join(person_face_path, f"{number_files}.jpg")

                    # Save the face to the database
                    cv2.imwrite(path_save_face, face_image)

                    # Extract features from the face
                    images_emb.append(get_feature(face_image=face_image))
                    images_name.append(name_person)

    # Check if no new person is found
    if images_emb == [] and images_name == []:
        print("No new person found!")
        for sub_dir in os.listdir(add_persons_dir):
            sub_dir_path = os.path.join(add_persons_dir, sub_dir)
            for filename in os.listdir(sub_dir_path):
                delete_file_path = os.path.join(sud_dir_path, filename)
                if os.path.isfile(delete_file_path) :
                    os.unlink(delete_file_path)  # 파일 또는 심볼릭 링크 삭제
            shutil.rmtree(sub_dir_path)  # 폴더 삭제
        return None

    # Convert lists to arrays
    images_emb = np.array(images_emb)
    images_name = np.array(images_name)

    # Read existing features if available
    features = read_features(features_path)

    if features is not None:
        # Unpack existing features
        old_images_name, old_images_emb = features

        # Combine new features with existing features
        images_name = np.hstack((old_images_name, images_name))
        images_emb = np.vstack((old_images_emb, images_emb))

        print("Update features!")

    # Save the combined features
    print(images_name)
    np.savez_compressed(features_path, images_name=images_name, images_emb=images_emb)

    # Remove the data of the new person
    for sub_dir in os.listdir(add_persons_dir):
        dir = os.path.join(add_persons_dir, sub_dir)
        shutil.rmtree(dir);
    if os.path.exists(add_persons_dir):
        shutil.rmtree(add_persons_dir) 

    # Remove the data of the new person
    for sub_dir in os.listdir(faces_save_dir):
        dir = os.path.join(faces_save_dir, sub_dir)
        shutil.rmtree(dir);
    
    print("Successfully added new person!")

def execute():
    add_persons_dir = "./datasets/new_persons"
    features_path = "./datasets/face_features/feature"
    faces_save_dir = "./datasets/data/"

    add_persons(add_persons_dir, features_path, faces_save_dir)

if __name__ == "__main__":
    execute()