import numpy as np
import pickle

import Pred.BuildingMatching as bm
import Pred.LocationCalculation as lc

def get_building_names():
  """
  Generated a reverse dictionary mapping of building id -> building name
  from the building_info dictionary
  """
  data_file = 'Pred/building_info.pkl'

  with open(data_file, "rb") as handle:
    building_info = pickle.load(handle)

  id_to_names = {id:name for name, (id, _, _) in building_info.items()}

  return id_to_names


def predict(my_lat, my_long, my_bearing, image_path):
  valid_buildings = lc.get_valid_buildings(my_long, my_lat, my_bearing)

  print(f"Potential Buildings from GPS Data: {valid_buildings}")

  if len(valid_buildings) == 0:
    return ["Location Error"]
  
  if len(valid_buildings) == 1:
    return valid_buildings

  preds, _, _ = bm.get_building_matches(image_path, valid_buildings)

  name_dict = get_building_names()

  pred_names = [name_dict[id] for id in preds]

  return pred_names

