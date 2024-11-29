"""
    여러 공유오피스 베포하기 위한 추가 기능 구현
    id만 추출해서 다음 공유오피스에 넣을 수 있도록 한다. 
    delete_feature은 아직 수정중..
"""

import threading
import time

import cv2
import numpy as np
import torch
import yaml
import os
from torchvision import transforms

from face_alignment.alignment import norm_crop
from face_detection.scrfd.detector import SCRFD
from face_recognition.arcface.model import iresnet_inference
from face_recognition.arcface.utils import compare_encodings, read_features
from face_tracking.tracker.byte_tracker import BYTETracker
from face_tracking.tracker.visualize import plot_tracking

def read_features(feature_path):
    try:
        data = np.load(feature_path + ".npz", allow_pickle=True)
        images_name = data["images_name"]
        images_emb = data["images_emb"]
        return images_name, images_emb
    except:
        return None

def delete_features(path, name):
    images_names, images_embs = read_features(feature_path=path)
    # 삭제할 인덱스를 수집
    indices_to_delete = [i for i in range(img_size) if images_names[i] == name]
    
    # 배열에서 요소 삭제
    images_names = np.delete(images_names, indices_to_delete)
    images_embs = np.delete(images_embs, indices_to_delete)
    np.savez_compressed(features_path, images_name=images_name, images_emb=images_emb)

def copy_features(path, name):
    images_names, images_embs = read_features(feature_path=old_path)
    add_images_embs = []
    for i in range(len(images_names)):
        if images_names[i] == name:
            add_images_embs.append(images_embs[i])

def add_features(features_path, images_emb, name):
    # Read existing features if available
    features = read_features(features_path)

    if features is not None:
        # Unpack existing features
        old_images_name, old_images_emb = features

        images_name = [name for _ in range(len(images_emb))]

        # Combine new features with existing features
        images_name = np.hstack((old_images_name, images_name))
        images_emb = np.vstack((old_images_emb, images_emb))

old_path = "./datasets/face_features/feature"
new_path = "./datasets/face_features/newfeature"

#delete_features(old_path, "iu")
#temp_images_embs = copy_features(old_path, "iu")
#add_freatures(old_path, temp_images_embs, "iu")
# extract(old_path, new_path, "dayun")
