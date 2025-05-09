# nlp_utils.py

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import spacy
from sentence_transformers import SentenceTransformer, util

# Download NLTK data
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

# Load spaCy model
spacy_model = spacy.load("en_core_web_sm")

# Load Sentence-BERT model
bert_model = SentenceTransformer('all-MiniLM-L6-v2')


def preprocess_nltk(text):
    """Tokenize, lemmatize and remove stopwords."""
    tokens = word_tokenize(text.lower())
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word.isalpha()]
    return set(word for word in tokens if word not in stop_words)


def preprocess_spacy(text):
    """Extract meaningful entities and tokens using spaCy."""
    doc = spacy_model(text)
    keywords = set()

    for ent in doc.ents:
        if ent.label_ in ['ORG', 'PRODUCT', 'WORK_OF_ART', 'PERSON', 'SKILL']:
            keywords.add(ent.text.lower())

    for token in doc:
        if token.pos_ in ['NOUN', 'PROPN', 'VERB'] and not token.is_stop:
            keywords.add(token.lemma_.lower())

    return keywords


def compute_keywords(text, model="nltk"):
    """Unified function to extract keywords based on model."""
    if model == "nltk":
        return preprocess_nltk(text)
    elif model == "spacy":
        return preprocess_spacy(text)
    elif model == "bert":
        return set(text.lower().split())  # fallback for visual output
    else:
        raise ValueError("Invalid model: choose from 'nltk', 'spacy', or 'bert'")


def compute_match(resume_keywords, jd_keywords):
    """Calculate match score and return matched/missing sets."""
    matched = resume_keywords & jd_keywords
    missing = jd_keywords - resume_keywords
    score = round((len(matched) / len(jd_keywords)) * 100) if jd_keywords else 0
    return matched, missing, score


def generate_suggestions(missing_keywords, match_score):
    """Generate tips based on gaps in skills."""
    suggestions = []
    if match_score < 70:
        suggestions.append("Include more relevant skills or keywords from the job description.")
    if {'team', 'collaboration'} & missing_keywords:
        suggestions.append("Add examples of teamwork or collaboration.")
    if 'project' in missing_keywords:
        suggestions.append("Include project work or hands-on experience.")
    return suggestions


def compute_similarity_bert(resume_text, jd_text):
    """Semantic similarity using Sentence-BERT."""
    resume_embed = bert_model.encode(resume_text, convert_to_tensor=True)
    jd_embed = bert_model.encode(jd_text, convert_to_tensor=True)
    similarity = util.pytorch_cos_sim(resume_embed, jd_embed)
    return float(similarity[0][0])
