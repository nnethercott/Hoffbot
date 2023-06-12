# Hoffbot :robot: :coffee:

<p align="center">
<img src="media/10x.gif" width=450>
</p>

## requirements 
```
!pip install -r requirements.txt 
```

## outline 
### LLMs :hugs:
* [this t5 model for question answering](https://huggingface.co/MaRiOrOsSi/t5-base-finetuned-question-answering) (grazie gli :it:)
* [cosine similarity model](https://huggingface.co/sentence-transformers/multi-qa-MiniLM-L6-cos-v1)
* [crossencoder](https://huggingface.co/cross-encoder/ms-marco-MiniLM-L-6-v2)

### Deploying 
I'm kinda new to the frontend stuff so I made heavy use of [this playlist](https://www.youtube.com/watch?v=KJ5bFv-IRFM&list=PLzMcBGfZo4-kqyzTzJWCV6lyK-ZMYECDc) on youtube for Flask + Slack API integration. Also for the [chromadb](https://www.trychroma.com) part refer to [their docs](https://docs.trychroma.com). 

That being said, the pipline itself fully doesn't require Slack integration, I just figured it would be nice to provide an interface to everything.  So if you want to get a feel for the model/workflow check out the `t5skeleton.ipynb` file which is essentially the rough draft of this project entirely offline. 

## comments
If you want to regenerate any of the data included in the `clean` folder you'll need a functioning YouTube API key and to dig into the `youtube-api.ipynb` notebook.  Same goes for the embeddings but this time you'll need to use the `t5skeleton.ipynb`. Otherwise I've included the cleaned subtitle .vtt's as well as the embeddings I generated for the demo here in the repo already.

Hopefully didn't leave any of my API keys around, that would be bad.
