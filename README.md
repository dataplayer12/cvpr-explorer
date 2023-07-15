# cvpr-explorer
Visualize CVPR papers as embeddings

# Browse
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
- [ ] Add more years, allow selecting year
- [ ] Docker image that builds on both arm and x86
