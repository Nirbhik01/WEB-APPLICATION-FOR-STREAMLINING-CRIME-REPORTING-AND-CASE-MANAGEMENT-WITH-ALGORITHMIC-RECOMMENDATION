import pandas as pd
import pickle
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet, words
from nltk import pos_tag

# Load count_vectorizer from the Keyword_extractor directory
count_vectorizer_path = r'C:\Users\ASUS\OneDrive\Documents\notes sixth sem\project\Project Code\Keyword_extractor\count_vectorizer.pkl'
feature_name_path = r'C:\Users\ASUS\OneDrive\Documents\notes sixth sem\project\Project Code\Keyword_extractor\feature_names.pkl'
tfidf_transformer_path = r'C:\Users\ASUS\OneDrive\Documents\notes sixth sem\project\Project Code\Keyword_extractor\tfidf_transformer.pkl'
stop_word_path = r'C:\Users\ASUS\OneDrive\Documents\notes sixth sem\project\Project Code\Keyword_extractor\stop_words.txt'
dictionary_words_path = r'C:\Users\ASUS\OneDrive\Documents\notes sixth sem\project\Project Code\Keyword_extractor\final_dictionary.csv'

count_vectorizer = pickle.load(open(count_vectorizer_path, 'rb'))
feature_names = pickle.load(open(feature_name_path, 'rb'))
tfidf_transformer = pickle.load(open(tfidf_transformer_path, 'rb'))

dictionary_word_list = pd.read_csv(dictionary_words_path, header=None)
dictionary_word_list = set(dictionary_word_list[0].str.strip())

stop_words = pd.read_csv(stop_word_path, header=None)
stop_words = set(stop_words[0].str.strip())


def smart_normalize(word, pos, lemmatizer, stemmer, dictionary_word_list):
    lemma = lemmatizer.lemmatize(word, pos)
    if lemma not in dictionary_word_list:
        return stemmer.stem(word)
    return lemma


def get_wordnet_pos(nltk_pos_tag):
    if nltk_pos_tag.startswith('J'):
        return wordnet.ADJ
    elif nltk_pos_tag.startswith('V'):
        return wordnet.VERB
    elif nltk_pos_tag.startswith('N'):
        return wordnet.NOUN
    elif nltk_pos_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN
    

def preprocess_text(text):
    PUNCTUATION = r"""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""
    lemmatizer = WordNetLemmatizer()
    # dictionary_word_list = set(words.words())
    # stemmer = PorterStemmer()
    # Clean special characters
    text = text.lower()
    text = re.sub(rf"[{re.escape(PUNCTUATION)}]", " ", text)
    # print("-----------------1",text)
    text = re.sub(r'\s+', ' ', text)
    # print("-----------------2",text)
    # Clean numbers
    text = re.sub(r"[^a-zA-Z\s]", "", text)
    # print("-----------------3",text)
    # Tokenize
    tokens = word_tokenize(text)
    # print("-----------------4",tokens)
    # Remove small words
    tokens = [word for word in tokens if len(word) >= 3]
    # print("-----------------5",tokens)
    # Remove stop words
    tokens = [word for word in tokens if word not in stop_words]
    # print("-----------------6",tokens)
    # Remove non-English words

    # Lemmatize with POS tagging
    pos_tags = pos_tag(tokens)
    tokens = [lemmatizer.lemmatize(word, get_wordnet_pos(pos)) for word, pos in pos_tags]
    # print("-----------------8",tokens)
    
    # stemmer = PorterStemmer()
    # tokens = [stemmer.stem(word) for word in tokens]    
    # tokens = [
    #     smart_normalize(word, get_wordnet_pos(pos), lemmatizer, stemmer, dictionary_word_list)
    #     for word, pos in pos_tags
    # ]
    # print("-----------------7",tokens)
    return ' '.join(tokens)


def get_keywords(docs):
    # print(docs)
    try:
        docs = preprocess_text(docs)
        # print(docs)
        # First transform the document using count vectorizer
        count = count_vectorizer.transform([docs])
        
        # Then transform using tfidf transformer
        tfidf_vector = tfidf_transformer.transform(count)
        
        cordinates = tfidf_vector.tocoo()
        tuples = zip(cordinates.col, cordinates.data)
        
        
        features = count_vectorizer.get_feature_names_out()
        # print(features)
        #sorting the vector
        sorted_items = sorted(tuples, key=lambda x: (x[1], x[0]), reverse=True)
        
        # print(sorted_items)
        # extract the top 10 keywords 
        sorted_items = sorted_items[:10]
        
        score_vals = []
        feature_vals = []
        for idx, score in sorted_items:
            score_vals.append(round(score,3))
            feature_vals.append(features[idx])
        
        #create a dictionary of features,score
        results = {}
        for idx in range(len(feature_vals)):
            results[feature_vals[idx]] = score_vals[idx]
        print(results)
        return results
    except Exception as e:
        print(f"Error in get_keywords: {str(e)}")
        print("CountVectorizer fitted:", hasattr(count_vectorizer, 'vocabulary_'))
        print("TfidfTransformer fitted:", hasattr(tfidf_transformer, 'idf_'))
        raise

