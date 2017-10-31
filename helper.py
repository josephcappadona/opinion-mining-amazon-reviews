from nltk import Tree

# generator to traverse nltk.Tree
def traverse(tree):
  for el in tree:
    if isinstance(el, unicode):
      yield tree
    elif isinstance(el, Tree):
      for leaf in traverse(el):
        yield leaf

