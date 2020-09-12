import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('hashtag_file.csv/hashtags.csv')

print(df.describe())


 
objects = df.word
y_pos = np.arange(len(objects))
count = df.word_count
 
plt.barh(y_pos, count, align='center', alpha=0.5, color="navy")
plt.yticks(y_pos, objects)
plt.xlabel('Count')
plt.title('Top Ten Hashtag Tweets')
 
plt.show()