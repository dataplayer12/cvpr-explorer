import json
import numpy as np
import spacy
from sklearn.manifold import TSNE
import plotly.graph_objects as go
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State


with open('testfile.txt', 'w') as f:
    f.write('hello world')

# Load the spaCy model
nlp = spacy.load('en_core_web_md')

# Load the data from the JSON file
with open('cvpr_2023_papers.json', 'r') as f:
    data = json.load(f)

# Extract the titles, abstracts, and PDF links
titles = [paper['title'] for paper in data]
abstracts = [paper['abstract'] for paper in data]
pdf_links = [paper['pdf_link'] for paper in data]

# Define the fields and their keywords
fields = {
    'object detection': ['object detection'],
    'segmentation': ['segmentation'],
    'language models': ['language model'],
    'transformers': ['transformer'],
    'ViT': ['ViT'],
    'NeRF': ['NeRF']
}

# Determine the field of each paper
paper_fields = []
for abstract in abstracts:
    field_found = False
    for field, keywords in fields.items():
        if any(keyword in abstract.lower() for keyword in keywords):
            paper_fields.append(field)
            field_found = True
            break
    if not field_found:
        paper_fields.append('other')

# Embed the abstracts in a vector space
embeddings = np.array([nlp(abstract).vector for abstract in abstracts])

# Reduce the dimensionality of the embeddings to 2D using t-SNE
tsne = TSNE(n_components=2, random_state=0, perplexity=10)
embeddings_2d = tsne.fit_transform(embeddings)

# Create a DataFrame with the 2D embeddings, the titles, the fields, and the PDF links
df = pd.DataFrame({
    'x': embeddings_2d[:, 0],
    'y': embeddings_2d[:, 1],
    'title': titles,
    'field': paper_fields,
    'pdf_link': pdf_links,
    'abstract': abstracts
})

# Create a scatter plot of the embeddings
fig = go.Figure()

for field in df['field'].unique():
    df_field = df[df['field'] == field]
    fig.add_trace(go.Scattergl(
        x=df_field['x'],
        y=df_field['y'],
        mode='markers',
        name=field,
        marker=dict(
            size=8
        ),
        text=df_field['title'],
        customdata=df_field[['pdf_link', 'abstract']].values,
        hovertemplate=
        '<b>%{text}</b><br><br>' +
        '<extra></extra>'
    ))

# Set the aspect ratio of the figure to 1 and the background color to white
fig.update_layout(
    autosize=False,
    width=800,
    height=800,
    margin=dict(
        l=50,
        r=50,
        b=100,
        t=100,
        pad=4
    ),
    paper_bgcolor="white",
    plot_bgcolor="white"
)

# Create a Dash application
app = dash.Dash(__name__)

# Define the layout of the application
app.layout = html.Div([
    dcc.Graph(
        id='scatter-plot',
        figure=fig
    ),
    html.Div(id='pdf-link'),
    html.Div(id='abstract')
])

# Define a callback that updates the PDF link and the abstract when a point is clicked
@app.callback(
    [Output('pdf-link', 'children'), Output('abstract', 'children')],
    Input('scatter-plot', 'clickData')
)
def update_link_and_abstract(clickData):
    if clickData is not None:
        href, abstract = clickData['points'][0]['customdata']
        return html.A('Open PDF', href=href, target='_blank'), html.P("Abstract: " + abstract)
    else:
        return '', ''

# Run the application
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=80)
