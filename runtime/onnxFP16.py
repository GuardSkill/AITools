

from onnxruntime.quantization import quantize_qat, QuantType

model_fp32 = '/home/sobey/model.onnx'
model_quant = '/home/sobey/model_fp16.onnx'
quantized_model = quantize_qat(model_fp32, model_quant)
print("saved model in ", model_quant)

def converto_fp16():# Update the input name and path for your ONNX model
    import onnxmltools
    from onnxmltools.utils.float16_converter import convert_float_to_float16
    input_onnx_model = '/home/sobey/model.onnx'

    # Change this path to the output name and path for your float16 ONNX model
    output_onnx_model = '/home/sobey/model_f16.onnx'


    # Load your model

    onnx_model = onnxmltools.utils.load_model(input_onnx_model)

    # Convert tensor float type from your input ONNX model to tensor float16
    onnx_model = convert_float_to_float16(onnx_model)

    # Save as protobuf
    onnxmltools.utils.save_model(onnx_model, output_onnx_model)
    print("saved model in ",output_onnx_model)
converto_fp16()