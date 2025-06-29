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
        attrs['class'] = attrs.get('class', '') + ' rating-select'
        attrs['style'] = 'display: none;'  # Cacher le select original

        select_html = super().render(name, value, attrs, renderer)

        # Créer l'interface d'étoiles
        stars_html = f'''
        <div class="rating-input" data-target="id_{name}">
            <input type="hidden" id="id_{name}" name="{name}" value="{value or 0}">
            {''.join([
                f'<span class="star {"filled" if i <= int(value or 0) else "empty"}" data-value="{i}">★</span>'
                for i in range(1, 6)
            ])}
        </div>
        <script>
        document.addEventListener('DOMContentLoaded', function() {{
            const ratingContainer = document.querySelector('.rating-input[data-target="id_{name}"]');
            const hiddenInput = document.getElementById('id_{name}');
            const stars = ratingContainer.querySelectorAll('.star');
            
            stars.forEach((star, index) => {{
                star.addEventListener('click', function() {{
                    const rating = parseInt(this.dataset.value);
                    hiddenInput.value = rating;
                    
                    // Mettre à jour l'affichage
                    stars.forEach((s, i) => {{
                        if (i < rating) {{
                            s.classList.remove('empty');
                            s.classList.add('filled');
                        }} else {{
                            s.classList.remove('filled');
                            s.classList.add('empty');
                        }}
                    }});
                }});
                
                // Effet de survol
                star.addEventListener('mouseenter', function() {{
                    const rating = parseInt(this.dataset.value);
                    stars.forEach((s, i) => {{
                        if (i < rating) {{
                            s.style.color = '#ffed4e';
                        }} else {{
                            s.style.color = '#ddd';
                        }}
                    }});
                }});
            }});
            
            // Restaurer l'affichage au départ de la souris
            ratingContainer.addEventListener('mouseleave', function() {{
                const currentRating = parseInt(hiddenInput.value) || 0;
                stars.forEach((s, i) => {{
                    if (i < currentRating) {{
                        s.style.color = '#ffd700';
                    }} else {{
                        s.style.color = '#ddd';
                    }}
                }});
            }});
        }});
        </script>
        '''

        return mark_safe(select_html + stars_html)


class SimpleStarRatingWidget(forms.RadioSelect):
    """
    Version plus simple avec des boutons radio stylisés en étoiles
    """
    def __init__(self, attrs=None):
        choices = [(i, f'{i}') for i in range(1, 6)]
        super().__init__(attrs, choices)

    def render(self, name, value, attrs=None, renderer=None):
        if attrs is None:
            attrs = {}

        html = f'<div class="star-radio-group" data-name="{name}">'

        for i in range(1, 6):
            checked = 'checked' if str(value) == str(i) else ''
            html += f'''
            <label class="star-label">
                <input type="radio" name="{name}" value="{i}" {checked} style="display: none;">
                <span class="star-radio {'filled' if str(value) == str(i) else 'empty'}">★</span>
            </label>
            '''

        html += '</div>'

        html += '''
        <script>
        document.addEventListener('DOMContentLoaded', function() {
            const radioGroups = document.querySelectorAll('.star-radio-group');
            
            radioGroups.forEach(group => {
                const labels = group.querySelectorAll('.star-label');
                const inputs = group.querySelectorAll('input[type="radio"]');
                const stars = group.querySelectorAll('.star-radio');
                
                labels.forEach((label, index) => {
                    label.addEventListener('click', function() {
                        // Mettre à jour tous les étoiles
                        stars.forEach((star, i) => {
                            if (i <= index) {
                                star.classList.remove('empty');
                                star.classList.add('filled');
                            } else {
                                star.classList.remove('filled');
                                star.classList.add('empty');
                            }
                        });
                    });
                });
            });
        });
        </script>
        '''

        return mark_safe(html)
