import torch
from torchvision import models

import cv2
import h5py

import numpy as np
import sklearn.metrics

# import matplotlib.pyplot as plt

MODEL_FILE = "Pred/CNN Model.pth"
DEVICE = torch.device('cpu')
FEATURES_DIRECTORY = "Pred/CNN Features/"

def load_model():
  """
  Loads CNN model from given .pth file.
  Currently using ResNet-152 pretrained on ImageNet1K w/o finetuning.

  Args:
    None

  Returns:
    resnet_model (torch.nn.Module): resnet model on cpu set to eval mode

  Note:
    - Only to be run on CPU
  """

  resnet_model = torch.load(MODEL_FILE)
  resnet_model.to(DEVICE)
  resnet_model.eval()

  return resnet_model


def get_feature_vector(image_path):
  """
  Generate feature vector for sample image using CNN model.

  Args:
    image_path (str): file to be read in as image

  Returns:
    features (ndarray): feature vector of shape (1, 2048)

  Note:
    - Only to be run on CPU
    - Currently using dummy test directories to work on Colab
  """

  # print(TEST_IMAGE)

  test_image = cv2.imread(image_path)
  test_image = cv2.cvtColor(test_image, cv2.COLOR_BGR2RGB)
  test_image = cv2.resize(test_image, (512, 512))

  test_image = test_image - np.min(test_image, axis=(0, 1))
  test_image = test_image / np.max(test_image, axis=(0, 1))

  # plt.imshow(test_image)

  tensor_image = torch.permute(torch.from_numpy(test_image), (2, 1, 0)).to(DEVICE).float().unsqueeze(0)

  feature_model = load_model()

  features = feature_model(tensor_image).squeeze().cpu().numpy()[np.newaxis,:]
  
  return features


def get_building_matches(image_path, valid_buildings):
  """
  Generate predictions based on pruned set of potential buildings and image

  Args:
    image_path (str): file to be read in as image
    valid_buildings (list): list of building names (str) obtained from 
                            pruning w/ gps and bearing data

  Returns:
    preds (list): list of integer ids corresponding to top predictions

    *currently also returning labels and counts for debugging purposes
    can simply ignore these returns when actually running 
    
    labels (ndarray): array of integer ids seen in top predictions 
    count (ndarray): array of integers of occurences of each id in labels

  Note:
    - Only to be run on CPU
    - Currently using dummy test directories to work on Colab
    - Prediction labels are sorted based on occurrences in top 10 matches
    - Best prediction is presented first in preds
  """

  sample_features = get_feature_vector(image_path)
  
  features_list = []
  ids_list = []

  for building_name in valid_buildings:
    feature_file = f"{FEATURES_DIRECTORY}{building_name} Features.h5"
    with h5py.File(feature_file, 'r') as db:
      features_list.append(db["features"][:])
      ids_list.append(db["id"][:])

  features = np.vstack(features_list)
  ids = np.concatenate(ids_list)

  # print(f"Feature Shape: {sample_features.shape}")
  # print(f"Feature Database Shape: {features.shape}")
  # print(f"Ids Shape: {ids.shape}")

  distances = sklearn.metrics.pairwise_distances(features, sample_features, metric="l1")
  sorted_idx = np.argsort(distances, axis=0)
  top_10 = ids[sorted_idx[:10]]

  labels, count = np.unique(top_10, return_counts=True)

  preds = labels[np.argsort(-count)]

  return list(preds), labels, count

