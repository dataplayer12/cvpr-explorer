import json
import numpy as np
import spacy
from sklearn.manifold import TSNE
import plotly.graph_objects as go
import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import os
from conf2year import conf2year

conferences=list(conf2year.keys())

# Load the data for all years
data = {}
embeddings = {}
for conference in conferences:
    years = conf2year[conference]
    for year in years:
        # Load the data from the JSON file
        with open(f'data/{conference}_{year}_papers.json', 'r') as f:
            data[(conference, year)] = json.load(f)
        
        # Load the embeddings
        embeddings[(conference, year)] = np.load(f'data/{conference}_{year}_embeddings_openai.npy')

# Define the fields and their keywords
fields = {
    'object detection': ['object detection'],
    'segmentation': ['segmentation'],
    'point cloud': ['point cloud'],
    'LLMs': ['language model'],
    'ViTs': ['vit', 'vision transformer'],
    'NeRF': ['radiance field', 'radiance fields', 'nerf'],
    'Gaussian splatting': ['gaussian splatting', 'splatting'],
    'video': ['video'],
}

# Determine the field of each paper for all years
paper_fields = {}
for conference in conferences:
    years = conf2year[conference]
    for year in years:
        abstracts = [paper['abstract'] for paper in data[(conference, year)]]
        paper_fields[(conference, year)] = []
        for abstract in abstracts:
            field_found = False
            for field, keywords in fields.items():
                if any(keyword in abstract.lower() for keyword in keywords):
                    paper_fields[(conference, year)].append(field)
                    field_found = True
                    break
            if not field_found:
                paper_fields[(conference, year)].append('other')

# Create a scatter plot for a specific conference and year
def calculate_tsne(conference, year):
    # Extract the data for the specified conference and year
    year_data = data[(conference, year)]
    year_embeddings = embeddings[(conference, year)]
    year_titles = [paper['title'] for paper in year_data]
    year_fields = paper_fields[(conference, year)]
    year_pdf_links = [paper['pdf_link'] for paper in year_data]
    year_abstracts = [paper['abstract'] for paper in year_data]

    # Reduce the dimensionality of the embeddings to 2D using t-SNE
    tsne = TSNE(n_components=2, random_state=0, perplexity=30)
    embeddings_2d = tsne.fit_transform(year_embeddings)

    # Create a DataFrame with the 2D embeddings, the titles, the fields, and the PDF links
    df = pd.DataFrame({
        'x': embeddings_2d[:, 0],
        'y': embeddings_2d[:, 1],
        'title': year_titles,
        'field': year_fields,
        'pdf_link': year_pdf_links,
        'abstract': year_abstracts
    })

    return df

# Create the Dash application
app = dash.Dash(__name__)
app.title = "CVPR Explorer"
#pre-compute all TSNE plots so graphs load quickly
calculated_tsnes = {}
for conference in conferences:
    years = conf2year[conference]
    calculated_tsnes.update({
    (conference, year): calculate_tsne(conference, year) for year in years
    })

def create_scatter_plot(conference, year):
    # Create a scatter plot of the embeddings
    df = calculated_tsnes[(conference, year)]
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
            customdata=df_field[['pdf_link', 'title', 'abstract']].values,
            hovertemplate='<b>%{text}</b><br><br><extra></extra>'
        ))

    # Set the aspect ratio of the figure to 1 and the background color to white
    fig.update_layout(
        autosize=True,
        #height=800,  # fallback height in pixels
        margin=dict(
            l=50,
            r=50,
            b=100,
            t=100,
            pad=4
        ),
        paper_bgcolor="#111111",
        plot_bgcolor="#111111",
        font=dict(
            color="white"
        ),
    title=f"t-SNE plot of {conference.upper()} {year} Paper Embeddings",
        title_font=dict(
            size=24
        ),
        title_x=0.5
    )

    return fig


