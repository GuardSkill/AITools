#!/usr/bin/env bash
# Only this scribe can convert the StyleGAN model to Onnx !!!!!!!!!!!!!!!!!!!!!
python -m tf2onnx.convert --graphdef /home/sobey/saved_model.pb --output /home/sobey/model.onnx \
--inputs 'Gs/latents_in':0[1,512],'Gs/images_in':0[1,3,512,512],'Gs/masks_in':0[1,1,512,512] --outputs 'Gs/images_out':0 \
--verbose \
--fold_const \
--opset 11 \
