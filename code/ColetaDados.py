import csv
import re
import praw

# Configurações da API
reddit = praw.Reddit(
    client_id="vy8DvyTTyFa6DdZEQk5oHw",
    client_secret="8878MvG21LThDZWj4gTP9wSsC3LPlg",
    user_agent="meu_script_reddit:v1.0 (by u/Icy_Demand_2670)"
)

# Definindo os subreddits e categorias para busca
subreddits = ["learnprogramming", "webdev", "programming"]
categories = ["video", "texto", "link", "enquete"]

# Lista de linguagens de programação
languages = ["Python", "JavaScript", "Java", "Ruby", "Go", "Rust", "Swift", "PHP", "Kotlin", "R", "TypeScript", "C", "Vue","Dockerfile", "Assembly" "CSS","HTML", "React", "Js", "React js", "React", "Java script", "Assembly", "JS", "Lua", "Angular", "Flutter", "Julia"]

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

# Função para detectar a linguagem de programação no título
def detect_language(title):
    # Converte o título para minúsculas
    title_lower = title.lower()
    for language in languages:
        # Escapa caracteres especiais no nome da linguagem e converte para minúsculas
        escaped_language = re.escape(language.lower())
        if re.search(rf"\b{escaped_language}\b", title_lower):
            return language
    return "Outros"
# Função para coletar posts e filtrar por tipo, de múltiplos subreddits
def collect_top_posts(subreddits, target_count=1000):
    all_posts = []
    
    # Coleta geral de posts para textos e links
    for subreddit_name in subreddits:
        subreddit = reddit.subreddit(subreddit_name)
        
        # Coletando posts recentes
        all_posts_data = subreddit.new(limit=10000)
        
        for post in all_posts_data:
            post_format = get_post_format(post)
            language = detect_language(post.title)
            
            all_posts.append({
                "subreddit": subreddit_name,
                "post_id": post.id,
                "titulo": post.title,
                "upvotes": post.score,
                "comentarios": post.num_comments,
                "compartilhamentos": post.num_crossposts,
                "formato": post_format,
                "tags": post.link_flair_text,
                "linguagem": language,
                "url": post.url
            })

            # Limita a coleta de posts por categoria
            if len(all_posts) >= target_count * len(categories):
                break

    return all_posts

# Coletando dados e salvando em um único CSV
posts = collect_top_posts(subreddits)

with open("reddit_top_posts.csv", "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["subreddit", "post_id", "titulo", "upvotes", "comentarios", "compartilhamentos", "formato", "tags", "linguagem", "url"])
    writer.writeheader()
    for post in posts:
        writer.writerow(post)

print("Dados salvos em reddit_top_posts.csv")
