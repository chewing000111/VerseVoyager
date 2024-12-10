from src.db import search
from src.glm import first_step

ask = "关于僧侣和寺庙的诗词"

step_1 = first_step(ask)

print(step_1)

search_rtn = search(step_1)



