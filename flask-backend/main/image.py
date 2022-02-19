# from flask import Flask, request, jsonify
# from PIL import Image
# from flask import send_file
# import boto3
# import uuid
# # from werkzeug import secure_filename
#
#
# app = Flask(__name__)
#
# @app.route("/im_size", methods=["POST"])
# def process_image():
#     # file = request.files['image']
#     # # Read the image via file.stream
#     # img = Image.open(file.stream)
#     # # img.save('im-received.jpeg')
#
#     # img_name = str(uuid.uuid4()) + '.jpg'
#     # client = boto3.client('s3', region_name='us-west-2')
#     # # client.upload_fileobj(
#     # #         file,
#     # #         'imagescmpt',
#     # #         file.filename,
#     # #         ExtraArgs={
#     # #             "ACL": acl,
#     # #             "ContentType": file.content_type    #Set appropriate content type as per the file
#     # #         }
#     # #     )
#     # client.upload_file(file, 'imagescmpt', img_name)
#
#
#
#
#
#
#     # return jsonify({'msg': 'success', 'size': [img.width, img.height]})
#
#
#
# if __name__ == "__main__":
#     app.run(debug=True)