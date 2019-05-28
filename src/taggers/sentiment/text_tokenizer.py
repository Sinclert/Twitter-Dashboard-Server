# Created by Sinclert Perez (Sinclert@hotmail.com)




class TextTokenizer(object):

	""" Represents the text lemmatizer and tokenizer class """


	def __init__(self):

		""" Creates a text tokenizer object (Unused) """

		self.tokenizer = None
		self.lemmatizer = None
		self.stopwords = None




	def __call__(self, text: str) -> list:

		"""
		Tokenize the specified text

		:param text: phrase to be tokenize
		"""

		tokens = self.tokenizer.tokenize(text)
		tokens = filter(lambda t: t not in self.stopwords, tokens)
		tokens = [self.lemmatizer.stem(token) for token in tokens]

		return tokens
