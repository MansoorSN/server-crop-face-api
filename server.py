from flask import Flask, request, jsonify
from PotraitFace import PotraitFace
from PIL import Image
import base64
import io
import traceback


app=Flask(__name__)

pf=PotraitFace(r"yolov8n-face.pt")


@app.route('/get', methods=['GET'])
def send_message():
        return jsonify({'message': 'use post method'})




@app.route('/process_image', methods=['POST'])
def process_image():
    
    try:
        images_list=[]

        print("got request")
        print(request.files)

        if 'image' not in request.files:
            return jsonify({"error": f"No image file in the request. {request.files}"}), 400

        image_file = request.files['image']
        img = Image.open(image_file.stream).convert('RGB')


        emb=pf.get_embeddings(img)
        coords=pf.get_face_coordinates(emb)
        sub_reslt=pf.get_faces(img,coords)
        
        if sub_reslt==[]:
                return jsonify(f"No faces found. {img}"), 201
        for k in sub_reslt:

            face_image=Image.fromarray(k)
            buffer=io.BytesIO()
            face_image.save(buffer,format='JPEG')
            buffer.seek(0)

            img_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
            images_list.append(img_base64)


        #response_image_list=[array.tolist() for array in images_list]
        return jsonify(images_list),200
    
    except Exception as e:
        traceback.print_exc() 
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)