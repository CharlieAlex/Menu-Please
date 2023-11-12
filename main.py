# Import Packages
from config import *
from output.menu import make_menu
from linebot.models import (
    MessageEvent, TextSendMessage,
    TextMessage, StickerSendMessage, LocationMessage
    )

@handler.add(MessageEvent, message=TextMessage)
def echo_text(event):
    '''
    Reply the text message.
    '''
    received_message = event.message.text

    try:
        if received_message in location_dict.keys():
            loc = location_dict[received_message]
            sent_message = TextSendMessage(text=make_menu(loc))
        else:
            sent_message = StickerSendMessage(package_id='6359', sticker_id='11069851')
    except Exception as e:
        sent_message = TextSendMessage(text=str(e))

    line_bot_api.reply_message(event.reply_token, sent_message)

@handler.add(MessageEvent, message=LocationMessage)
def echo_location(event):
    '''
    Reply the location message.
    '''
    received_location = [event.message.longitude, event.message.latitude]

    try:
        sent_message = TextSendMessage(text=make_menu(received_location))
    except Exception as e:
        sent_message = TextSendMessage(text=str(e))

    line_bot_api.reply_message(event.reply_token, sent_message)

# Main
if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port)