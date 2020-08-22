### Single Image Fréchet Inception Distance (SIFID score)
To calculate the SIFID between real images and their corresponding fake samples, please run:
```
python SIFID/sifid_score.py --path2real <real images path> --path2fake <fake images path> 
```  
Make sure that each of the fake images file name is identical to its cooresponding real image file name. Images should be saved in `.jpg` format.
