# cvpr-explorer
Visualize CVPR papers as embeddings on [cvprexplorer.com](http://cvprexplorer.com)

# Problem Statement
As the field of AI and machine learning has exploded in recent years, it has become increasingly difficult to keep up to date with latest research. Conference websites frequently list >2000 papers in one giant list out of which it is not easy to find papers one is interested in.

# This Project
The current project is a visual aid for browsing CVPR papers. I am starting with CVPR because its a popular conference and has extensive public records. I scraped the website and found the paper titles and abstracts, then used OpenAI embedding API to find vector embeddings of the abstracts. Finally, I visualized the embeddings in 2D with t-SNE plot. Each point in the plot is a paper.

The results are amazing. The embeddings reveal clusters of popular topics like transformers, NeRF, diffusion models etc in recent years. So, if you are interested in only diffusion models, for example, you do not have to wade through hundreds of irrelevant papers and only need to look at points (papers) in the corresponding cluster.

I hope this tool will be useful for stuents, researchers and ML engineers. I invite the community to biuld on this project and add more conferences. I hope that some day this will become the standard way of finding new papers and that unorganized long lists of >2000 papers will be a thing of the past.

# Demo
You can view the app at [cvprexplorer.com](http://cvprexplorer.com)

# Results
![embeddings](https://github.com/dataplayer12/cvpr-explorer/assets/11517109/d8913d58-26f2-43a2-b0f8-de5c526f0ab6)


## Deploy using docker
```Shell
git clone http://github.com/dataplayer12/cvpr-explorer.git
cd cvpr-explorer/
docker build -t cvpr-explorer .
docker run --network=host cvpr-explorer
```

## Deploy with docker compose
```Shell
docker compose build
docker compose up
```

## Roadmap

- [x] Show paper title, abstract and PDF link
- [x] Allow figure to stretch with screen size
- [x] Cache embeddings to disk, read from disk
- [x] Add links to the GitHub repo and my LinkedIn
- [ ] Mark papers with code, add 'see code' button
- [ ] Allow searching by keyword
- [x] Use OpenAI embeddings
- [x] Add more years, allow selecting year
- [ ] Docker image that builds on both arm and x86
