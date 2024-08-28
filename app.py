from meta_ai_api import MetaAI
ai = MetaAI(fb_email="skk12112003@gmail.com", fb_password="")
resp = ai.prompt(message="Generate an image of a tech CEO")
print(resp)