from pprint import pprint
import nltk
import yaml
import sys
import os
import re
import math
from textblob import TextBlob as tb

def tf(word, blob):
    return blob.words.count(word) / len(blob.words)

def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob)

def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))

def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)

class Splitter(object):

    def __init__(self):
        self.nltk_splitter = nltk.data.load('tokenizers/punkt/english.pickle')
        self.nltk_tokenizer = nltk.tokenize.TreebankWordTokenizer()

    def split(self, text):
        """
        input format: a paragraph of text
        output format: a list of lists of words.
            e.g.: [['this', 'is', 'a', 'sentence'], ['this', 'is', 'another', 'one']]
        """
        sentences = self.nltk_splitter.tokenize(text)
        tokenized_sentences = [self.nltk_tokenizer.tokenize(sent) for sent in sentences]
        return tokenized_sentences


class POSTagger(object):

    def __init__(self):
        pass
        
    def pos_tag(self, sentences):
        """
        input format: list of lists of words
            e.g.: [['this', 'is', 'a', 'sentence'], ['this', 'is', 'another', 'one']]
        output format: list of lists of tagged tokens. Each tagged tokens has a
        form, a lemma, and a list of tags
            e.g: [[('this', 'this', ['DT']), ('is', 'be', ['VB']), ('a', 'a', ['DT']), ('sentence', 'sentence', ['NN'])],
                    [('this', 'this', ['DT']), ('is', 'be', ['VB']), ('another', 'another', ['DT']), ('one', 'one', ['CARD'])]]
        """

        pos = [nltk.pos_tag(sentence) for sentence in sentences]
        #adapt format
        pos = [[(word, word, [postag]) for (word, postag) in sentence] for sentence in pos]
        return pos

class DictionaryTagger(object):

    def __init__(self, dictionary_paths):
        files = [open(path, 'r') for path in dictionary_paths]
        dictionaries = [yaml.load(dict_file) for dict_file in files]
        map(lambda x: x.close(), files)
        self.dictionary = {}
        self.max_key_size = 0
        for curr_dict in dictionaries:
            for key in curr_dict:
                if key in self.dictionary:
                    self.dictionary[key].extend(curr_dict[key])
                else:
                    self.dictionary[key] = curr_dict[key]
                    self.max_key_size = max(self.max_key_size, len(key))

    def tag(self, postagged_sentences):
        return [self.tag_sentence(sentence) for sentence in postagged_sentences]

    def tag_sentence(self, sentence, tag_with_lemmas=False):
        """
        the result is only one tagging of all the possible ones.
        The resulting tagging is determined by these two priority rules:
            - longest matches have higher priority
            - search is made from left to right
        """
        tag_sentence = []
        N = len(sentence)
        if self.max_key_size == 0:
            self.max_key_size = N
        i = 0
        while (i < N):
            j = min(i + self.max_key_size, N) #avoid overflow
            tagged = False
            while (j > i):
                expression_form = ' '.join([word[0] for word in sentence[i:j]]).lower()
                expression_lemma = ' '.join([word[1] for word in sentence[i:j]]).lower()
                if tag_with_lemmas:
                    literal = expression_lemma
                else:
                    literal = expression_form
                if literal in self.dictionary:
                    #self.logger.debug("found: %s" % literal)
                    is_single_token = j - i == 1
                    original_position = i
                    i = j
                    taggings = [tag for tag in self.dictionary[literal]]
                    tagged_expression = (expression_form, expression_lemma, taggings)
                    if is_single_token: #if the tagged literal is a single token, conserve its previous taggings:
                        original_token_tagging = sentence[original_position][2]
                        tagged_expression[2].extend(original_token_tagging)
                    tag_sentence.append(tagged_expression)
                    tagged = True
                else:
                    j = j - 1
            if not tagged:
                tag_sentence.append(sentence[i])
                i += 1
        return tag_sentence

def value_of(sentiment):
    if sentiment == 'positive': return 1
    if sentiment == 'negative': return -1
    return 0

