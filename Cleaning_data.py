from nltk.tokenize import *
from nltk.corpus import stopwords
from nltk.stem import *
import nltk
from nltk.corpus import movie_reviews



txt = [["Just brought the Crystal Green baby home! :D This is by far the best color realme has ever chosen to work "
        "on!"],['Bck and front cam was amazing'],['Flipkart had scheduled me 11 am exactly by 11 am I got in hand '
                                                  'delivery was best, very good mobile with this cost u can go for '
                                                  'it'],['bad product with good features','good products with bad '
                                                                                          'features']]

filtered_words= []
tokenizer = RegexpTokenizer(r'\w+')
ps = PorterStemmer()
lematizer = WordNetLemmatizer()
for i in txt:
    tokenized = word_tokenize(i[0])
    rem_spec_chars = [tokenizer.tokenize(words)[0] for words in tokenized if len(tokenizer.tokenize(words)) != 0]
    rem_stop_words = [words for words in rem_spec_chars if words not in stopwords.words('english')]
    stemmed_words = [ps.stem(words) for words in rem_stop_words ]
    lematized_words = [lematizer.lemmatize(words) for words in rem_stop_words]
    filtered_words.append(lematized_words)

print 'removed special chars and num from tokens\n',filtered_words


