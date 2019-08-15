import re
import logging
import pickle
import yaml
import pathlib
import spacy
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence

from constants import Constants

import warnings
warnings.filterwarnings("ignore")

# device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')
device = torch.device('cpu')

logger = logging.getLogger(Constants.MICROSERVICE_NAME)

PAD = 0
UNK = 1

with open('project/sentiment/ml_models/idxs.pkl', mode='rb') as f:
    prepro_idxs = pickle.load(f)
word2idx = prepro_idxs['word2idx']
idx2word = prepro_idxs['idx2word']

nlp = spacy.load('en_core_web_sm', disable=['parser', 'tagger', 'ner'])


class ConcatPoolingGRUAdaptive(nn.Module):
    def __init__(self, vocab_size, embedding_dim, n_hidden, n_out):
        super().__init__()
        self.vocab_size = vocab_size
        self.embedding_dim = embedding_dim
        self.n_hidden = n_hidden
        self.n_out = n_out
        self.emb = nn.Embedding(self.vocab_size, self.embedding_dim)
        self.emb_drop = nn.Dropout(0.3)
        self.gru = nn.GRU(self.embedding_dim, self.n_hidden, dropout=0.3)
        self.out = nn.Linear(self.n_hidden*3, self.n_out)

    def forward(self, seq, lengths):
        self.h = self.init_hidden(seq.size(1))
        embs = self.emb_drop(self.emb(seq))
        embs = pack_padded_sequence(embs, lengths)
        gru_out, self.h = self.gru(embs, self.h)
        gru_out, lengths = pad_packed_sequence(gru_out)

        avg_pool = F.adaptive_avg_pool1d(
            gru_out.permute(1, 2, 0), 1).view(seq.size(1), -1)
        max_pool = F.adaptive_max_pool1d(
            gru_out.permute(1, 2, 0), 1).view(seq.size(1), -1)

        outp = self.out(torch.cat([self.h[-1], avg_pool, max_pool], dim=1))
        return F.log_softmax(outp, dim=-1)  # it will return log of softmax

    def init_hidden(self, batch_size):
        return torch.zeros(
            (1, batch_size, self.n_hidden),
            requires_grad=True).to(device)

    def predict(self, text):
        if not isinstance(text, str):
            return None, None
        vec = self.preprocess(text)
        x, lens = ConcatPoolingGRUAdaptive.collate_fn([vec])
        with torch.no_grad():
            y_pred = self.forward(x, lens)
        probs = torch.exp(y_pred)
        logger.debug(f'text: {text}, probabilities: {probs.tolist()}')
        return torch.max(y_pred, dim=1)[1].item(), probs.tolist()[0]

    def preprocess(self, text):
        tokens = [w.text.lower() for w in nlp(self.tweet_clean(text))]
        vec = self.vectorize(tokens, word2idx)
        return vec

    def tweet_clean(self, text):
        """Very basic text cleaning. This function can be built upon for
           better preprocessing
        """
        # replace multiple white spaces with single space
        text = re.sub(r'[\s]+', ' ', text)
        # remove links
        text = re.sub(r'https?:/\/\S+', ' ', text)
        # remove non alphanumeric character
        text = re.sub(r'[^A-Za-z0-9]+', ' ', text)
        logger.debug(f'cleaned text: {text}')
        return text.strip()

    def vectorize(self, tokens, word2idx):
        """Convert tweet to vector
        """
        vec = [word2idx.get(token, UNK) for token in tokens]
        return vec

    def collate_fn(data):
        """This function will be used to pad the tweets to max length
        in the batch and transpose the batch from
        batch_size x max_seq_len to max_seq_len x batch_size.
        It will return padded vectors, labels and lengths of each tweets
        (before padding)
        It will be used in the Dataloader
        """
        # data.sort(key=lambda x: len(x[0]), reverse=True)
        lens = [len(sent) for sent in data]
        padded_sents = torch.zeros(len(data), max(lens)).long()
        for i, sent in enumerate(data):
            padded_sents[i, :lens[i]] = torch.LongTensor(sent)

        padded_sents = padded_sents.transpose(0, 1)
        return padded_sents, lens

    def load(path=None):
        try:
            with open(pathlib.Path(__file__).parent.joinpath('model_config.yaml')) as f:
                ml_config = yaml.full_load(f)
        except FileNotFoundError as fnf:
            logger.error(fnf)
            raise fnf
        params = ml_config['sentiment_analysis']['params']
        model = ConcatPoolingGRUAdaptive(
            params['vocab_size'],
            params['embedding_dim'],
            params['n_hidden'],
            params['n_out'])
        print('Loading model...')
        model.load_state_dict(
            torch.load(
                ml_config['sentiment_analysis']['model_path'], map_location='cpu'))
        model.eval()
        return model


model = ConcatPoolingGRUAdaptive.load()
