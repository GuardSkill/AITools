import argparse
import glob
import os
import time
import cv2
import PIL.ImageOps
import numpy as np
import PIL.Image
import onnxruntime as ort


# test on onnxruntime 1.1.0

def adjust_dynamic_range(data, drange_in, drange_out):
    if drange_in != drange_out:
        scale = (np.float32(drange_out[1]) - np.float32(drange_out[0])) / (
                    np.float32(drange_in[1]) - np.float32(drange_in[0]))
        bias = (np.float32(drange_out[0]) - np.float32(drange_in[0]) * scale)
        data = data * scale + bias
    return data


def get_flist(flist):
    flist = list(glob.glob(flist + '/*.jpg')) + list(glob.glob(flist + '/*.png')) + list(
        glob.glob(flist + '/*.jfif'))
    flist.sort()
    return flist


def infer_from_images(checkpoint, image, mask, output, accurate, invert_mask=0, save_flag=1):
    # real = np.asarray(PIL.Image.open(image)).transpose([2, 0, 1])

    latent = np.random.randn(1, 512).astype(np.float32)
    sess = ort.InferenceSession(checkpoint)
    # ,provider_options=[{"device_id": -1, "cuda_mem_limit": 1024}])
    option = {'device_id': 0}
    # print(ort.get_available_providers())
    # print(sess.get_providers())
    # ORT version>=1.5
    # sess.set_providers(['CUDAExecutionProvider'], [option])

    if os.path.isdir(image):
        if os.path.isfile(output) or not os.path.isdir(mask):
            print("ALL paths should be the folder, or all are image paths")
            return -1
        create_dir(output)
        img_list = get_flist(image)
        mask_list = get_flist(mask)
        # mask_list=mask_list + [mask_list[-1]] * (len(img_list) - len(mask_list))
        if len(mask_list) < len(img_list):
            mask_list = mask_list * int((len(img_list) - len(mask_list)) / len(mask_list)) \
                        + [mask_list[-1]] * ((len(img_list) - len(mask_list)) % len(mask_list))
        elif len(mask_list) > len(img_list):
            img_list = img_list * int((len(mask_list) - len(img_list)) / len(img_list)) \
                       + [img_list[-1]] * ((len(mask_list) - len(img_list)) % len(img_list))

        infer_start = time.perf_counter()

        for (image, mask) in zip(img_list, mask_list):
            raw_img = PIL.Image.open(image).convert('RGB')
            input_img = raw_img.resize((512, 512))
            temp = output + '/Input'

            # Save input image
            if save_flag:
                create_dir(temp)
                input_img.save(os.path.join(temp, os.path.basename(image)))

            real = np.asarray(input_img).transpose([2, 0, 1])
            real = adjust_dynamic_range(real, [0, 255], [-1, 1])
            raw_mask = PIL.Image.open(mask).convert('1')
            if invert_mask:
                raw_mask = raw_mask.convert('L')
                raw_mask = PIL.ImageOps.invert(raw_mask)
                raw_mask = raw_mask.convert('1')
            mask = np.asarray(raw_mask.resize((512, 512)), dtype=np.float32)[np.newaxis]
            mask = (mask > 0.5).astype(np.float32)

            # Save damaged image
            if save_flag:
                damaged = real * mask + (1 - mask) * 1
                damaged = adjust_dynamic_range(damaged, [-1, 1], [0, 255])
                temp = output + '/Damaged'
                create_dir(temp)
                PIL.Image.fromarray(damaged.clip(0, 255).astype(np.uint8).transpose([1, 2, 0])).save(
                    os.path.join(temp, os.path.basename(image)))

            # Save Mask map
            if save_flag:
                temp = output + '/Mask'
                create_dir(temp)
                save_mask=adjust_dynamic_range(mask, [0, 1], [0, 255])
                PIL.Image.fromarray(save_mask.astype(np.uint8).squeeze()).save(os.path.join(temp, os.path.basename(image)))

            if int(accurate) == 16:
                latent = latent.astype(np.float16)
                real = real.astype(np.float16)
                mask = mask.astype(np.float16)
            # input_name = sess.get_inputs()[0].name
            fake = sess.run(['Gs/images_out:0'], {'Gs/latents_in:0': latent, 'Gs/images_in:0': real[np.newaxis],
                                                  'Gs/masks_in:0': mask[np.newaxis]})
            # print("Inference success")
            fake = fake[0].astype(np.float64).squeeze()
            fake = adjust_dynamic_range(fake, [-1, 1], [0, 255])
            fake = fake.clip(0, 255).astype(np.uint8).transpose([1, 2, 0])

            raw_mask = np.asarray(raw_mask, dtype=np.float32)[np.newaxis].transpose(
                [1, 2, 0])
            fake = cv2.resize(fake, dsize=(raw_mask.shape[1], raw_mask.shape[0]), interpolation=cv2.INTER_CUBIC)
            raw_mask = (raw_mask > 0.5).astype(np.float32)
            composite = fake * (1 - raw_mask)  + raw_img * raw_mask

            composite = PIL.Image.fromarray(composite.clip(0, 255).astype(np.uint8))
            temp = output + '/Out'
            create_dir(temp)
            composite.save(os.path.join(temp, os.path.basename(image)))
            print("Save successful for",os.path.basename(image))
        infer_elapsed = (time.perf_counter() - infer_start)
        print("Inference Time used:", infer_elapsed, "image numerbers:", len(img_list))



    else:
        print("Please input the directory as the params.")
        return -1


def create_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--checkpoint', help='Network checkpoint path', default=None)
    parser.add_argument('-i', '--image', help='Original image path', required=True)
    parser.add_argument('-m', '--mask', help='Mask path', required=True)
    parser.add_argument('-o', '--output', help='Output (inpainted) image path', required=True)
    parser.add_argument('-acc', '--accurate', help='Output (inpainted) image path', default=32)
    parser.add_argument('-inv', '--invert_mask', help='If invert the mask', default=0)
    parser.add_argument('-s', '--save_flag', help='Save mask and input', default=0)
    # parser.add_argument('-t', '--truncation', help='Truncation psi for the trade-off between quality and diversity. Defaults to 1.', default=None)

    args = parser.parse_args()
    if int(args.accurate) == 16 and args.checkpoint == None:
        args.checkpoint = "/home/sobey/model_f16.onnx"
    start = time.perf_counter()
    infer_from_images(**vars(args))
    elapsed = (time.perf_counter() - start)
    print("Whole Time used:", elapsed)


if __name__ == "__main__":
    main()
