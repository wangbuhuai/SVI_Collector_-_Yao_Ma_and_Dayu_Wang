from serpapi import GoogleSearch

params = {
  "engine": "google_trends",
  "q": "coffee,milk,bread,pasta,steak",
  "data_type": "TIMESERIES",
  "api_key": "86810ee7cdd61b10b3ef56614c09662b3f0d0b158f864731e5d1dd337bf5f7f4"
}

search = GoogleSearch(params)
results = search.get_dict()
interest_over_time = results["interest_over_time"]

