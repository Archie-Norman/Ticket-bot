# Ticket-bot
Ticket bot

**SB.py**
SeleniumBase implementation that avoids the antibot CloudFlare Turnstile

**bot-with-GUI-and-auth.py**
a user-friendly bot that asks for the login details what date they need a ticket for and what time the ticket needs to be. Unfortunately, this was never used due to the anti-bot system being implemented.

**server.py**
the server for the bot-with-GUI-and-auth.py as it used authentication keys to make sure the software couldn't be pirated. it used a ngrok api gateway.

**page check v2.py**
checks for page updates to inform you when the event page updates and adds tickets.

**pre-antibot.py**
selenium code that was used before CloudFlare Turnstile

**pre_antibot_js-code**
javascript code to test if it would be any faster and it was.

**thread.py**
code that would buy multiple tickets at the same time on different accounts using threading

**v2.py**
this code connects to an Android emulator that then buys tickets. could be altered to work on a real phone. this was done as the app doesn't have the Cloudflare Turnstile but android emulation was very resource-intensive to make it worth it as only three tickets could be purchased at a time.
