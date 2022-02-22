from time import strftime
from pyfiglet import Figlet

d_form = "%Y %d %b, %A"
d_font = "graceful"

def date(format = d_form, font = d_font):
    
    fig = Figlet(font = font)
    return fig.renderText(strftime(format))