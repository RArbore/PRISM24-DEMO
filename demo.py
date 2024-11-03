import subprocess, os

subprocess.run("clear")
print("=========================================")
print("            HD-Classification            ")
print("=========================================")

#TODO: Fill with HD-Classification commands once that's ready.

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
		print("From look-up table, using", mlc, "MLC bits and", wv, "write-verify cycles will achieve", lower_bound, "mutual info score.")
		break

print("")
print("Compiling HD-Clustering.")
print("")
myenv["MLC"] = str(mlc)
myenv["WRITE_VERIFY"] = str(wv)
subprocess.run(["make", "clean", "host-sim"], env=myenv)
subprocess.run(["./host-sim", "3"])
subprocess.run(["python3", "mutual_info.py"])

os.chdir("../..")