# Define the layout of the application
app.layout = html.Div(
    children=[
        html.Div(
            children=[
                dcc.Dropdown(
                    id='conference-dropdown',
                    options=[
                        {'label': 'CVPR', 'value': 'cvpr'},
                        {'label': 'ECCV', 'value': 'eccv'},
                        {'label': 'ICCV', 'value': 'iccv'}
                    ],
                    value='cvpr',
                    style={'color': 'black', 'backgroundColor': 'black', 'width': '150px'}
                ),
                dcc.Dropdown(
                    id='year-dropdown',
                    options=[
                        {'label': str(year), 'value': year} for year in conf2year['cvpr']
                    ],
                    value=max(conf2year['cvpr']),
                    style={'color': 'black', 'backgroundColor': 'black', 'width': '150px'}
                ),
            ],
            style={'display': 'flex', 'justifyContent': 'center', 'marginTop': '20px'}
        ),
        dcc.Graph(
            id='scatter-plot',
            figure=create_scatter_plot('cvpr', max(conf2year['cvpr'])),
            style={"height": "80vh"}
        ),
        html.Div(
            children=[
                html.Div(id='pdf-link'),
                html.Div(id='title'),
                html.Div(id='abstract'),
                html.Div(
                    children=[
                    html.P("This site allows you to visualize over 30,000 papers from top computer vision conferences like CVPR, ECCV and ICCV"),
                    html.P("Find similar papers from nearby points on the TSNE plot"),
                    html.P("Click on a data point to view the title, abstract, and open the PDF link."),
                    html.P("Use the GitHub and LinkedIn links to view the source code and connect with me. Happy reading :)"),
                ],
                style={'color': 'white', 'textAlign': 'center', 'marginTop': '20px'}
                ),
                dcc.Link(
                    'GitHub',
                    href='https://github.com/dataplayer12/cvpr-explorer',
                    target='_blank',
                    style={
                        'display': 'inline-block',
                        'backgroundColor': '#6c757d',
                        'color': 'white',
                        'padding': '10px',
                        'textDecoration': 'none',
                        'marginRight': '10px'
                    }
                ),
                dcc.Link(
                    'LinkedIn',
                    href='https://linkedin.com/in/jaiyam-sharma',
                    target='_blank',
                    style={
                        'display': 'inline-block',
                        'backgroundColor': '#6c757d',
                        'color': 'white',
                        'padding': '10px',
                        'textDecoration': 'none'
                    }
                )
            ],
            style={'marginTop': '20px', 'marginBottom': '0'}
        )],
        style={'backgroundColor': '#111111', 'color': 'white', 'display': 'flex', 'flexDirection': 'column'}
        )


# Define a callback that updates the year dropdown based on the selected conference
@app.callback(
    Output('year-dropdown', 'options'),
    Input('conference-dropdown', 'value')
)
def update_year_dropdown(conference):
    years = conf2year[conference.lower()]
    return [{'label': str(year), 'value': year} for year in years]

# Define a callback that updates the scatter plot based on the selected conference and year
@app.callback(
    Output('scatter-plot', 'figure'),
    [Input('conference-dropdown', 'value'), Input('year-dropdown', 'value')]
)
def update_scatter_plot(conference, year):
    if (conference.lower(), year) in calculated_tsnes.keys():
        return create_scatter_plot(conference.lower(), year)
    else:
        year = max(conf2year[conference.lower()])
        return create_scatter_plot(conference.lower(), year)


# Define a callback that updates the PDF link, title, and abstract when a data point is clicked
@app.callback(
    [Output('pdf-link', 'children'), Output('title', 'children'), Output('abstract', 'children')],
    Input('scatter-plot', 'clickData')
)
def update_link_and_abstract(clickData):
    if clickData is not None:
        href, title, abstract = clickData['points'][0]['customdata']
        return (
            html.A('Open PDF', href=href, target='_blank', style={'color': 'white'}),
            html.P(f"Title: {title}", style={'color': 'white'}),
            html.P(f"Abstract: {abstract}", style={'color': 'white'})
        )
    else:
        return '', '', ''


# Run the application
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=80)

