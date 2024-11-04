import torch
import os
import random


def expand_model_embeddings(ckpt_path, new_ckpt_path, num_new_tokens=42):
    seed = 666
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

    ckpt = torch.load(ckpt_path, map_location="cpu")

    ema_sd = ckpt.get("ema_model_state_dict", {})
    embed_key_ema = "ema_model.transformer.text_embed.text_embed.weight"
    old_embed_ema = ema_sd[embed_key_ema]

    vocab_old = old_embed_ema.size(0)
    embed_dim = old_embed_ema.size(1)
    vocab_new = vocab_old + num_new_tokens

    def expand_embeddings(old_embeddings):
        new_embeddings = torch.zeros((vocab_new, embed_dim))
        new_embeddings[:vocab_old] = old_embeddings
        new_embeddings[vocab_old:] = torch.randn((num_new_tokens, embed_dim))
        return new_embeddings

    ema_sd[embed_key_ema] = expand_embeddings(ema_sd[embed_key_ema])

    torch.save(ckpt, new_ckpt_path)

    return vocab_new


