This read-me contains two sets of instructions. 
One is how to reproduce everything from scratch (model, filters, etc.). One is how to simply perform the plagiarism check.
We recommend the first instruction set since the other one is very time consuming

Instructions on performing plagiarism check:
	1) Decide if you want to check plagiarism for the full wikipedia or the simple wikipedia.
		- Full wikipedia requires you to download a model and filters (link below). All files for the simple wikipedia is included in this project.
	2) Download the filters and models and place in project directory (skip if simple wiki)
	3) Run the command "python check_plagiarism.py <mode>", where mode="full" or mode="simple".
	4) Write the path to the file you want to check plagiarism for.
	    - Sample test files are provided in texts/simple/ for simple wiki, and in texts/full/ for full wiki
	    - In each folder there is a file with 100% match, one with close to 0% match and one in between

Instructions on reproducing results
	1) Download the newest Wikipedia XML Dump from: https://dumps.wikimedia.org/enwiki/
	2) Open the python file "make_doc2vec_model.py" and change the path to the XML file to match.
	3) Run "python make_doc2vec_model.py" to train the doc2vec model and save it to disk. This is the most lengthy part of the preprocessing.
	4) Use the "WikiExtractor" library to convert the wikipedia XML dump to plain text.
	5) Open the python file "make_filters.py" and change the path to the model and the extracted Wikipedia to match
	6) Run "python make_filters.py" to cluster wikipedia and make the filters.
	7) Run step 3 and 4 of the first instruction set.

Link to Full Wikipedia Doc2Vec model + filters (2GB total):
	https://drive.google.com/open?id=1Bd67cJ4M3nFYMTTS8X2WPRz3yLl1sK2v

Link to WikiExtractor:
	https://github.com/attardi/wikiextractor