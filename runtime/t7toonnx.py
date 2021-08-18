import torch.onnx

from model.sttn import InpaintGenerator

torch_model = InpaintGenerator()
# Load pretrained model weights
model_path = '/Disk1/Projects/AtomProjects/smart_g_video_inpainting_sobey/app/src/AlgorithmPackage/VideoInpainting/checkpoints/CV_VideoInpainting_STTN_YoutubeVOS-v1.0.pth'
batch_size = 1    # just a random number

torch_model = InpaintGenerator()

# Initialize model with the pretrained weights
map_location = lambda storage, loc: storage
if torch.cuda.is_available():
    map_location = None
# torch_model.load_state_dict(model_zoo.load_url(model_path, map_location=map_location))
torch_model.load_state_dict(torch.load(
            model_path, map_location='cpu')['netG'], strict=True)

torch_model.cuda()
# set the model to inference mode
torch_model.eval()

x = torch.randn(1, 5, 3, 240, 432, requires_grad=True).cuda()
x=x
mask = torch.randn(1, 5, 3, 240, 432, requires_grad=True).cuda()
torch_out = torch_model(x,mask)

# Export the model
torch.onnx.export(torch_model,               # model being run
                  x,                         # model input (or a tuple for multiple inputs)
                  "/home/sobey/CV_VideoInpainting_STTN_Onnx32-v1.0.onnx",   # where to save the model (can be a file or file-like object)
                  export_params=True,        # store the trained parameter weights inside the model file
                  opset_version=11,          # the ONNX version to export the model to
                  do_constant_folding=True,  # whether to execute constant folding for optimization
                  input_names = ['input'],   # the model's input names
                  output_names = ['output'], # the model's output names
                  dynamic_axes={'input' : {0 : 'batch_size'},    # variable length axes
                                'output' : {0 : 'batch_size'}})

