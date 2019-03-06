import os
import subprocess

TUM_PATH = os.path.join(os.path.expanduser('~'), 'TUM')
ORB_SLAM2_PATH = os.path.join(os.path.expanduser('~'), 'ORB_SLAM2')
EVA_PATH = os.path.join(os.path.expanduser('~'), 'evaluate_ate_scale')
NUM_TEST = 5


TUM_EXECUTABLE = os.path.join(ORB_SLAM2_PATH, 'Examples', 'RGB-D', 'rgbd_tum')
TUM_YAML = os.path.join(ORB_SLAM2_PATH, 'Examples', 'RGB-D', 'TUM{}.yaml')
ORB_VOC = os.path.join(ORB_SLAM2_PATH, 'Vocabulary', 'ORBvoc.txt')
ASSOCIATE_PY = os.path.join(EVA_PATH, 'associate.py')
EVA_PY = os.path.join(EVA_PATH, 'evaluate_ate_scale.py')


all_data = os.listdir(TUM_PATH)


for each_data in all_data:
	if 'freiburg3' in each_data:
		yaml_path = TUM_YAML.format(3)
	elif 'freiburg2' in each_data:
		yaml_path = TUM_YAML.format(2)

	data_path = os.path.join(TUM_PATH, each_data)
	rgb_path = os.path.join(TUM_PATH, each_data, 'rgb.txt')
	depth_path = os.path.join(TUM_PATH, each_data, 'depth.txt')
	gt_path = os.path.join(TUM_PATH, each_data, 'groundtruth.txt')
	asso_path = os.path.join(TUM_PATH, each_data, 'associations.txt')

	trajectory_path = './CameraTrajectory.txt'

	#First associate depth and rgb
	subprocess.Popen("python {} {} {} > {}".format(ASSOCIATE_PY, rgb_path, depth_path, asso_path), shell=True).communicate() 
	for i in range(NUM_TEST):
		plot_name = each_data + '_plot{}.png'.format(i)
		output_file_name = each_data + '_error{}.txt'.format(i)

		if os.path.exists(trajectory_path):
			os.remove(trajectory_path)
			print("Remove previous trajectory file")
		#Run ORBSLAM
		print("Running ORB_SLAM2 {}/{}".format(i+1, NUM_TEST))
		subprocess.Popen("{} {} {} {} {}".format(TUM_EXECUTABLE, ORB_VOC, yaml_path, data_path, asso_path), shell=True).communicate() 

		#Finish
		subprocess.Popen("python {} --plot={} {} {} > {}".format(EVA_PY, 
			plot_name ,
			gt_path, 
			trajectory_path, 
			output_file_name), 
					shell=True).communicate() 
