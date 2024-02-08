from django import template
from django.utils.safestring import mark_safe
import re
import inflect

register = template.Library()

unique_characters = {"T":"tap this permanent","W":"one white mana","U":"one blue mana","B":"one black mana","R":"one red mana","G":"one green mana","C":"one colorless mana","X":"X generic mana",
                     "U/R":"one blue or red mana","W/B":"one white or black mana","R/G":"one red or green mana","G/U":"one green or blue mana",
                     "B/R":"one black or red mana","W/U":"one white or blue mana","R/W":"one red or white mana","U/B":"one blue or black mana",
                     "B/G":"one black or green mana","G/W":"one green or white mana", "S":"one snow mana","E":"An energy counter","INFINITY":"infinite generic mana"}


@register.filter
def oracle_text(text):

    text = parse_symbols(text)
    text = text.replace('(', '<i>(')
    text = text.replace(')', ')</i>')
    #turn linebreaks into double line breaks so following filter delivers desired result
    text = text.replace("\n", "\n\n")

#italics on keyword is shelved for now
    # if "—" in text:
    #     items = text.split("—")
    #     keyword = items[0]
    #     if keyword != "Cumulative upkeep":
    #         del items[0]
    #         text = "<i>"+keyword+"</i>"+ "—".join(items)




    return mark_safe(text)

def parse_symbols(text):

    engine = inflect.engine()
    res = set(re.findall(r'\{.*?\}', text))
    for symbol in res:
        char = symbol[1:-1]
        if char.isdigit():
            text = text.replace(symbol,'<abbr class="card-symbol card-symbol-'+ char +'" title="'+engine.number_to_words(char)+' generic mana">'+symbol+'</abbr>')
        else:
            if char == '∞':
                char = "INFINITY"

            card_symbol = char
            if "/" in char:
                card_symbol = char[:1] + char[2:]


            try:
               text = text.replace( symbol,'<abbr class="card-symbol card-symbol-'+ card_symbol +'" title="'+ unique_characters[char] +'">'+symbol+'</abbr>')
            except:
                print("symbol not found")

    return text


