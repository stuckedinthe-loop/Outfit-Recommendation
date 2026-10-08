from PIL import Image
import numpy as np
from sklearn.cluster import KMeans


def analyze_image(uploaded_file):
    """
    Load and preprocess the uploaded image.
    """

    image = Image.open(uploaded_file).convert("RGB")

    # Resize for display and analysis
    image = image.resize((224, 224))

    image_array = np.array(image)

    return image, image_array


def get_dominant_colors(image_array, num_colors=3):
    """
    Extract dominant colors using K-Means clustering.
    """

    # Convert image into list of pixels
    pixels = image_array.reshape(-1, 3)

    # Use KMeans to find dominant colors
    kmeans = KMeans(
        n_clusters=num_colors,
        random_state=42,
        n_init=10
    )

    kmeans.fit(pixels)

    colors = kmeans.cluster_centers_.astype(int)

    return colors

def rgb_to_color_name(rgb):

    r, g, b = rgb

    # Black
    if r < 60 and g < 60 and b < 60:
        return "Black"

    # White
    elif r > 200 and g > 200 and b > 200:
        return "White"

    # Red
    elif r > 150 and g < 100 and b < 100:
        return "Red"

    # Blue
    elif b > r and b > g:
        return "Blue"

    # Green
    elif g > r and g > b:
        return "Green"

    # Grey
    elif abs(r - g) < 20 and abs(g - b) < 20:
        return "Grey"

    # Beige / Light colors
    elif r > 150 and g > 120 and b < 120:
        return "Beige"

    else:
        return "Other"