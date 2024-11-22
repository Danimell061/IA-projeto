import requests
import boto3
from gtts import gTTS

# ID
ID_desejado = "66f487d9ebdb9a0568e1cc0d"  

api_url = "https://projeto-backend.fly.dev/noticias"
response = requests.get(api_url)

if response.status_code == 200:
    noticias = response.json()

    # ID especifico
    noticia_encontrada = None
    for noticia in noticias:
        if noticia.get("_id") == ID_desejado:
            noticia_encontrada = noticia
            break

    if noticia_encontrada:
        titulo = noticia_encontrada.get("titulo", "Sem título")
        autor = noticia_encontrada.get("nome_autor", "Autor desconhecido")
        texto = noticia_encontrada.get("texto", "Sem conteúdo")

        conteudo = f"Notícia: {titulo}. Escrita por {autor}. Conteúdo do texto: {texto}"

        # Nome do arquivo MP3
        arquivo_mp3 = f"noticia_{ID_desejado}.mp3"

        # Converte o texto em áudio e salva como MP3
        tts = gTTS(text=conteudo, lang='pt', slow=False)
        tts.save(arquivo_mp3)

        print(f"Áudio gerado e salvo como: {arquivo_mp3}")
    else:
        print(f"Notícia com o título '{titulo_desejado}' não encontrada.")
else:
    print(f"Erro ao acessar a API. Status Code: {response.status_code}")
