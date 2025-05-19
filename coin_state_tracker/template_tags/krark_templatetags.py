from django import template

register = template.Library()

@register.filter
def percentage(value):
    """Convert a decimal to percentage with % sign"""
    try:
        decimal_value = float(value)
        return f"{decimal_value * 100:.2f}%"
    except (ValueError, TypeError):
        return ""