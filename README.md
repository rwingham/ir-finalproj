# ir-finalproj
Final project for CSE 535 Information Retrieval

## Guide to Files
* pilot.py is the result of the code initially used for the pilot tests.  It counts JSON and non-JSON-like objects and reports timing statistics; it was mostly used to explore the tar file and doesn't form part of the final pipleine.
* bigram.py creates a bigram model from text
* json2model.py is misnamed; it actually scrapes text in the format used in the original CLEF .dat files, then creates ScrapedPage objects which store this text and an associated bigram model
* trainmodels.py goes through a list of files and writes out ScrapedPages to a pickle file.
* runqueries.py takes queries and runs them through all the ScrapedPages in the pickle file, storing the top n with the best perplexity scores and writing out results every 10,000 models seen.  