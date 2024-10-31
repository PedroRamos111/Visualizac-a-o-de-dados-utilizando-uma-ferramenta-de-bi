import praw
import csv

# Configurações da API
reddit = praw.Reddit(
    client_id="vy8DvyTTyFa6DdZEQk5oHw",
    client_secret="8878MvG21LThDZWj4gTP9wSsC3LPlg",
    user_agent="meu_script_reddit:v1.0 (by u/Icy_Demand_2670)",  # algo como "meu_script_reddit:v1.0 (by u/seu_usuario)"
)

# Definindo o subreddit e palavras-chave para a Pergunta 1
subreddit = reddit.subreddit("learnprogramming")  # Altere para o subreddit desejado
pergunta_1_keywords = ["tutorial", "dicas e truques", "pedido de ajuda", "carreira", "indicação de livros"]

# Coletando dados para Pergunta 1
dados_pergunta_1 = []
for palavra in pergunta_1_keywords:
    for post in subreddit.search(palavra, limit=100):  # Aqui, 100 posts para cada palavra-chave
        dados_pergunta_1.append([
            post.id,
            post.title,
            post.score,
            post.num_comments,
            post.upvote_ratio,
            post.created_utc,
            post.url
        ])

# Salvando dados em CSV para Pergunta 1
with open("reddit_posts_pergunta_1.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["post_id", "upvotes", "comentarios", "upvote_ratio", "data_criacao", "url"])
    
    for linha in dados_pergunta_1:
        writer.writerow(linha)

print("Dados da Pergunta 1 salvos em reddit_posts_pergunta_1.csv")
