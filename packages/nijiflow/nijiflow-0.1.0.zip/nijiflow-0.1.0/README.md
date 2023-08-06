# NijiFlow

NijiFlow is a Python library wrapping TensorFlow and trained NijiNet
models. Its goal is to make it super simple to run 2D-3D image
classifier without any knowledge about deep learning or TensorFlow.


## Installation

NijiFlow can be simply installed from PyPI with pip.
You also need to install TensorFlow to make NijiFlow work.

```
$ pip install --user nijiflow tensorflow
```

Supported Python versions are 2.7 and 3.4+.


## Usage

```py
import nijiflow

image_paths = [...]

classifier = nijiflow.Classifier()
predictions = classifier.classify(image_paths)
for image_path, prediction in zip(image_paths, predictions):
    print('%.3f\t%s' % (prediction, image_path))
```

Prediction values are floating point numbers between 0 and 1.
They will be >=0.5 for 2D images, <0.5 otherwise.


## NijiNet models

NijiFlow is built on top of NijiNets [2]. NijiNets are MobileNet
networks [1] trained for 2D-3D image classification.
Details of NijiNets are described in an article in SIG2D Letters #1.

NijiFlow contains the NijiNet model based on MobileNet v1 (1.0/224),
but the author also provides several trained models with different
parameters. They can be downloaded from following links:

| Network             | Size  | Accuracy | Precision | Recall | Download |
| ------------------- | -----:| --------:| ---------:| ------:| -------- |
| NijiNet (1.0, 224)  |  12MB |    99.1% |     99.7% |  98.5% | [nijinet_1.0_224.pb](https://www.dropbox.com/s/abbz2cgsq5ah902/nijinet_1.0_224.pb?dl=1) |
| NijiNet (1.0, 128)  |  12MB |    98.7% |     99.8% |  97.6% | [nijinet_1.0_128.pb](https://www.dropbox.com/s/raz3q7u5z4lyda5/nijinet_1.0_128.pb?dl=1) |
| NijiNet (0.25, 224) | 0.9MB |    98.5% |     99.7% |  97.4% | [nijinet_0.25_224.pb](https://www.dropbox.com/s/zq8lc1ol3jmwsal/nijinet_0.25_224.pb?dl=1) |


## License

Aapache 2.0


## References

[1] A. G. Howard, M. Zhu, B. Chen, D. Kalenichenko, W. Wang, T. Weyand,
M. Andreetto, and H. Adam. Mobilenets: Efficient convolutional neural
networks for mobile vision applications. CoRR, abs/1704.04861, 2017.

[2] H. Tachibana. NijiFlow: MobileNets に基づくコンパクトな二次元画像判別機.
SIG2D Letters #1, 2017.
