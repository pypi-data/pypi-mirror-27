onnx-caffe2
========
[![Build Status](https://travis-ci.org/onnx/onnx-caffe2.svg?branch=master)](https://travis-ci.org/onnx/onnx-caffe2)

Caffe2 implementation of Open Neural Network Exchange (ONNX).

Repository location may change.

# Installation

```
pip install onnx-caffe2
```

# Usage

* [ONNX to Caffe2](https://github.com/onnx/tutorials/blob/master/tutorials/OnnxCaffe2Import.ipynb)
* [Caffe2 to ONNX](https://github.com/onnx/tutorials/blob/master/tutorials/Caffe2OnnxExport.ipynb)
* [other end-to-end tutorials](https://github.com/onnx/tutorials)

# Folder Structure

- onnx_caffe2/: the main folder that all code lies under
  - frontend.py: translate from caffe2 model to onnx model
  - backend.py: execution engine that runs onnx on caffe2
- tests/: test files

# Testing

onnx-caffe2 uses [pytest](https://docs.pytest.org) as test driver. In order to run tests, first you need to install pytest:

```
pip install pytest-cov
```

After installing pytest, do

```
pytest
```

to run tests.

# Development

During development it's convenient to install onnx-caffe2 in development mode:

```
git clone  https://github.com/onnx/onnx-caffe2.git
pip install -e onnx-caffe2/
```

# License

[MIT License](LICENSE)

