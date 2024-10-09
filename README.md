# My portfolio consists of four segments:

# 1.) A splash page with an intro to myself and links to relevant resources
# 2.) An agglomerative clustering app
- App was built to showcase some basic unsuperzised ML skills using a Kaggle dataset.
- Agglomerative clustering app loads 1_000_000 rows of crash data into cache, each run of the model randomly samples n of those 1_000_000 rows.
- Uses pyarrow data format to be more performant in the data load and sample functions.
# 3.) An LLM integration app
- This app was borne of an idea I had to create a tool to generate Toastmasters meeting conversation topics.
- Azure OpenAI gpt-35-turbo-16k model optimized for the use case.
# 4.) An Rshiny web app
- Explores the interaction of car prices and mileage at time of sale using a Kaggle dataset.
- Hosted in shinyapps.io and presented in Streamlit through an iframe.

# 
# Architecture:
## Streamlit web app packaged in a Docker container for cross-platform compatibility and scalability. Utilizes Azure Container Registry and Azure App Service.
See the app at: https://www.portfolio-callahan.com/

