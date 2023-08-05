# kamer/version.py
#
#

""" version plugin. """

from kamer import __version__

txt = """ mishandeling gepleegd door toediening van voor het leven of de gezondheid schadelijk stoffen """

def version(event):
    event.reply("KAMER #%s - %s" % (__version__, txt))
