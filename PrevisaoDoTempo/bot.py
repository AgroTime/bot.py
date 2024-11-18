import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TELEGRAM_TOKEN = '7665761475:AAFW-pycIQ6vvGUWQuqXIKfPtgPG35fCV_4'
OPENWEATHER_API_KEY = 'a1d215ea39e2c5cda9574ba9534eb595'

# Lista de cidades japonesas
cidades_japonesas = [
    "Tóquio", "Osaka", "Quioto", "Hiroshima", "Nagoya", 
    "Yokohama", "Sapporo", "Fukuoka", "Kobe", "Sendai"
]

# Lista de cidades brasileiras
cidades_brasileiras = [
    "São Paulo", "Rio de Janeiro", "Belo Horizonte", "Brasília", "Salvador",
    "Fortaleza", "Pompeia", "Manaus", "Recife", "Porto Alegre",
    "Belém", "Goiânia", "São Luís", "Natal", "João Pessoa",
    "Garça", "Campo Grande", "Teresina", "Marilia", "Vitória"
]

# Lista de cidades alemãs
cidades_alemas = [
    "Berlim", "Munique", "Hamburgo", "Colônia", "Frankfurt",
    "Stuttgart", "Düsseldorf", "Dortmund", "Nuremberg", "Dresden",
    "Leipzig", "Hannover", "Bremen", "Duisburg", "Esslingen"
]

def centralizar(texto, largura):
    return texto.center(largura)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('🌤️ Olá! Eu sou o Bot do Clima! 🌤️ \n\nPara obter a previsão do tempo faça: \n/weather <cidade> ')

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) == 0:
        await update.message.reply_text('⚠️ Por favor, forneça uma cidade. Exemplo: /weather Londres')
        return

    city = ' '.join(context.args)
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric'

    try:
        response = requests.get(url)
        response.raise_for_status()  # Levanta um erro se a resposta não for 200
        data = response.json()

        temp = data['main']['temp']
        weather_description = data['weather'][0]['description']
        humidity = data['main']['humidity']
        temp_max = data['main']['temp_max']
        temp_min = data['main']['temp_min']
                ##### Troca as descrições do clima######
        if weather_description == 'clear sky':
            weather_description = 'Céu Claro, dia iluminado, perfeito para uma colheita e plantio! 🌱'
            emoji = '☀️'
        elif weather_description == 'broken clouds':
            weather_description = 'Céu parcialmente nublado, pouco risco de chuva, bom para uma colheita! 🌱'
            emoji = '☁️'
        elif weather_description == 'scattered clouds':
            weather_description = 'Céu com poucas nuvens, alta possibilidade de Sol, bom para uma colheita! 🌱'
            emoji = '🌤️'
        elif weather_description == 'overcast clouds':
            weather_description = 'Céu com muitas nuvens, alerta de Chuva, cuidado com o plantio e colheita! 🌱'
            emoji = '🌧️'
        elif weather_description == 'light rain':
            weather_description = 'Céu com cara de chuva, cuidado com a chuva leve, plantio e sua colheita! 🌱'
            emoji = '💧'
        else:
            emoji = '🌥️'

        # Verifica se a cidade é japonesa, brasileira ou alemã e adiciona a bandeira
        bandeira = ''
        city_normalized = city.strip().title()  # Normaliza a capitalização da cidade
        if city_normalized in cidades_japonesas:
            bandeira = '🇯🇵 '  # Bandeira do Japão
        elif city_normalized in cidades_brasileiras:
            bandeira = '🇧🇷 '  # Bandeira do Brasil
        elif city_normalized in cidades_alemas:
            bandeira = '🇩🇪 '  # Bandeira da Alemanha
        
        # Parâmetros da mensagem
        cidade = f'{bandeira}{city_normalized}'
        temperatura = f'A temperatura é {temp}°C'
        clima = f' {weather_description}'
        umidade = f'A umidade da cidade é de {humidity}%'
        maxima = f'{temp_max}'
        minima = f'{temp_min}'
        
        # Mensagem que o bot vai enviar
        await update.message.reply_text(
            f'| 🏙️ cidade: {cidade} |\n'
            f'| temperatura: {temperatura} 🌡️ |\n'
            f'| clima: {clima} {emoji} |\n'
            f'| umidade: {umidade} 💧 |\n'
            
            f'| maxima: {maxima} 🥵 |  \n'
            f'| minima: {minima}  🥶 |'
        )
    
    except requests.exceptions.HTTPError:
        await update.message.reply_text('❌ Cidade não encontrada. Tente outra! 🌧️')
    except Exception as e:
        await update.message.reply_text('😔 Ocorreu um erro. Tente novamente mais tarde.')
        print(e)

def main():
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("weather", weather))

    application.run_polling()

if __name__ == '__main__':
    main()
