import markdown
from markdown.util import etree
from markdown.treeprocessors import Treeprocessor
from markdown.postprocessors import Postprocessor
from markdown.preprocessors import Preprocessor
from markdown.blockprocessors import BlockProcessor

class WrapImgTreeprocessor(Treeprocessor):
	def run(self, root):
		# print 'RUNNING'
		# print etree.tostring(root)
		return root

class WrapImgPostprocessor(Postprocessor):
	def run(self, text):
		# print text
		return text

class WrapImgPreprocessor(Preprocessor):
	def run(self, text):
		# print text
		return text

class WrapImgExtension(markdown.Extension):

	def extendMarkdown(self, md, md_globals):
		md.treeprocessors.add("wrapimg", WrapImgTreeprocessor(md), "_begin")
		# md.preprocessors.add("wrapimg", WrapImgPreprocessor(md), "_begin")
		md.postprocessors.add("wrapimg", WrapImgPostprocessor(md), "_begin")
		# md.blockprocessors.add('wrapimg', CodeBlockParser(md), '<code')