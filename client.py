import base64
import requests
from PIL import Image
from io import BytesIO
import numpy as np

# The Flask server endpoint
url = 'http://127.0.0.1:5000/process_image'
#url = 'http://172.17.0.2:5000/process_image'

# Path to the image file to send
image_path = r'C:\Users\snman\Desktop\2024\Learn\Streamlit\media\k6.jpg'

# Send the image using POST request
img=Image.open(image_path).resize((640,640)).convert('RGB')
#img = Image.new('RGB', (640, 640), color='red')
print(img)


image_io = BytesIO()
img.save(image_io, 'JPEG')
image_io.seek(0)

files = {'image': ('image.jpg', image_io, 'image/jpeg')}
print(files)
#response = requests.post(url, files=files, headers={'Content-Type': 'multipart/form-data'})
response = requests.post(url, files=files)
response.raise_for_status()  # Ensure the response status is OK

print("got response from server")
#print(response.text)
# Check if the response was successful
if response.status_code == 200:
    images_list = response.json()
    
    print(f"Received {len(images_list)} cropped images.")

    #print(len(images_list))

    for i, img_data in enumerate(images_list):
        print(f"{i} : {np.array(img_data).shape}")

    print(f"Received {images_list}")
    # Loop over the received images and display/save them
    for i, img_data in enumerate(images_list):
        # Assuming the server returns base64-encoded images
        img_data = base64.b64decode(img_data)
        img = Image.open(BytesIO(img_data))
        #img = Image.fromarray(np.array(img_data).astype(np.uint8))
        
        # Save the image or display it (e.g., using PIL)
        img.save(f'cropped_image_{i}.jpg')
        img.show()  # This will open the image using your default viewer
else:
    print(f"Error: {response.status_code}, {response.text}")
