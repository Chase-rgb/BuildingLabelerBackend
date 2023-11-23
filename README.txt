Prediction.py is the driver code.
The only function that needs to be called is predict(long, lat, bearing, image_path) in Prediction.py which returns a list of building names.

All other code/data files are stored in Pred.

imports.txt just contains all imports used throughout the code. 


MAINTAIN SAME DIRECTORY STRUCTURE AND NAMING
Parts of code have directory structures and file names hardcoded.

Prediction.ipynb is a demo notebook. 



Files needed to run:
Prediction.py
Pred
    -CNN Features (folder)
    -__init__.py
    -building_info.pkl
    -BuildingMatching.py
    -LocationCalculation.py
    -CNN Model.pth
    
*All code assumes that the code is being called from the same directory as Prediction.py

