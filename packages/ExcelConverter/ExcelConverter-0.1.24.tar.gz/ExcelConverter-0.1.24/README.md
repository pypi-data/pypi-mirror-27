TODO: marker for old file

Deployment to pypi:
Ref: https://tom-christie.github.io/articles/pypi/

1) Increment the version in the file version.py

2) Create the distribution package:
python setup.py sdist

3) Use twine to upload it to pypi (ensure it's installed):
twine upload -r test dist/PACKAGENAME-VERSION.tar.gz

