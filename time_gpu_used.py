import time
import gpustat # pip install

def show_memusage(device=0):
    gpu_stats = gpustat.GPUStatCollection.new_query()
    item = gpu_stats.jsonify()["gpus"][device]
    print("{}/{}".format(item["memory.used"], item["memory.total"]))


device = 0
print("before run model:", show_memusage(device=device))
start = time.clock()
#outputs = self.inpaint_model(images, masks) inference
elapsed = (time.clock() - start)
print("after run model:", show_memusage(device=device))
print("Inference Time used:", elapsed)