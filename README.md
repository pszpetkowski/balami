## Balami
***

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/pszpetkowski/balami/blob/master/LICENSE)

***

Balami (`baˈlaːme`) is a mispronunciation of the word salami, which I like very much.
It is also the name of this R&D Python parser that has a goal of a tasty API
manually tailored for the best developer experience.

At the moment I learn as I go and this repository is just a proof-of-concept.
It provides a basic groundwork to allow declarative definitions of parsing rules,
however even that might change in future if it doesn't turn out to be flexible
or efficient enough.
Ideas are being explored and implementation will likely change many times.

Right now I advise you to avoid using code in this repository for your projects.

### Example usage

Right now parser should work fine, besides few corner cases, for import statements:

```
>>> from balami import Parser
>>> source = """
... from somewhere import a as d,   b , c
... import random as r, math as m
... import test
... """
>>> Parser().run(source)
[
  <ImportFromNode(from=somewhere, modules=[<ModuleImportNode(module=a, alias=d)>, <ModuleImportNode(module=b, alias=None)>, <ModuleImportNode(module=c, alias=None)>])>,
  <ImportNode(modules=[<ModuleImportNode(module=random, alias=r)>, <ModuleImportNode(module=math, alias=m)>])>,
  <ImportNode(modules=[<ModuleImportNode(module=test, alias=None)>])>
]
```

### Roadmap

In the coming months I plan to research and develop basic support for Python
expressions and statements and then, step by step, aim for full syntax support.
When that happens and the performance will be satisfying I will release 1.0 version
which will freeze the public API and guarantee stable interface for use in your projects.