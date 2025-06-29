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
            <input type="hidden" id="{field_id}" name="{name}" value="{current_value}">
            <div class="stars-display">
                {''.join([
                    (
                        f'<span class="star" data-rating="{i}" '
                        f'style="color: {"#ffd700" if i <= current_value else "#ddd"}; '
                        f'cursor: pointer; font-size: 24px;">★</span>'
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
                        star.style.color = '#ffd700';
                    }} else {{
                        star.style.color = '#ddd';
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
                            s.style.color = '#ffed4e';
                        }} else {{
                            s.style.color = '#ddd';
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
