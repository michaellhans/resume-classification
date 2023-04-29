import joblib
import re
import fitz
import pandas as pd
import datetime
from sklearn.metrics.pairwise import cosine_similarity

class Model:
    def __init__(self):
        # Load all necessary models
        self.database = pd.read_csv("data/data.csv")
        self.word_vectorizer = joblib.load(open('models/resume-classification-word-vectorizer.joblib', 'rb'))
        self.suggestion_vectorizer = joblib.load(open('models/resume-classification-suggestion-vectorizer.joblib', 'rb'))
        self.le = joblib.load(open('models/resume-classification-label-encoder.joblib', 'rb'))
        self.clf = joblib.load(open('models/resume-classification-linear-svc.joblib', 'rb'))
    
    def cleanResume(self, resumeText):
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
    
    def get_full_text(self, filename):
        doc = fitz.open(filename)
        full_text = ""
        for page in doc:
          text = page.get_text()
          full_text += " " + self.cleanResume(text)
        
        return full_text

    def resume_classification(self, paths):
        """
        Classify the resume file into corresponding roles
        """
        texts = []
        for path in paths:
          texts.append(self.get_full_text(path))
        
        text_vector = self.word_vectorizer.transform(texts)   

        # Predict the resume vector with classifier model
        prediction = self.clf.predict(text_vector)
        
        return self.le.inverse_transform(prediction)
    
    def suggestions(self, job_desc):
        suggestion_df = pd.read_csv("data/data.csv")
        full_text = []

        if (len(suggestion_df) == 0):
            raise Exception("No resume stored in database. Please upload first")

        for _, row in suggestion_df.iterrows():
            full_text.append(self.get_full_text('test/' + row['path']))

        full_text_vector = self.suggestion_vectorizer.transform(full_text)
        job_desc_clean = self.cleanResume(job_desc)
        job_desc_vector = self.suggestion_vectorizer.transform([job_desc_clean])

        # Compute cosine similarity matrix
        cosine_sim = cosine_similarity(job_desc_vector, full_text_vector)

        # Sort the resume based on the similarity scores
        suggestion_df['scores'] = [x * 100 for x in cosine_sim[0]]
        sim_scores = list(enumerate(cosine_sim[0]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Get the scores for 5 most similar resume
        sim_scores = sim_scores[:5]

        # Get the movie indices
        movie_indices = [i[0] for i in sim_scores]

        # Return the top 5 most similar resume
        return suggestion_df.iloc[movie_indices]

    def save(self, info):
        id = len(self.database)
        data = {
            "id": id,
            "name": info['name'],
            "path": info['path'],
            "predicted_role": info['predicted_role'],
            "timestamp": str(datetime.datetime.now())
        }

        self.database = self.database._append(data, ignore_index=True)
        self.database.to_csv("data/data.csv", index=False)

        return data

    def reset(self):
        df = pd.DataFrame(columns=self.database.columns)
        self.database = df
        self.database.to_csv("data/data.csv", index=False)


if __name__ == '__main__':
    model = Model()
    predicted_role = model.resume_classification('test/resume-1.pdf')
    info = {
        "name": "Mario Gunawan",
        "path": "test/resume-1.pdf",
        "predicted_role": predicted_role
    }
    model.save(info)