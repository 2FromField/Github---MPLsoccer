import json
import pandas as pd
from mplsoccer import Pitch
import matplotlib.pyplot as plt



pitch= Pitch(pitch_color='grass', line_color='white')
fig, ax = pitch.draw()
fig.set_size_inches(10,7)
plt.scatter([0],[0], s=100)

plt.show()