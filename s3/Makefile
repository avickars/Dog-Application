bucket=dog-app-756

bucket-create:
	aws s3 mb bucket --region us-west-2
bucket-list:
	aws s3 ls
file-copy:
	@echo aws s3 cp $(local_file) s3://$(bucket)/$(aws_file)
file-move:
	aws s3 mv $(local_file) s3://$(bucket)/$(aws_file)
file-delete:
	aws s3 rm s3://$(bucket)/$(aws_file)
file-list:
	aws s3 ls $(bucket)
file-get:
	aws s3 cp s3://$(bucket)/$(aws_file) $(local_file) 
bucket-location:make
	aws s3api get-bucket-location --bucket $(bucket)
bucket-update-policy:
	aws s3api put-bucket-policy --bucket $(bucket) --policy file://policy.json
folder-add:
	aws s3 cp --recursive $(local_folder) s3://$(bucket)/$(aws_folder)
folder-move:
	aws s3 mv --recursive $(local_folder) s3://$(bucket)/$(aws_folder)

	