def sentence_score(sentence_tokens, previous_token, acum_score):    
    if not sentence_tokens:
        return acum_score
    else:
        current_token = sentence_tokens[0]
        tags = current_token[2]
        token_score = sum([value_of(tag) for tag in tags])
        if previous_token is not None:
            previous_tags = previous_token[2]
            if 'inc' in previous_tags:
                token_score *= 2.0
            elif 'dec' in previous_tags:
                token_score /= 2.0
            elif 'inv' in previous_tags:
                token_score *= -1.0
        return sentence_score(sentence_tokens[1:], current_token, acum_score + token_score)

def sentiment_score(review):
    return sum([sentence_score(sentence, None, 0.0) for sentence in review])

if __name__ == "__main__":
    
    filename = sys.argv[1]
    if filename == "-h":
        print("Welcome to the text summarization software")
        print(" ")
        print("Use the python script as:")
        print("python newsenti.py <data-file-path>")
        sys.exit()
        
    with open(filename) as f:
	      text=f.readline().replace("."," ")

    with open(filename) as f:
	      for line in f:
		        varline = line.split(".")
		        
    functionwords = []
    with open('Wordlist.txt') as f:
        for word in f:
            word = word.replace("\n","")
            functionwords.append(word)
    text = re.sub("[^A-Za-z0-9 ]+","", text)
    text = text.replace("'","")
    text = text.replace("-","")
    text = text.replace(";","")
    text = text.replace("?","")
    text = text.replace("'","")

    document1 = tb(text)

    bloblist = [document1]
    for i, blob in enumerate(bloblist):
        #print("Top words in document {}".format(i + 1))
        scores = {word: tfidf(word, blob, bloblist) for word in blob.words}

        sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        print("Each word and its TF-IDF score (starting from the highest)")
        print(" ")
        for word, score in sorted_words:
            print("Word: {}, TF-IDF: {}".format(word, round(score, 5)))
        print(" ")

    dicto = {}
    sentscore = []
    for i,item in enumerate(varline[:-1]):
        item = re.sub("[^A-Za-z0-9 ]+","", item)
        
        item = item.replace("'","")
        item = item.replace("-","")
        item = item.replace(";","")
        item = item.replace("?","")
        item = item.replace("'","")
        if item[0] == " ":
            item = item[1:]
        sums = 0
        for word in item.split(" "):
		        if word not in functionwords:
		            sums = sums + abs(scores[word])
        dicto[i]=sums

    #print(dicto)
    
    for item in varline[:-1]:
        text1 = item

        splitter = Splitter()
        postagger = POSTagger()
        dicttagger = DictionaryTagger([ 'dicts/positive.yml', 'dicts/negative.yml', 
                                    'dicts/inc.yml', 'dicts/dec.yml', 'dicts/inv.yml'])

        splitted_sentences = splitter.split(text1)
        #pprint(splitted_sentences)

        pos_tagged_sentences = postagger.pos_tag(splitted_sentences)
        print("The POS tagged sentences to use for sentiment analysis:")
        print(" ")
        pprint(pos_tagged_sentences)
        print(" ")

        dict_tagged_sentences = dicttagger.tag(pos_tagged_sentences)
        #pprint(dict_tagged_sentences)

        
        score = sentiment_score(dict_tagged_sentences)
        sentscore.append(score)
        
    
    averagesentscore = sum(sentscore)/len(sentscore)
    print("The Sentiment analysis score for all sentences in the data:")
    print(" ")
    print(sentscore)
    print(" ")
    
    sorted_dicto = sorted(dicto.items(), key=lambda x: x[1], reverse=True)
    #print(sorted_dicto[2])
    
    howmanylines = math.ceil(0.5 * len(varline))
    
    f = open('Output.txt','w')
    count = 0
    for i,item in enumerate(varline[:-1]):
        for j in sorted_dicto[:howmanylines]:
            if j[0]==i and (sentscore[j[0]]>averagesentscore*2 or sentscore[j[0]]>averagesentscore/2): 
                f.write(varline[i]+".")
                count = count + 1
    
    print("The summarized text is in the output.txt file in the project directory. Thank you for using my software")
    #print("Total sentences in summary"+str(count))
    print(" ")