# Server Setup

This directory is the one which is made to run in the server of your choice

## Ec2 Setup

After launching an instance or while creating, make sure to have
these ports open

5001, 443, 80

1) After launching an instance you can open these ports by heading over to the security group of your instance
2) Under security group there is inbound rules which can be edited
3) Under inbound rules make sure to add custom tcp, http and https ports open as shown below

![alt text](https://github.com/avickars/Dog-Application/blob/main/flask-celery-backend/snaps/ports.png)

4) Once all this is done hop on your instance and run these commands below
```bash
sudo apt upgrade
sudo apt install python3-pip
pip install virtualenv
cd Dog-Application/flask-celery-backend/
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

5) Create a s3 bucket and add the below policy to make it public

```bash
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "AddPerm",
            "Effect": "Allow",
            "Principal": "*",
            "Action": "s3:GetObject",
            "Resource": "arn:aws:s3:::<bucketname>/*"
        }
    ]
}
```

6) Create a Sendgrid account and generate the api key

7) Create .env file in /home/ubuntu/Dog-Application/flask-celery-backend/ and fill up the necessary values from the template given below

```bash
CELERY_BROKER_URL=<your_rabbit_mq_url>
CELERY_RESULT_BACKEND=db+sqlite:///db.sqlite3
SQLALCHEMY_DATABASE_URI=<your_postgres_url>
AWS_ACCESS_KEY_ID=<your_access_id>
AWS_SECRET_ACCESS_KEY=<your_secret_key>
REGION_NAME=<your_desired_region>
SEND_GRID_API_KEY=<your_sendgrid_api_key>
```

## Models
1. Place the model files given in respective folders of 
2. model.pt in flask-celery-backend/dog_detection_demo/
3. vgg19_60_based_model2.pt in flask-celery-backend/breed_classifier/
4. dog-identification-model.pt in flask-celery-backend/dog_identification_demo/


## Cron Setup
1. Place these commands below in cron to make the application running

```bash
* * * * *  bash /home/ubuntu/Dog-Application/flask-celery-backend/autostart_app.sh
* * * * *  bash /home/ubuntu/Dog-Application/flask-celery-backend/autostart_celery.sh
```