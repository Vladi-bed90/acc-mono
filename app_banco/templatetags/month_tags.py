"""
    Sirven para crear Template Tags personalizados.
    En primer caso <month_name()> se convierta el numero
    a Nombre del mes.
    
    
    URL:  https://www.youtube.com/watch?v=-RzLQ9V_97k&ab_channel=OpenWebinars
"""
from django import template
import calendar

register = template.Library()


@register.filter
def month_name(month_number):
    month_number = int(month_number)
    return calendar.month_name[month_number]