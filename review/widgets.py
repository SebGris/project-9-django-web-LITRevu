from django import forms
from django.utils.safestring import mark_safe


class StarRatingWidget(forms.Select):
    """
    Widget personnalisé pour afficher un sélecteur d'étoiles
    """
    def __init__(self, attrs=None):
        choices = [(i, f'{i} étoile{"s" if i > 1 else ""}')
                   for i in range(1, 6)]
        super().__init__(attrs, choices)

    def render(self, name, value, attrs=None, renderer=None):
        if attrs is None:
            attrs = {}

        # Assurer que value est un entier valide
        current_value = int(value) if value and str(value).isdigit() else 0

        # Générer un ID unique pour éviter les conflits
        import uuid
        unique_id = str(uuid.uuid4())[:8]
        field_id = f"rating_{name}_{unique_id}"

        # Créer l'interface d'étoiles directement
        html = f'''
        <div class="star-rating-widget" id="{field_id}_container">
            <input type="hidden" id="{field_id}" name="{name}"
                   value="{current_value}">
            <div class="stars-display">
                {''.join([
                    (
                        f'<span class="star" data-rating="{i}" '
                        f'style="color: '
                        f'{"#996600" if i <= current_value else "#666"}; '
                        f'cursor: pointer; font-size: 32px;">★</span>'
                    )
                    for i in range(1, 6)
                ])}
            </div>
        </div>

        <script>
        (function() {{
            const container = document.getElementById('{field_id}_container');
            const hiddenInput = document.getElementById('{field_id}');
            const stars = container.querySelectorAll('.star');

            function updateStars(rating) {{
                stars.forEach((star, index) => {{
                    const starValue = index + 1;
                    if (starValue <= rating) {{
                        star.style.color = '#996600';
                    }} else {{
                        star.style.color = '#666';
                    }}
                }});
                hiddenInput.value = rating;
            }}

            // Initialiser avec la valeur actuelle
            updateStars({current_value});

            stars.forEach((star) => {{
                star.addEventListener('click', function() {{
                    const rating = parseInt(this.dataset.rating);
                    updateStars(rating);
                }});

                star.addEventListener('mouseenter', function() {{
                    const rating = parseInt(this.dataset.rating);
                    stars.forEach((s, index) => {{
                        const starValue = index + 1;
                        if (starValue <= rating) {{
                            s.style.color = '#996600';
                        }} else {{
                            s.style.color = '#666';
                        }}
                    }});
                }});
            }});

            container.addEventListener('mouseleave', function() {{
                const currentRating = parseInt(hiddenInput.value) || 0;
                updateStars(currentRating);
            }});
        }})();
        </script>
        '''

        return mark_safe(html)


class SimpleRatingWidget(forms.RadioSelect):
    """
    Version simple avec boutons radio horizontaux
    """
    def __init__(self, attrs=None):
        choices = [(i, f'{i}') for i in range(0, 6)]
        super().__init__(attrs, choices)

    def render(self, name, value, attrs=None, renderer=None):
        # Rendu HTML simple et fonctionnel en horizontal
        html = '<div class="simple-rating-widget" style="display: flex; gap: 15px; align-items: center;">'
        
        for i in range(0, 6):
            checked = 'checked' if str(value) == str(i) else ''
            if i == 0:
                label_text = "0 étoile"
            else:
                label_text = f'{i} étoile{"s" if i > 1 else ""}'
            
            html += f'''
            <label style="display: flex; align-items: center; cursor: pointer; white-space: nowrap;">
                <input type="radio" name="{name}" value="{i}" {checked} style="margin-right: 5px;">
                {label_text}
            </label>
            '''
        html += '</div>'
        return mark_safe(html)
