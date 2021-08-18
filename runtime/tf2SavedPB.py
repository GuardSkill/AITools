import argparse
import glob
import os
import time
import tensorflow as tf
import numpy as np
import PIL.Image
import tf2onnx
from tensorflow.python.compiler.tensorrt.trt_convert import TrtPrecisionMode

from dnnlib import tflib
from training import misc
def get_flist(flist):
    flist = list(glob.glob(flist + '/*.jpg')) + list(glob.glob(flist + '/*.png')) + list(
        glob.glob(flist + '/*.jfif'))
    flist.sort()
    return flist

def SaveFrozenModePB(checkpoint, image, mask, output, truncation):
    # real = np.asarray(PIL.Image.open(image)).transpose([2, 0, 1])
    tf.contrib.resampler
    tflib.init_tf()

    tf.contrib.resampler  # This is effectively importing some more ops
    _, _, Gs = misc.load_pkl(checkpoint)
    # converter = tf.lite.TFLiteConverter.from_saved_model(checkpoint)
    # input_data = tf.constant(1., shape=[1,3,512,512])
    # 转换模型。
    # tf_latent= tf.placeholder(name="tf_latent", dtype=tf.float32, shape=(None,512))
    tf_latent =tf.ones(name="latents_in", dtype=tf.float32, shape=(1,512))
    # label = tf.placeholder(name="label", dtype=tf.float32, shape=(1, 0))

    # img = tf.placeholder(name="img", dtype=tf.float32, shape=(None,3,512, 512))
    img = tf.ones(name="img", dtype=tf.float32, shape=(1, 3, 512, 512))
    # mask = tf.placeholder(name="mask", dtype=tf.float32, shape=(None,1, 512, 512))
    mask = tf.ones(name="mask", dtype=tf.float32, shape=(1, 1, 512, 512))

    out=Gs.get_output_for(tf_latent, None, img, mask, truncation_psi=truncation)[0]
    Gs.print_layers()
    Gs.components['synthesis'].print_layers()
    # print(os.path.curdir)

    # save ckpt and graph
    sess= tf.get_default_session()
    # sess.run(out)
    saver = tf.train.Saver()
    saver.save(sess, '/home/sobey/tensorflowModel.ckpt')
    tf.train.write_graph(sess.graph.as_graph_def(add_shapes=True), '.', '/home/sobey/tensorflowModel.pb', as_text=True)

    # Save Frozen model
    from tensorflow.python.framework.graph_util import convert_variables_to_constants
    graph = convert_variables_to_constants(sess, sess.graph_def, ['Gs/images_out'])  # out为保存网络的最后输出节点名称
    tf.train.write_graph(graph, '.', '/home/sobey/saved_model.pb', as_text=False)
    print([tensor.name for tensor in tf.get_default_graph().as_graph_def().node])



    #########---------------- lite from  frozen mode ---------------------------
    ## Fails becasue BCHW input data_fomat
    # saved_model_dir='/home/sobey/'
    # converter = tf.compat.v1.lite.TFLiteConverter.from_frozen_graph(
    #     saved_model_dir + 'saved_model.pb',
    #     input_arrays=['Gs/latents_in, 'Gs/images_in', 'Gs/masks_in'],
    #     input_shapes={'G_synthesis/dlatents_in': [1,512],'G_synthesis/images_in':[1,3,512, 512],'G_synthesis/masks_in':[1,1, 512, 512]},
    #     output_arrays=['Gs/images_out']
    # )
    # converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir)
    # converter = tf.compat.v1.lite.TFLiteConverter.from_session(
    #     sess, [tf_latent,img,mask], [out])
    # tflite_model = converter.convert()
    # converter.optimizations = [tf.lite.Optimize.DEFAULT]
    # converter.target_spec.supported_types = [tf.lite.constants.FLOAT16]
    # #converter.target_spec.supported_types = [tf.lite.constants.INT8]
    # converter.post_training_quantize = True
    # tflite_fp16_model = converter.convert()
    # tflite_model_fp16_file =  "~/quant_fp16.tflite"
    # # tflite_model_fp16_file = tflite_models_dir/"mnist_model_quant_int8.pb"
    # tflite_model_fp16_file.write_bytes(tflite_fp16_model)
    #########-----------------------------------------------------------------

    #########---------------- tensorRT ---------------------------
    # To tensorRT  (Fail )
    # from tensorflow.python.compiler.tensorrt import trt_convert as trt
    # converter = trt.TrtGraphConverter(
    #     input_graph_def=graph,precision_mode=TrtPrecisionMode.FP16)
    # converter = trt.TrtGraphConverterV2(
    #     input_saved_model_dir='/home/sobey')
    # frozen_graph = converter.convert()
    #########-----------------------------------------------------------------

    # with tf.Session() as sess:
    #     sess.run(tf.global_variables_initializer())
    #     converter = tf.lite.TFLiteConverter.from_session(sess,[tf_latent,img,mask], [out])
    #     tflite_model = converter.convert()
    #     open("converted_model.tflite", "wb").write(tflite_model)

    # ####
    # converter = tf.contrib.lite.TFLiteConverter.from_session(sess, latent,img,mask], [out])
    # tflite_model = converter.convert()
    # open("converted_model.tflite", "wb").write(tflite_model)
    # tflite_model = tf.contrib.lite.toco_convert(Gs.graph_def, [latent,img,mask], [out])
    # open("test.tflite", "wb").write(tflite_model)
    #
    # export_dir = "./tmp_test_saved_model"
    # tf.saved_model.save(Gs, export_dir, to_save)
    #
    # converter = tf.lite.TFLiteConverter.from_saved_model(export_dir)
    # tflite_model = converter.convert()

def create_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--checkpoint', help='Network checkpoint path', required=True)
    parser.add_argument('-i', '--image', help='Original image path', required=True)
    parser.add_argument('-m', '--mask', help='Mask path', required=True)
    parser.add_argument('-o', '--output', help='Output (inpainted) image path', required=True)
    parser.add_argument('-t', '--truncation', help='Truncation psi for the trade-off between quality and diversity. Defaults to 1.', default=None)

    args = parser.parse_args()
    start = time.clock()
    SaveFrozenModePB(**vars(args))
    elapsed = (time.clock() - start)
    print("Whole Time used:", elapsed)

if __name__ == "__main__":
    main()
