from optioncomplete.optioncomplete import autocomplete
from optioncomplete.createAutoOptDatabase import createdatabase
import os
dir=os.path.join(os.environ['HOME'],'.pyautocomplete')
if not os.path.exists(dir):
    os.makedirs(dir)
if not os.path.exists(os.path.join(dir,'autocomplete.db')):
    createdatabase()
