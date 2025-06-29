from django import template

register = template.Library()


@register.filter
def stars(rating):
    """
    Convertit un rating numérique en étoiles HTML
    """
    if rating is None:
        return ""
    
    rating = int(rating)
    full_stars = "★" * rating
    empty_stars = "☆" * (5 - rating)
    return full_stars + empty_stars


@register.filter
def stars_html(rating):
    """
    Convertit un rating numérique en étoiles HTML avec classes CSS
    """
    if rating is None:
        return ""
    
    rating = int(rating)
    stars_html = ""
    
    for i in range(1, 6):
        if i <= rating:
            stars_html += '<span class="star filled">★</span>'
        else:
            stars_html += '<span class="star empty">☆</span>'
    
    return stars_html


@register.inclusion_tag('review/_stars.html')
def display_stars(rating):
    """
    Template tag d'inclusion pour afficher les étoiles
    """
    return {'rating': rating}


@register.simple_tag
def rating_stars(rating, max_rating=5):
    """
    Simple tag pour générer des étoiles avec plus d'options
    """
    if rating is None:
        rating = 0
    
    rating = min(max(int(rating), 0), max_rating)
    
    html = '<div class="rating-stars">'
    for i in range(1, max_rating + 1):
        if i <= rating:
            html += (f'<span class="star star-filled" '
                     f'data-rating="{i}">★</span>')
        else:
            html += (f'<span class="star star-empty" '
                     f'data-rating="{i}">☆</span>')
    html += '</div>'
    
    return html
