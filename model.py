from io import BytesIO
import joblib
import re
import PyPDF2
from PyPDF2 import PdfReader

def cleanResume(resumeText):
    """
    Clean the resume by remove all unnecessary characters
    """ 
    resumeText = re.sub('http\S+\s*', ' ', resumeText)  # remove URLs
    resumeText = re.sub('RT|cc', ' ', resumeText)  # remove RT and cc
    resumeText = re.sub('#\S+', '', resumeText)  # remove hashtags
    resumeText = re.sub('@\S+', '  ', resumeText)  # remove mentions
    resumeText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', resumeText)  # remove punctuations
    resumeText = re.sub(r'[^\x00-\x7f]',r' ', resumeText) 
    resumeText = re.sub('\s+', ' ', resumeText)  # remove extra whitespace
    return resumeText

def resume_classification(filename):  
    # Creating a pdf reader object
    file = open(filename, 'rb')
    reader = PdfReader(file)
    text = ""

    # Extracting text from page
    for page in reader.pages:
        text = page.extract_text()
        text += cleanResume(text)

    file.close()

    # Load all necessary models
    word_vectorizer = joblib.load(open('models/resume-word-vectorizer.sav', 'rb'))
    le = joblib.load(open('models/resume-label-encoder.sav', 'rb'))
    clf = joblib.load('models/resume-classification.sav')
    text_vector = word_vectorizer.transform([cleanResume(text)])

    # Predict the resume vector with classifier model
    prediction = clf.predict(text_vector)
    
    return le.inverse_transform(prediction)[0]

if __name__ == '__main__':
    print(resume_classification('test/resume-1.pdf'))