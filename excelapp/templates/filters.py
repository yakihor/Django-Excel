from django import template
register = template.Library()

@register.filter(name='times') 
def times(number):
  return range(number)

def m_id(col, row):
  return ("loc" + str(((int(col) + 1) * 100) + int(row) + 1))