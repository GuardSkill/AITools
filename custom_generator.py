from glob import glob
import numpy as np
from copy import deepcopy
from PIL import Image, ImageOps
import numpy as np
import math

def get_input(path):
    img = Image.open(path)
    return (img)


def preprocess_input(img, rescale=1, rotation_range=0, horizontal_flip=False,target_size=(512, 512), interpolation='nearest'):
    assert target_size[0] >= target_size[1], 'target_size[0] must be >= target_size[1]'
    if rotation_range > 0:
        angle = np.random.choice(range(0, rotation_range))
        img = rotated_image(img,angle)
    if horizontal_flip:
        if np.random.choice(range(0, 2)) > 0:
            img = ImageOps.mirror(img)
    if img.height<=img.width:
        targe_width = int(img.width / img.height * target_size[0])  # get targe[1](width) with same aspect
        img = img.resize((targe_width, target_size[0]), Image.ANTIALIAS)  # resizing with same aspect
        if targe_width >= target_size[1]:
            delta_w = targe_width - target_size[1]
            img = img.crop((delta_w // 2 , 0,img.width - (delta_w - (delta_w // 2))
                            , target_size[0])).convert('RGB')  # left, upper, right, and lower
        elif targe_width < target_size[1]:
            delta_w = target_size[1] - targe_width
            padding = (delta_w // 2, 0, delta_w - (delta_w // 2), 0)
            img = ImageOps.expand(img, padding).convert('RGB')
    else:
        targe_height = int(img.height /img.width  * target_size[1])  # get targe[1](width) with same aspect
        img = img.resize((target_size[1], targe_height), Image.ANTIALIAS)  # resizing with same aspect
        if targe_height>=target_size[0]:
            delta_h = targe_height - target_size[0]
            img = img.crop((0, delta_h // 2,target_size[1],img.height - (delta_h - (delta_h // 2)))).convert('RGB')  
            # left, upper, right, and lower
        elif targe_height < target_size[0]:
            delta_h = target_size[0] - targe_height
            padding = (delta_h // 2, 0,delta_h - (delta_h // 2), 0 )
            img = ImageOps.expand(img, padding).convert('RGB')
    image = np.array(img)
    image = image * rescale
    return (image)


def image_generator(directory, batch_size=4, target_size=(512, 512),
                    rotation_range=0, rescale=1, horizontal_flip=False,
                    interpolation='nearest', seed=None):
    np.random.seed(seed)
    paths = glob('{:s}/**/*.*'.format(directory), recursive=True)
    while True:
        # Select files (paths/indices) for the batch
        batch_paths = np.random.choice(a=paths,size=batch_size)
        batch_input = []
        # Read in each input, perform preprocessing and get labels
        for input_path in batch_paths:
            input = get_input(input_path)
            input = preprocess_input(img=input, rescale=rescale, rotation_range=rotation_range,
                                     horizontal_flip=horizontal_flip,target_size=target_size, interpolation=interpolation)
            batch_input += [input]
        # Return a tuple of (input,output) to feed the network
        batch_x = np.array(batch_input)
        yield batch_x


if __name__ == '__main__':
    import gc
    from keras.preprocessing.image import ImageDataGenerator
    from libs.util import MaskGenerator
    import matplotlib.pyplot as plt

    BATCH_SIZE = 4
    TEST_DIR = r"E:\Dataset\train_img"


    class AugmentingDataGenerator(ImageDataGenerator):
        """Wrapper for ImageDataGenerator to return mask & image"""

        def flow_from_directory(self, directory, mask_generator, rotation_range=0, rescale=1, horizontal_flip=False,
                                seed=None,batch_size=4):
            generator = image_generator(directory, rotation_range=rotation_range, rescale=rescale,
                                        horizontal_flip=horizontal_flip, seed=None)

            # generator = super().flow_from_directory(directory, class_mode=None, *args, **kwargs)
            while True:
                # Get augmentend image samples
                ori = next(generator)

                # Get masks for each image sample
                mask = np.stack([
                    mask_generator.sample(seed)
                    for _ in range(ori.shape[0])], axis=0
                )

                # Apply masks to all image sample
                masked = deepcopy(ori)
                masked[mask == 0] = 1

                # Yield ([ori, masl],  ori) training batches
                # print(masked.shape, ori.shape)
                gc.collect()
                yield [masked, mask], ori


    train_datagen = AugmentingDataGenerator(
        rotation_range=10,
        rescale=1. / 255,
        horizontal_flip=True
    )
    test_datagen = AugmentingDataGenerator(
        rescale=1. / 255,
        horizontal_flip=True)

    # Pick out an example to be send to test samples folder
    test_generator = test_datagen.flow_from_directory(
        TEST_DIR,
        MaskGenerator(512, 512, 3),
        target_size=(512, 512),
        batch_size=BATCH_SIZE,
        seed=42
    )

    test_data = next(test_generator)
    (masked, mask), ori = test_data
    # Show side by side
    for i in range(len(ori)):
        _, axes = plt.subplots(1, 3, figsize=(20, 5))
        axes[0].imshow(masked[i, :, :, :])
        axes[1].imshow(mask[i, :, :, :] * 255)
        axes[2].imshow(ori[i, :, :, :])
        plt.show()
        
def rotated_image(img, angle):
    """
    Given a rectangle of size wxh that has been rotated by 'angle' (in
    radians), computes the width and height of the largest possible
    axis-aligned rectangle (maximal area) within the rotated rectangle.
    """
    w = img.width
    h = img.height
    if w <= 0 or h <= 0:
        return 0, 0
    width_is_longer = w >= h
    side_long, side_short = (w, h) if width_is_longer else (h, w)
    # since the solutions for angle, -angle and 180-angle are all the same,
    # if suffices to look at the first quadrant and the absolute values of sin,cos:
    sin_a, cos_a = abs(math.sin(angle)), abs(math.cos(angle))
    if side_short <= 2. * sin_a * cos_a * side_long or abs(sin_a - cos_a) < 1e-10:
        # half constrained case: two crop corners touch the longer side,
        #   the other two corners are on the mid-line parallel to the longer line
        x = 0.5 * side_short
        wr, hr = (x / sin_a, x / cos_a) if width_is_longer else (x / cos_a, x / sin_a)
    else:
        # fully constrained case: crop touches all 4 sides
        cos_2a = cos_a * cos_a - sin_a * sin_a
        wr, hr = (w * cos_a - h * sin_a) / cos_2a, (h * cos_a - w * sin_a) / cos_2a

    d_w = img.width - wr
    d_h = img.height - hr
    # left, upper, right, and lower
    pad = (d_w // 2, d_h // 2, img.width - (d_w - d_w // 2), img.height - (d_h - d_h // 2))
    img = img.crop(pad)
    return img

