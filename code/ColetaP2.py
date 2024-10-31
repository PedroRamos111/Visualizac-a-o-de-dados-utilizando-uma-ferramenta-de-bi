import praw
import csv

# Configurações da API
reddit = praw.Reddit(
    client_id="vy8DvyTTyFa6DdZEQk5oHw",
    client_secret="8878MvG21LThDZWj4gTP9wSsC3LPlg",
    user_agent="meu_script_reddit:v1.0 (by u/Icy_Demand_2670)"
)

# Definindo os subreddits e categorias para busca
subreddits = ["learnprogramming", "webdev", "programming"]
categories = ["video", "texto", "link", "enquete"]

# Função para determinar o formato do post
def get_post_format(post):
    if post.is_video:
        return "video"
    elif post.is_self:
        return "texto"
    elif "poll" in post.url:
        return "enquete"
    else:
        return "link"

# Função para coletar posts e filtrar por tipo, de múltiplos subreddits
def collect_top_posts(subreddits, target_count=1000):
    posts_by_category = {category: [] for category in categories}
    
    # Coleta geral de posts para textos e links
    for subreddit_name in subreddits:
        subreddit = reddit.subreddit(subreddit_name)
        
        # Coletando posts recentes
        all_posts = subreddit.new(limit=10000)
        
        for post in all_posts:
            post_format = get_post_format(post)

            # Adiciona post à categoria correspondente se ainda não atingiu o limite
            if len(posts_by_category[post_format]) < target_count:
                posts_by_category[post_format].append({
                    "subreddit": subreddit_name,
                    "post_id": post.id,
                    "titulo": post.title,
                    "upvotes": post.score,
                    "comentarios": post.num_comments,
                    "compartilhamentos": post.num_crossposts,
                    "formato": post_format,
                    "tags": post.link_flair_text,
                    "url": post.url
                })

    # Busca por vídeos e enquetes
    for subreddit_name in subreddits:
        subreddit = reddit.subreddit(subreddit_name)

        # Buscar vídeos
        video_posts = subreddit.search("video", sort="relevance", limit=1000)
        for post in video_posts:
            post_format = get_post_format(post)
            if post_format == "video" and len(posts_by_category["video"]) < target_count:
                posts_by_category["video"].append({
                    "subreddit": subreddit_name,
                    "post_id": post.id,
                    "titulo": post.title,
                    "upvotes": post.score,
                    "comentarios": post.num_comments,
                    "compartilhamentos": post.num_crossposts,
                    "formato": post_format,
                    "tags": post.link_flair_text,
                    "url": post.url
                })

        # Buscar enquetes
        poll_posts = subreddit.search("poll", sort="relevance", limit=1000)
        for post in poll_posts:
            post_format = get_post_format(post)
            if post_format == "enquete" and len(posts_by_category["enquete"]) < target_count:
                posts_by_category["enquete"].append({
                    "subreddit": subreddit_name,
                    "post_id": post.id,
                    "titulo": post.title,
                    "upvotes": post.score,
                    "comentarios": post.num_comments,
                    "compartilhamentos": post.num_crossposts,
                    "formato": post_format,
                    "tags": post.link_flair_text,
                    "url": post.url
                })

    return posts_by_category

# Coletando dados e salvando em CSV para cada categoria
posts_by_category = collect_top_posts(subreddits)

for category, posts in posts_by_category.items():
    # Salvando em CSV
    with open(f"P2_reddit_top_1000_posts_{category}.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["subreddit", "post_id", "titulo", "upvotes", "comentarios", "compartilhamentos", "formato", "tags", "url"])
        writer.writeheader()
        for post in posts:
            writer.writerow(post)

    print(f"Dados salvos para {category} em reddit_top_1000_posts_{category}.csv")
