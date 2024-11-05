import subprocess, os

CLASS_8K = {(1, 1): 0.628608, (1, 2): 0.63374, (1, 3): 0.64721, (1, 4): 0.64721, (1, 5): 0.631174, (1, 6): 0.619628, (1, 7): 0.586273, (1, 8): 0.586273, (2, 1): 0.0333547, (2, 2): 0.0128287, (2, 3): 0.0224503, (2, 4): 0.0442591, (2, 5): 0.0269403, (2, 6): 0.0153945, (2, 7): 0.020526, (2, 8): 0.0218089, (3, 1): 0.0699166, (3, 2): 0.0673509, (3, 3): 0.0564464, (3, 4): 0.0647851, (3, 5): 0.0724824, (3, 6): 0.0699166, (3, 7): 0.0513149, (3, 8): 0.0622194}
CLUSTER_8K = {(1, 1): 0.5197505379530619, (1, 2): 0.5258278422677438, (1, 3): 0.5348405376521809, (1, 4): 0.5348405376521809, (1, 5): 0.5248307542102685, (1, 6): 0.5210396040247453, (1, 7): 0.5278655433853346, (1, 8): 0.5278655433853346, (2, 1): 0.18428792463417387, (2, 2): 0.17335079149230057, (2, 3): 0.20574008210341083, (2, 4): 0.15364443288709476, (2, 5): 0.1422689782714547, (2, 6): 0.1698782269073038, (2, 7): 0.1913158252862678, (2, 8): 0.16388915485857794, (3, 1): 0.1564721016376119, (3, 2): 0.15296828220907122, (3, 3): 0.11466415435470828, (3, 4): 0.17800891890826917, (3, 5): 0.12535850540012, (3, 6): 0.12131065869383656, (3, 7): 0.14534399964601097, (3, 8): 0.12511469449737248}
CLASS_3K = {(1, 1): 0.418858, (1, 2): 0.436818, (1, 3): 0.430404, (1, 4): 0.430404, (1, 5): 0.47338, (1, 6): 0.406029, (1, 7): 0.408595, (1, 8): 0.408595, (2, 1): 0.0295061, (2, 2): 0.0224503, (2, 3): 0.0288647, (2, 4): 0.0256575, (2, 5): 0.0301475, (2, 6): 0.020526, (2, 7): 0.0288647, (2, 8): 0.00833868, (3, 1): 0.0744067, (3, 2): 0.0898012, (3, 3): 0.0801796, (3, 4): 0.0647851, (3, 5): 0.0737652, (3, 6): 0.091084, (3, 7): 0.0673509, (3, 8): 0.0744067}
CLUSTER_2K = {(1, 1): 0.35266254032103894, (1, 2): 0.35486538539990364, (1, 3): 0.3551589984851035, (1, 4): 0.3551589984851035, (1, 5): 0.35542964828095214, (1, 6): 0.3639382046421232, (1, 7): 0.3780675694930806, (1, 8): 0.3780675694930806, (2, 1): 0.13580144350347903, (2, 2): 0.13435274502468939, (2, 3): 0.14850620225521224, (2, 4): 0.16261388601199106, (2, 5): 0.15456332766746378, (2, 6): 0.1548059698957929, (2, 7): 0.1608169007687904, (2, 8): 0.16768488102157728, (3, 1): 0.14553094335319047, (3, 2): 0.14437470462209234, (3, 3): 0.14751343142888187, (3, 4): 0.15977391137655372, (3, 5): 0.11342177668299419, (3, 6): 0.12172456147773908, (3, 7): 0.14172897202655363, (3, 8): 0.14014495844187516}

subprocess.run("clear")
print("=========================================")
print("            HD-Classification            ")
print("=========================================")

os.chdir("HD-Classification/Hetero-C++")
myenv = os.environ.copy()

while True:
	lower_bound = input("Enter a target test accuracy. ")
	result = subprocess.run(["python3", "lookup_cfg.py", str(lower_bound)], capture_output=True)
	cfg = str(result.stdout).split(" ")
	if "None" in cfg[0]:
		print("Please input a viable test accuracy.")
	else:
		mlc = int(cfg[0].split("'")[1])
		wv = int(cfg[1].split("\\")[0])
		print("From look-up table, using", mlc, "MLC bits and", wv, "write-verify cycles will achieve >=", lower_bound, "test accuracy.")
		break

print("")
input("Press enter to compile.")
print("")
print("Compiling HD-Classification (26 classes, 617 features, 3072 hypervector dims,", mlc, "MLC bits,", wv, "write-verify cycles).")
print("")
myenv["MLC"] = str(mlc)
myenv["WRITE_VERIFY"] = str(wv)
subprocess.run(["make", "-s", "clean"], env=myenv)
subprocess.run(["make", "-s", "-j", "host-sim"], env=myenv)
print("")
print("Running HD-Classification.")
print("")
subprocess.run(["./host-sim", "1"])
print("")
input("Press enter to move on to HD-Clustering.")

os.chdir("../..")
subprocess.run("clear")
print("=========================================")
print("              HD-Clustering              ")
print("=========================================")

os.chdir("HD-Clustering/Hetero-C++")
myenv = os.environ.copy()

while True:
	lower_bound = input("Enter a target mutual info score. ")
	result = subprocess.run(["python3", "lookup_cfg.py", str(lower_bound)], capture_output=True)
	cfg = str(result.stdout).split(" ")
	if "None" in cfg[0]:
		print("Please input a viable mutual info score.")
	else:
		mlc = int(cfg[0].split("'")[1])
		wv = int(cfg[1].split("\\")[0])
		print("From look-up table, using", mlc, "MLC bits and", wv, "write-verify cycles will achieve >=", lower_bound, "mutual info score.")
		break

print("")
input("Press enter to compile.")
print("")
print("Compiling HD-Clustering (26 clusters, 617 features, 2048 hypervector dims,", mlc, "MLC bits,", wv, "write-verify cycles).")
print("")
myenv["MLC"] = str(mlc)
myenv["WRITE_VERIFY"] = str(wv)
subprocess.run(["make", "-s", "clean"], env=myenv)
subprocess.run(["make", "-s", "-j", "host-sim"], env=myenv)
print("")
print("Running HD-Clustering.")
print("")
subprocess.run(["./host-sim", "2"])
subprocess.run(["python3", "mutual_info.py"])
print("")
input("Press enter to exit.")

os.chdir("../..")
subprocess.run("clear")
