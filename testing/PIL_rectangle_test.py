import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from PIL import Image

import json

with open('results.json', 'r') as f:
  data = json.load(f)

im = Image.open('capture.jpg')

# Display the image
plt.imshow(im)

# Get the current reference
ax = plt.gca()


for regions in data['regions']:
    for line in regions['lines']:
        x1, y1, x2, y2 = [int(x) for x in line['boundingBox'].split(",")]
        # Create a Rectangle patch 127,59,144,347
        rect = Rectangle((x1, y1), x2, y2, linewidth=1, edgecolor='r', facecolor='none')
        # Add the patch to the Axes
        ax.add_patch(rect)

plt.show()