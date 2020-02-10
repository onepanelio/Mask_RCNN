import json
import csv
import os

# create csv file for inference
def generate_csv(input_file):
	with open(input_file) as f:
		data = json.load(f)

	csv_out = open(os.path.join("/onepanel/output/", "classes.csv"), "w", newline='')

	csv_writer = csv.writer(csv_out)
	csv_writer.writerow(['labels','id'])

	for lbl in data['categories']:
		csv_writer.writerow([lbl['name'], lbl['id']])


if __name__ == '__main__':
	import sys
	generate_csv(sys.argv[1])

	from datetime import datetime
	time = datetime.now()
	stamp = time.strftime("%m%d%Y%H%M%S")
	dataset_name = "MaskRCNN-model-output-{}".format(stamp)
	
	os.system("onepanel datasets create {}".format(dataset_name))
	os.chdir("/onepanel/code/{}".format(dataset_name))
	os.system("mv /onepanel/output/classes.csv /onepanel/code/{}".format(dataset_name))
	for i,_,_ in os.walk("/onepanel/output/logs"):
		if "cvat" in i:
			model_path = i
	os.system("mv model_path/{} /onepanel/code/{}".format('mask_rcnn_cvat_0001.h5','dataset_name'))
	print("\n\n\n")
	print("Dataset Created with Name: {}".format(dataset_name))
