# HKLP-Double-Row
generates HK license plates 2 rows

### To run

```sh
python fake_plate_generator.py
```

### Run with arguments to indicate number of images wanted (Default is 1000)
#### '--img_dir', '-id' : put generated image directory
#### '--num_imgs', '-ni' : put number of generated images wanted
#### '--resample', '-r' : put resample value such that it shrinks image by ImageSize/resample and re-enlarges it
#### '--gaussian', '-g' : put range of gaussian blur
#### '--noise', '-n' : put range of noise strength
```sh
python fake_plate_generator.py 3000
```

#### Images are stored in the folder test_plate
#### Background images are randomly selected from the folder "/fake_resources/plate_background_use"
#### Numbers and Lettters are randomly selected from the folder "/fake_resources/numbers" and "/fake_resources/numbers respectively"
