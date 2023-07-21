import requests
import json
import numpy as np
import uc
from conf2year import conf2year
import sys

conference_name = sys.argv[1] if len(sys.argv) > 1 else 'cvpr'

# Your OpenAI API key
api_key = uc.NOT_OAI_API

# The URL of the OpenAI embeddings API
url = 'https://api.openai.com/v1/embeddings'

# The headers for the API request
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {api_key}'
}

for year in conf2year[conference_name]:
    print(f'Processing papers for {conference_name} {year}')
    # Load the data from the JSON file
    with open(f'data/{conference_name}_{year}_papers.json', 'r') as f:
        data = json.load(f)

    # Extract the abstracts
    abstracts = [paper['abstract'] for paper in data]

    # Generate embeddings for each abstract
    embeddings = []
    for (idx,abstract) in enumerate(abstracts):
        print(f'Processing abstract {idx+1} of {len(abstracts)}')
        # The data for the API request
        data = {
            'input': abstract,
            'model': 'text-embedding-ada-002'
        }

        # Make the API request
        response = requests.post(url, headers=headers, data=json.dumps(data))

        # Check if the request was successful
        if response.status_code == 200:
            # Extract the embedding from the response
            embedding = response.json()['data'][0]['embedding']
            embeddings.append(embedding)
        else:
            print(f'Error: {response.status_code}')
            print(response.text)

    # Convert the list of embeddings to a NumPy array
    embeddings = np.array(embeddings)

    # Save the embeddings to a .npy file
    np.save(f'data/{conference_name}_{year}_embeddings_openai.npy', embeddings)
