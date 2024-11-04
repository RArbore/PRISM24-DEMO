import subprocess, os

CLASS_8K = {(1, 1): 0.628608, (1, 2): 0.63374, (1, 3): 0.64721, (1, 4): 0.64721, (1, 5): 0.631174, (1, 6): 0.619628, (1, 7): 0.586273, (1, 8): 0.586273, (2, 1): 0.0333547, (2, 2): 0.0128287, (2, 3): 0.0224503, (2, 4): 0.0442591, (2, 5): 0.0269403, (2, 6): 0.0153945, (2, 7): 0.020526, (2, 8): 0.0218089, (3, 1): 0.0699166, (3, 2): 0.0673509, (3, 3): 0.0564464, (3, 4): 0.0647851, (3, 5): 0.0724824, (3, 6): 0.0699166, (3, 7): 0.0513149, (3, 8): 0.0622194}
CLUSTER_8K = {(1, 1): 0.5197505379530619, (1, 2): 0.5258278422677438, (1, 3): 0.5348405376521809, (1, 4): 0.5348405376521809, (1, 5): 0.5248307542102685, (1, 6): 0.5210396040247453, (1, 7): 0.5278655433853346, (1, 8): 0.5278655433853346, (2, 1): 0.18428792463417387, (2, 2): 0.17335079149230057, (2, 3): 0.20574008210341083, (2, 4): 0.15364443288709476, (2, 5): 0.1422689782714547, (2, 6): 0.1698782269073038, (2, 7): 0.1913158252862678, (2, 8): 0.16388915485857794, (3, 1): 0.1564721016376119, (3, 2): 0.15296828220907122, (3, 3): 0.11466415435470828, (3, 4): 0.17800891890826917, (3, 5): 0.12535850540012, (3, 6): 0.12131065869383656, (3, 7): 0.14534399964601097, (3, 8): 0.12511469449737248}

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
print("Compiling HD-Classification (26 classes, 617 features, 3072 hypervector dims,", mlc, "MLC bits,", wv, "write-verify cycles).")
print("")
myenv["MLC"] = str(mlc)
myenv["WRITE_VERIFY"] = str(wv)
subprocess.run(["make", "clean"], env=myenv)
subprocess.run(["make", "-j", "host-sim"], env=myenv)
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
print("Compiling HD-Clustering (26 clusters, 617 features, 2048 hypervector dims,", mlc, "MLC bits,", wv, "write-verify cycles).")
print("")
myenv["MLC"] = str(mlc)
myenv["WRITE_VERIFY"] = str(wv)
subprocess.run(["make", "clean"], env=myenv)
subprocess.run(["make", "-j", "host-sim"], env=myenv)
print("")
print("Running HD-Clustering.")
print("")
subprocess.run(["./host-sim", "3"])
subprocess.run(["python3", "mutual_info.py"])
print("")
input("Press enter to exit.")

os.chdir("../..")
subprocess.run("clear")
