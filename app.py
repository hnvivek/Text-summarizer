import streamlit as st

# UI
def main():

# Defining UI Code
	st.set_page_config(
     page_title="Text summarizer",
     page_icon="🧊",
     #layout="wide",
     initial_sidebar_state="expanded")

	html_temp = """
    <div style="background-color:#a2d0c1;padding:5px">
    <h1 style="color:white;text-align:center;"> Text Summarizer App </h1>

    </div>
    """
	st.markdown(html_temp,unsafe_allow_html=True)
	st.subheader("Enter the text to summarize")
	
	text = st.text_area("",height=300)
	key = st.button("Summarize")

	if (len(text)>0 or key):

# ML Code

		import spacy
		from spacy.lang.en.stop_words import STOP_WORDS
		from string import punctuation
		import math
		import en_core_web_sm

		#loading
		nlp = en_core_web_sm.load()

		text= text.replace('\n', '')

		doc=nlp(text)

		# creating tokens
		tokens = [token.text for token in doc]

		pun = punctuation+'\n'

		wordfreq = {}

		# counting the work frequency
		for word in doc:
		  if word.text.lower() not in STOP_WORDS:
		    if word.text.lower() not in pun:
		      if word.text not in wordfreq.keys():
		        wordfreq[word.text]=1
		      else:
		        wordfreq[word.text]+=1

		max_freq = max(wordfreq.values())

		# Normalizing
		for word in wordfreq.keys():
		  wordfreq[word]=wordfreq[word]/max_freq

		# creating sentences tokens
		sent_tokens = [sent for sent in doc.sents]

		sent_score={}

		# Calculating thr sentence scores
		for sent in sent_tokens:
		  for word in sent:
		    if word.text.lower() in wordfreq.keys():
		      if sent not in sent_score.keys():
		        sent_score[sent]=wordfreq[word.text.lower()]
		      else:
		        sent_score[sent]+=wordfreq[word.text.lower()]

		# Choosing sentences with high score
		from heapq import nlargest

		st.subheader("Define the Summary length")

		level = st.selectbox("",options =['short','medium','long'])


		if level == 'short':
			length = 0.10
		elif level== 'medium':
			length =0.30
		else:
			length=0.60

		n=math.ceil(len(sent_score) * length)

		summary = nlargest(n,iterable=sent_score,key=sent_score.get)

		final_summary = [word.text for word in summary]

		summary=" ".join(final_summary)

		html_Summary = """
	    <div style="background-color:#a2d0c1;padding:2px">
	    <h3 style="color:white;text-align:center;"> Generated Summary </h3>

	    </div>
	    </br>
	    """

		st.markdown(html_Summary,unsafe_allow_html=True)
		st.markdown(summary)



if __name__=='__main__':
    main()


