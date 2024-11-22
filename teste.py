import requests
import boto3
from gtts import gTTS

AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''

s3 = boto3.resource(
    's3',
    region_name='sa-east-1',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

# URL da API que fornece as notícias
api_url = "https://projeto-backend.fly.dev/noticias"
response = requests.get(api_url)

if response.status_code == 200:
    noticias = response.json()  # Lista de notícias retornada pela API

    for i, noticia in enumerate(noticias):
        titulo = noticia.get("titulo", "Sem título")
        autor = noticia.get("nome_autor", "Autor desconhecido")
        texto = noticia.get("texto", "Sem conteúdo")

        # Combina o autor, título e texto em um único conteúdo
        conteudo = f"Notícia: {titulo}. Escrita por {autor}. Conteúdo do texto: {texto}"

        # Nome do arquivo MP3 com o ID da notícia ou índice
        arquivo_mp3 = f"noticia_{i+1}.mp3"

        # Converte o texto em áudio e salva como MP3
        tts = gTTS(text=conteudo, lang='pt', slow=False)
        tts.save(arquivo_mp3)

        print(f"Áudio gerado e salvo como: {arquivo_mp3}")

        # Corrigir o upload para o S3, especificando o caminho correto
        s3.Bucket('audioia').upload_file(arquivo_mp3, arquivo_mp3)
else:
    print(f"Erro ao acessar a API. Status Code: {response.status_code}")

