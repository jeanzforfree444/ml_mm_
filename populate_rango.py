import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ml_mm_.settings')

django.setup()

from rango.models import Category, Article

def populate():

    categories = {
        'Rock': {
            'articles': [
                {'title': 'The Evolution of Rock Music', 'url': 'https://example.com/rock-evolution', 'views': 120, 'likes': 50, 'content': 'A' * 15000, 'article_picture': 'rock_evolution.jpg'},
                {'title': 'Top 10 Rock Bands of All Time', 'url': 'https://example.com/top10-rock', 'views': 95, 'likes': 40, 'content': 'B' * 15000, 'article_picture': 'top10_rock.jpg'}
            ],
            'views': 200, 'likes': 80
        },
        'Jazz': {
            'articles': [
                {'title': 'The Golden Era of Jazz', 'url': 'https://example.com/jazz-golden-era', 'views': 80, 'likes': 30, 'content': 'C' * 15000, 'article_picture': 'jazz_golden_era.jpg'},
                {'title': 'Famous Jazz Musicians and Their Impact', 'url': 'https://example.com/famous-jazz', 'views': 70, 'likes': 25, 'content': 'D' * 15000, 'article_picture': 'famous_jazz.jpg'}
            ],
            'views': 150, 'likes': 60
        },
        'Hip-Hop': {
            'articles': [
                {'title': 'The Rise of Hip-Hop Culture', 'url': 'https://example.com/hiphop-rise', 'views': 110, 'likes': 45, 'content': 'E' * 15000, 'article_picture': 'hiphop_rise.jpg'},
                {'title': 'Lyrics That Changed the World', 'url': 'https://example.com/hiphop-lyrics', 'views': 85, 'likes': 35, 'content': 'F' * 15000, 'article_picture': 'hiphop_lyrics.jpg'}
            ],
            'views': 180, 'likes': 75
        },
        'Classical': {
            'articles': [
                {'title': 'The Influence of Beethoven', 'url': 'https://example.com/beethoven-influence', 'views': 90, 'likes': 38, 'content': 'G' * 15000, 'article_picture': 'beethoven.jpg'},
                {'title': 'Why Mozart’s Music is Timeless', 'url': 'https://example.com/mozart-timeless', 'views': 85, 'likes': 34, 'content': 'H' * 15000, 'article_picture': 'mozart.jpg'}
            ],
            'views': 160, 'likes': 65
        },
        'Electronic': {
            'articles': [
                {'title': 'The Birth of Electronic Dance Music', 'url': 'https://example.com/edm-birth', 'views': 100, 'likes': 42, 'content': 'I' * 15000, 'article_picture': 'edm_birth.jpg'},
                {'title': 'Best Electronic Music Festivals', 'url': 'https://example.com/edm-festivals', 'views': 92, 'likes': 37, 'content': 'J' * 15000, 'article_picture': 'edm_festivals.jpg'}
            ],
            'views': 170, 'likes': 70
        }
    }
    
    for cat, cat_data in categories.items():

        c = add_cat(cat, cat_data['views'], cat_data['likes'])

        for a in cat_data['articles']:

            add_article(c, a['title'], a['url'], a['views'], a['likes'], a['content'], a['article_picture'])
    
    for c in Category.objects.all():

        for a in Article.objects.filter(category=c):

            print(f'- {c}: {a}')

def add_article(cat, title, url, views=0, likes=0, content='', article_picture=''):

    a = Article.objects.get_or_create(category=cat, title=title)[0]

    a.url = url
    
    a.content = content
    
    a.article_picture = article_picture
    
    a.views = views
    
    a.likes = likes
    
    a.save()
    
    return a

def add_cat(name, views=0, likes=0):
    
    c = Category.objects.get_or_create(name=name)[0]
    
    c.views = views
    
    c.likes = likes
    
    c.save()
    
    return c

if __name__ == '__main__':
    
    print('Starting Rango population script...')
    
    populate()