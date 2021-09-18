import json
import boto3


def detect_faces(photo, bucket):

    client = boto3.client('rekognition')

    response = client.detect_faces(
        Image={'S3Object': {'Bucket': bucket, 'Name': photo}}, Attributes=['ALL'])

    print('Detected faces for ' + photo)
    for faceDetail in response['FaceDetails']:
        print('The detected face is between ' + str(faceDetail['AgeRange']['Low'])
              + ' and ' + str(faceDetail['AgeRange']['High']) + ' years old')

        print('Here are the other attributes:')
        print(json.dumps(faceDetail, indent=4, sort_keys=True))

        # Access predictions for individual face details and print them
        print("Gender: " + str(faceDetail['Gender']))
        print("Smile: " + str(faceDetail['Smile']))
        print("Eyeglasses: " + str(faceDetail['Eyeglasses']))
        print("Emotions: " + str(faceDetail['Emotions'][0]))

    return len(response['FaceDetails'])


def pushsns(face_count):
    sns_client = boto3.client('sns')
    sns_client.publish(
        TopicArn='arn:aws:sns:ap-northeast-1:065125513144:honsha-konzatsu-sns',
        Subject='出社人数',
        Message="今日の出社人数は"+str(face_count)+"人です",
    )
    return "ok"


def lambda_handler(event, context):
    photo = event['Records'][0]['s3']['object']['key']
    bucket = event['Records'][0]['s3']['bucket']['name']
    face_count = detect_faces(photo, bucket)
    print("Faces detected: " + str(face_count))
    pushsns(face_count)
    print("done")
