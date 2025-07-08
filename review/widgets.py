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

        # Générer un ID unique pour éviter les conflits
        import uuid
        unique_id = str(uuid.uuid4())[:8]
        group_id = f"star_group_{unique_id}"

        # Assurer que value est un entier valide
        current_value = int(value) if value and str(value).isdigit() else 0

        html = f'<div class="star-radio-group" id="{group_id}" data-name="{name}">'

        for i in range(1, 6):
            checked = 'checked' if current_value == i else ''
            filled_class = 'filled' if current_value >= i else 'empty'
            input_id = f"{group_id}_star_{i}"
            
            html += f'''
            <label class="star-label" for="{input_id}">
                <input type="radio" id="{input_id}" name="{name}" value="{i}" {checked}>
                <span class="star-radio {filled_class}">★</span>
            </label>
            '''

        html += '</div>'

        html += f'''
        <script>
        (function() {{
            const group = document.getElementById('{group_id}');
            const inputs = group.querySelectorAll('input[type="radio"]');
            const stars = group.querySelectorAll('.star-radio');

            function updateStars(selectedValue) {{
                stars.forEach((star, index) => {{
                    const starValue = index + 1;
                    if (starValue <= selectedValue) {{
                        star.classList.remove('empty');
                        star.classList.add('filled');
                    }} else {{
                        star.classList.remove('filled');
                        star.classList.add('empty');
                    }}
                }});
            }}

            // Initialiser avec la valeur actuelle
            updateStars({current_value});

            inputs.forEach((input, index) => {{
                input.addEventListener('change', function() {{
                    if (this.checked) {{
                        updateStars(parseInt(this.value));
                    }}
                }});
            }});
        }})();
        </script>
        '''

        return mark_safe(html)
