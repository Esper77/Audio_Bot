import struct

import telebot
import uuid

TOKEN = "5880785142:AAEU12-MT3jdVPk6M5reRQvEIFG3-QOABtk"
bot = telebot.TeleBot(TOKEN)


def download_audio(message):
    voice_id = message.voice.file_id
    file_description = bot.get_file(voice_id)
    downloaded_file = bot.download_file(file_description.file_path)

    filename = 'audio/' + str(uuid.uuid4()) + '.oga'

    with open(filename, 'wb') as file:
        file.write(downloaded_file)

    return filename


def convert_audio(path):
    import subprocess
    src_filename = path
    dest_filename = path + '.wav'

    subprocess.run(['ffmpeg', '-i', src_filename, dest_filename])
    return dest_filename


def speed_up(path):
    import wave

    audio = wave.open(path)
    data = audio.readframes(audio.getnframes())
    values = struct.unpack(f'<{ len(data) // 2 }h', data)
    values2 = []

    audio_beat = wave.open("beat.wav")
    data_beat = audio_beat.readframes(audio_beat.getnframes())
    values_beat = struct.unpack(f'<{ len(data_beat) // 2 }h', data_beat)
    values2_beat = values_beat[0:len(values)]

    for i in range(len(values)):
        values2.append((values2_beat[i] + values[i])//2)

    data = struct.pack(f'<{ len(values2) }h', *values2)

    audio2 = wave.open(path + '.2.wav', 'wb')
    audio2.setnchannels(audio.getnchannels())
    audio2.setframerate(audio.getframerate())
    audio2.setsampwidth(audio.getsampwidth())
    audio2.writeframes(data)

    return path + '.2.wav'


@bot.message_handler(content_types=['voice'])
def voice(message):
    path = download_audio(message)
    path = convert_audio(path)
    path = speed_up(path)

    bot.send_audio(message.chat.id, open(path, 'rb').read())
    print(path)


bot.polling(none_stop=True)
