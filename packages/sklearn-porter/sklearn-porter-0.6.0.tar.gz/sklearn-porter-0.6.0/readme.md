
# sklearn-porter

[![Build Status](https://img.shields.io/travis/nok/sklearn-porter/stable.svg)](https://travis-ci.org/nok/sklearn-porter)
[![PyPI](https://img.shields.io/pypi/v/sklearn-porter.svg)](https://pypi.python.org/pypi/sklearn-porter)
[![PyPI](https://img.shields.io/pypi/pyversions/sklearn-porter.svg)](https://pypi.python.org/pypi/sklearn-porter)
[![GitHub license](https://img.shields.io/pypi/l/sklearn-porter.svg)](https://raw.githubusercontent.com/nok/sklearn-porter/master/license.txt)
[![Join the chat at https://gitter.im/nok/sklearn-porter](https://badges.gitter.im/nok/sklearn-porter.svg)](https://gitter.im/nok/sklearn-porter?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Transpile trained [scikit-learn](https://github.com/scikit-learn/scikit-learn) estimators to C, Java, JavaScript and others.<br>It's recommended for limited embedded systems and critical applications where performance matters most.


## Machine learning algorithms

<table>
    <tbody>
        <tr>
            <td align="center" width="32%"><strong>Algorithm</strong></td>
            <td align="center" colspan="6" width="68%"><strong>Programming language</strong></td>
        </tr>
        <tr>
            <td align="left" width="32%">Classifier</td>
            <td align="center" width="13%">Java *</td>
            <td align="center" width="11%">JS</td>
            <td align="center" width="11%">C</td>
            <td align="center" width="11%">Go</td>
            <td align="center" width="11%">PHP</td>
            <td align="center" width="11%">Ruby</td>
        </tr>
        <tr>
            <td><a href="http://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html">svm.SVC</a></td>
            <td align="center"><a href="examples/estimator/classifier/SVC/java/basics.ipynb">✓</a>, <a href="examples/estimator/classifier/SVC/java/basics_imported.ipynb">✓ ᴵ</a></td>
            <td align="center"><a href="examples/estimator/classifier/SVC/js/basics.ipynb">✓</a></td>
            <td align="center"><a href="examples/estimator/classifier/SVC/c/basics.ipynb">✓</a></td>
            <td align="center"></td>
            <td align="center"><a href="examples/estimator/classifier/SVC/php/basics.ipynb">✓</a></td>
            <td align="center"><a href="examples/estimator/classifier/SVC/ruby/basics.ipynb">✓</a></td>
        </tr>
        <tr>
            <td><a href="http://scikit-learn.org/stable/modules/generated/sklearn.svm.NuSVC.html">svm.NuSVC</a></td>
            <td align="center"><a href="examples/estimator/classifier/NuSVC/java/basics.ipynb">✓</a>, <a href="examples/estimator/classifier/NuSVC/java/basics_imported.ipynb">✓ ᴵ</a></td>
            <td align="center"><a href="examples/estimator/classifier/NuSVC/js/basics.ipynb">✓</a></td>
            <td align="center"><a href="examples/estimator/classifier/NuSVC/c/basics.ipynb">✓</a></td>
            <td align="center"></td>
            <td align="center"><a href="examples/estimator/classifier/NuSVC/php/basics.ipynb">✓</a></td>
            <td align="center"><a href="examples/estimator/classifier/NuSVC/ruby/basics.ipynb">✓</a></td>
        </tr>
        <tr>
            <td><a href="http://scikit-learn.org/stable/modules/generated/sklearn.svm.LinearSVC.html">svm.LinearSVC</a></td>
            <td align="center"><a href="examples/estimator/classifier/LinearSVC/java/basics.ipynb">✓</a>, <a href="examples/estimator/classifier/LinearSVC/java/basics_imported.ipynb">✓ ᴵ</a></td>
            <td align="center"><a href="examples/estimator/classifier/LinearSVC/js/basics.ipynb">✓</a></td>
            <td align="center"><a href="examples/estimator/classifier/LinearSVC/c/basics.ipynb">✓</a></td>
            <td align="center"><a href="examples/estimator/classifier/LinearSVC/go/basics.ipynb">✓</a></td>
            <td align="center"><a href="examples/estimator/classifier/LinearSVC/php/basics.ipynb">✓</a></td>
            <td align="center"><a href="examples/estimator/classifier/LinearSVC/ruby/basics.ipynb">✓</a></td>
        </tr>
        <tr>
            <td><a href="http://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeClassifier.html">tree.DecisionTreeClassifier</a></td>
            <td align="center"><a href="examples/estimator/classifier/DecisionTreeClassifier/java/basics.ipynb">✓</a>, <a href="examples/estimator/classifier/DecisionTreeClassifier/java/basics_embedded.ipynb">✓ ᴱ</a>, <a href="examples/estimator/classifier/DecisionTreeClassifier/java/basics_imported.ipynb">✓ ᴵ</a></td>
            <td align="center"><a href="examples/estimator/classifier/DecisionTreeClassifier/js/basics.ipynb">✓</a>, <a href="examples/estimator/classifier/DecisionTreeClassifier/js/basics_embedded.ipynb">✓ ᴱ</a></td>
            <td align="center"><a href="examples/estimator/classifier/DecisionTreeClassifier/c/basics.ipynb">✓</a>, <a href="examples/estimator/classifier/DecisionTreeClassifier/c/basics_embedded.ipynb">✓ ᴱ</a></td>
            <td align="center"><a href="examples/estimator/classifier/DecisionTreeClassifier/go/basics.ipynb">✓</a>, <a href="examples/estimator/classifier/DecisionTreeClassifier/go/basics_embedded.ipynb">✓ ᴱ</a></td>
            <td align="center"><a href="examples/estimator/classifier/DecisionTreeClassifier/php/basics.ipynb">✓</a>,  <a href="examples/estimator/classifier/DecisionTreeClassifier/php/basics_embedded.ipynb">✓ ᴱ</a></td></td>
            <td align="center"><a href="examples/estimator/classifier/DecisionTreeClassifier/ruby/basics.ipynb">✓</a>, <a href="examples/estimator/classifier/DecisionTreeClassifier/ruby/basics_embedded.ipynb">✓ ᴱ</a></td>
        </tr>
        <tr>
            <td><a href="http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html">ensemble.RandomForestClassifier</a></td>
            <td align="center"><a href="examples/estimator/classifier/RandomForestClassifier/java/basics_embedded.ipynb">✓ ᴱ</a>, <a href="examples/estimator/classifier/RandomForestClassifier/java/basics_imported.ipynb">✓ ᴵ</a></td>
            <td align="center"><a href="examples/estimator/classifier/RandomForestClassifier/js/basics_embedded.ipynb">✓ ᴱ</a></td>
            <td align="center"><a href="examples/estimator/classifier/RandomForestClassifier/c/basics_embedded.ipynb">✓ ᴱ</a></td>
            <td align="center"></td>
            <td align="center">✓ ᴱ</td>
            <td align="center">✓ ᴱ</td>
        </tr>
        <tr>
            <td><a href="http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.ExtraTreesClassifier.html">ensemble.ExtraTreesClassifier</a></td>
            <td align="center"><a href="examples/estimator/classifier/ExtraTreesClassifier/java/basics_embedded.ipynb">✓ ᴱ</a>, <a href="examples/estimator/classifier/ExtraTreesClassifier/java/basics_imported.ipynb">✓ ᴵ</a></td>
            <td align="center"><a href="examples/estimator/classifier/ExtraTreesClassifier/js/basics.ipynb">✓ ᴱ</a></td>
            <td align="center"><a href="examples/estimator/classifier/ExtraTreesClassifier/c/basics.ipynb">✓ ᴱ</a></td>
            <td align="center"></td>
            <td align="center">✓ ᴱ</td>
            <td align="center">✓ ᴱ</td>
        </tr>
        <tr>
            <td><a href="http://scikit-learn.org/stable/modules/generated/sklearn.ensemble.AdaBoostClassifier.html">ensemble.AdaBoostClassifier</a></td>
            <td align="center"><a href="examples/estimator/classifier/AdaBoostClassifier/java/basics_embedded.ipynb">✓ ᴱ</a>, <a href="examples/estimator/classifier/AdaBoostClassifier/java/basics_imported.ipynb">✓ ᴵ</a></td>
            <td align="center"><a href="examples/estimator/classifier/AdaBoostClassifier/js/basics_embedded.ipynb">✓ ᴱ</a>, <a href="examples/estimator/classifier/AdaBoostClassifier/js/basics_imported.ipynb">✓ ᴵ</a></td>
            <td align="center"><a href="examples/estimator/classifier/AdaBoostClassifier/c/basics_embedded.ipynb">✓ ᴱ</a></td>
            <td align="center"></td>
            <td align="center"></td>
            <td align="center"></td>
        </tr>
        <tr>
            <td><a href="http://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html">neighbors.KNeighborsClassifier</a></td>
            <td align="center"><a href="examples/estimator/classifier/KNeighborsClassifier/java/basics.ipynb">✓</a>, <a href="examples/estimator/classifier/KNeighborsClassifier/java/basics_imported.ipynb">✓ ᴵ</a></td>
            <td align="center"><a href="examples/estimator/classifier/KNeighborsClassifier/js/basics.ipynb">✓</a>, <a href="examples/estimator/classifier/KNeighborsClassifier/js/basics_imported.ipynb">✓ ᴵ</a></td>
            <td align="center"></td>
            <td align="center"></td>
            <td align="center"></td>
            <td align="center"></td>
        </tr>
        <tr>
            <td><a href="http://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.GaussianNB.html#sklearn.naive_bayes.GaussianNB">naive_bayes.GaussianNB</a></td>
            <td align="center"><a href="examples/estimator/classifier/GaussianNB/java/basics.ipynb">✓</a>, <a href="examples/estimator/classifier/GaussianNB/java/basics_imported.ipynb">✓ ᴵ</a></td>
            <td align="center"><a href="examples/estimator/classifier/GaussianNB/js/basics.ipynb">✓</a></td>
            <td align="center"></td>
            <td align="center"></td>
            <td align="center"></td>
            <td align="center"></td>
        </tr>
        <tr>
            <td><a href="http://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.BernoulliNB.html#sklearn.naive_bayes.BernoulliNB">naive_bayes.BernoulliNB</a></td>
            <td align="center"><a href="examples/estimator/classifier/BernoulliNB/java/basics.ipynb">✓</a>, <a href="examples/estimator/classifier/BernoulliNB/java/basics_imported.ipynb">✓ ᴵ</a></td></td>
            <td align="center"><a href="examples/estimator/classifier/BernoulliNB/js/basics.ipynb">✓</a></td>
            <td align="center"></td>
            <td align="center"></td>
            <td align="center"></td>
            <td align="center"></td>
        </tr>
        <tr>
            <td><a href="http://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html">neural_network.MLPClassifier</a></td>
            <td align="center"><a href="examples/estimator/classifier/MLPClassifier/java/basics.ipynb">✓</a>, <a href="examples/estimator/classifier/MLPClassifier/java/basics_imported.ipynb">✓ ᴵ</a></td>
            <td align="center"><a href="examples/estimator/classifier/MLPClassifier/js/basics.ipynb">✓</a>, <a href="examples/estimator/classifier/MLPClassifier/js/basics_imported.ipynb">✓ ᴵ</a></td></td>
            <td align="center"></td>
            <td align="center"></td>
            <td align="center"></td>
            <td align="center"></td>
        </tr>
        <tr>
            <td align="left" width="32%">Regressor</td>
            <td colspan="6" width="68%"></td>
        </tr>
        <tr>
            <td><a href="http://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPRegressor.html">neural_network.MLPRegressor</a></td>
            <td align="center"></td>
            <td align="center"><a href="examples/estimator/regressor/MLPRegressor/js/basics.ipynb">✓</a></td>
            <td align="center"></td>
            <td align="center"></td>
            <td align="center"></td>
            <td align="center"></td>
        </tr>
    </tbody>
</table>

✓ = is full-featured,　ᴱ = with embedded model data,　ᴵ = with imported model data,　* = default language

## Installation

```bash
$ pip install sklearn-porter
```

If you want the [latest changes](https://github.com/nok/sklearn-porter/blob/master/changelog.md#unreleased), you can install the module from the [master](https://github.com/nok/sklearn-porter/tree/master) branch:

```bash
$ pip uninstall -y sklearn-porter
$ pip install --no-cache-dir https://github.com/nok/sklearn-porter/zipball/master
```

## Minimum requirements

```
- python>=2.7.3
- scikit-learn>=0.14.1
```

If you want to transpile a [multilayer perceptron](http://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html), you have to upgrade the scikit-learn package:

```
- python>=2.7.3
- scikit-learn>=0.18.0
```


## Usage

### Export

The following example shows how you can port a [decision tree estimator](http://scikit-learn.org/stable/modules/tree.html#classification) to Java:

```python
from sklearn.datasets import load_iris
from sklearn.tree import tree
from sklearn_porter import Porter

# Load data and train the classifier:
samples = load_iris()
X, y = samples.data, samples.target
clf = tree.DecisionTreeClassifier()
clf.fit(X, y)

# Export:
porter = Porter(clf, language='java')
output = porter.export(embed_data=True)
print(output)
```

The exported [result](examples/estimator/classifier/DecisionTreeClassifier/java/basics_embedded.py#L25-L75) matches the [official human-readable version](http://scikit-learn.org/stable/_images/iris.svg) of the decision tree.

### Prediction

Run the prediction(s) in the target programming language directly:

```python
# ...
porter = Porter(clf, language='java')

# Prediction(s):
Y_java = porter.predict(X)
y_java = porter.predict(X[0])
y_java = porter.predict([1., 2., 3., 4.])
```

### Integrity

Always compute and test the integrity between the original and the transpiled estimator:

```python
# ...
porter = Porter(clf, language='java')

# Accuracy:
integrity = porter.integrity_score(X)
print(integrity)  # 1.0
```


### Command-line interface

First of all have a quick view on the available arguments:

```
$ python -m sklearn_porter [-h] --input <PICKLE_FILE> [--output <DEST_DIR>] \
                           [--class_name <CLASS_NAME>] [--method_name <METHOD_NAME>] \
                           [--c] [--java] [--js] [--go] [--php] [--ruby] \
                           [--export] [--checksum] [--data] [--pipe]
```

The following example shows how you can save an trained estimator to the [pickle format](http://scikit-learn.org/stable/modules/model_persistence.html#persistence-example):

```python
# ...

# Extract estimator:
joblib.dump(clf, 'estimator.pkl')
```

After that the estimator can be transpiled to JavaScript by using the following command:

```
$ python -m sklearn_porter -i estimator.pkl --js
```

The target programming language is changeable on the fly: 

```
$ python -m sklearn_porter -i estimator.pkl --c
$ python -m sklearn_porter -i estimator.pkl --go
$ python -m sklearn_porter -i estimator.pkl --php
$ python -m sklearn_porter -i estimator.pkl --java
$ python -m sklearn_porter -i estimator.pkl --ruby
```

For further processing the argument `--pipe` can be used to pass the result:

```
$ python -m sklearn_porter -i estimator.pkl --js --pipe > estimator.js
```

For instance the result can be minified by using [UglifyJS](https://github.com/mishoo/UglifyJS2):

```
$ python -m sklearn_porter -i estimator.pkl --js --pipe | uglifyjs --compress -o estimator.min.js 
```

Further information will be shown by using the `--help` argument:

```
$ python -m sklearn_porter --help
$ python -m sklearn_porter -h
```


## Development

### Environment

Install the required [environment modules](environment.yml) by executing the script [environment.sh](scripts/environment.sh):

```bash
$ bash ./scripts/environment.sh
```

```bash
#!/usr/bin/env bash

conda env create -c conda-forge -n sklearn-porter python=2 -f environment.yml
source activate sklearn-porter
```

The following compilers or intepreters are required to cover all tests:

- [GCC](https://gcc.gnu.org) (`>=4.2`)
- [Java](https://java.com) (`>=1.6`)
- [PHP](http://www.php.net/) (`>=7`)
- [Ruby](https://www.ruby-lang.org) (`>=2.4.1`)
- [Go](https://golang.org/) (`>=1.7.4`)
- [Node.js](https://nodejs.org) (`>=6`)

### Testing

The tests cover module functions as well as matching predictions of transpiled estimators. Run [all tests](tests) by executing the script [test.sh](scripts/test.sh):

```bash
$ bash ./scripts/test.sh
```

```bash
#!/usr/bin/env bash

python -m unittest discover -vp '*Test.py'
```

The test files have a specific pattern: `'[Algorithm][Language]Test.py'`:

```bash
$ python -m unittest discover -vp 'RandomForest*Test.py'
$ python -m unittest discover -vp '*JavaTest.py'
```

While you are developing new features or fixes, you can reduce the test duration by setting the number of tests:

```bash
$ N_RANDOM_FEATURE_SETS=15 N_EXISTING_FEATURE_SETS=30 python -m unittest discover -vp '*Test.py'
```


### Quality

It's highly recommended to ensure the code quality. For that I use [Pylint](https://github.com/PyCQA/pylint/), which you can run by executing the script [lint.sh](scripts/lint.sh): 

```bash
$ bash ./scripts/lint.sh
```

```bash
#!/usr/bin/env bash

find ./sklearn_porter -name '*.py' -exec pylint {} \;
```


## Citation

If you use this implementation in you work, please add a reference/citation to the paper. You can use the following BibTeX entry:

```
@misc{SkPoDaMo,
  author = {Darius Morawiec},
  title = {sklearn-porter: Transpile trained scikit-learn estimators to C, Java, JavaScript and others},
  url = {https://github.com/nok/sklearn-porter},
  year = {2016--2017}
}
``` 


## License

The module is Open Source Software released under the [MIT](license.txt) license.


## Questions?

Don't be shy and feel free to contact me on [Twitter](https://twitter.com/darius_morawiec) or [Gitter](https://gitter.im/nok/sklearn-porter).
