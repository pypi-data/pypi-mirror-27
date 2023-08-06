## pre-install

```
pip install twine # for uploading project distribution
```

## setting

```
[distutils]
index-servers=
    pypi
    testpypi

[testpypi]
repository: https://test.pypi.org/legacy/
username: USERNAME
password: PASSWORD

[pypi]
repository: 
```
