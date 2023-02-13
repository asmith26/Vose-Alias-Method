# Vose-Alias-Method
Python implementation of Vose's alias method, an efficient algorithm for sampling from a discrete probability distribution (a good explanation of which can be found at http://www.keithschwarz.com/darts-dice-coins/).

For example, this code can be used for creating and efficiently sampling from a probability distribution representing rolling a weighted die (i.e where side j has probability P(j) of being rolled). Alternatively, it could be used for creating a simple [unigram language model](https://en.wikipedia.org/wiki/Language_model#Unigram_models) (see [example below](#unigram-usage))

Any suggestions/contributions very welcome.

## Installation
`$ pip install Vose-Alias-Method`

Or via conda: `$ conda install -c conda-forge vose-alias-method`


## Depends on:
- The Python Standard Library https://docs.python.org/3/library/)

## Example Usage
In a python shell:

```python
>>> from vose_sampler import VoseAlias
>>> # Create the required probability distribution (here we use the example of a weighted coin with probability H:=Heads=0.2 and T:=Tail=0.8)
>>> dist = {"H":0.2, "T":0.8}
>>> # Create probability and alias tables from the probability distribution, for sampling via Vose's alias method
>>> VA = VoseAlias(dist)
>>> # Generate n random outcomes (here n=10)
>>> VA.sample_n(size=10)
['T', 'T', 'H', 'T', 'T', 'T', 'T', 'H', 'T', 'T']
```

### Unigram language model example
To create a [unigram language model](https://en.wikipedia.org/wiki/Language_model#Unigram_models) for [Alice in Wonderland](http://www.gutenberg.org/cache/epub/11/pg11.txt) and sample 10 words from this, run the main script from the command line with options:

```
$ vose-sampler -p data/Alice.txt -n 10  # or: python vose_sampler/vose_sampler.py -p data/Alice.txt -n 10

Generating 10 random samples:

the
more
she
Rabbit,
say
suddenly
at
soon
thing
solemn
```

[Note, this is intended to illustrate how Vose's alias method could be used. Thus I have not included any preprocessing steps that would make the language model more realistic; for example, we could add handling of upper vs. lower case words (so that e.g. "The" and "the" are not considered distinct), as well as handling of punctuation (e.g. so "the" and "the." are considered the same).]


## Tests
Run via: `$ python setup.py test` (or `$ python tests/tests.py`)

## Build
- `$ python setup.py sdist bdist_wheel`
- `$ twine upload dist/* -r testpypi --skip-existing` assuming twine is installed and *~/.pypirc* exists with something like:
```
[distutils]
index-servers=
    testpypi
    pypi
    
[testpypi]
repository = https://test.pypi.org/legacy/
username = asmith26
password = some_password

[pypi]
repository = https://upload.pypi.org/legacy/
username = asmith26
password = some_harder_password
```

- Assuming everything looks good `$ twine upload dist/*`
- Create new git release `$ git tag <tagname> && git push origin <tag_name>`, and [create a new release](https://github.com/asmith26/Vose-Alias-Method/releases/new) with the same `<tagname>`.
