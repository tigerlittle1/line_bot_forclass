from flask import Flask, request, abort
import datetime
from Invoice import Invoice

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

Channel_Token = ""#填入Channel access token
Channel_Secret = ""#填入Channel secret

# Channel Access Token
line_bot_api = LineBotApi(Channel_Token) 
# Channel Secret
handler = WebhookHandler(Channel_Secret) 

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):

    get_massage = event.message.text
    print(get_massage)
    if get_massage == "現在時間":
        message = TextSendMessage(text=str(datetime.datetime))
    elif get_massage == "image":
        message = ImageSendMessage(
            original_content_url='https://img.hypesphere.com/2015-10-22-174039-60.jpg',
            preview_image_url='https://img.hypesphere.com/2015-10-22-174039-60.jpg'
        )
    elif get_massage == "video":
        try:
            message = VideoSendMessage(
                original_content_url='http://192.168.43.250/Videos/1.mp4',
                preview_image_url='https://img.hypesphere.com/2015-10-22-174039-60.jpg'
            )
            line_bot_api.reply_message(event.reply_token, message)
        except:
            message = TextSendMessage(text="影片錯誤")  # 回復訊息設定
    elif get_massage == "audio":
        try:
            message = AudioSendMessage(
                original_content_url='http://ys.yisell.com/yisell/pays2018050819052088/sound/yisell_sound_204914563156330_88012.m4a',
                duration=240000
            )
            line_bot_api.reply_message(event.reply_token, message)
        except:
            message = TextSendMessage(text="聲音錯誤")  # 回復訊息設定
    elif get_massage == "location":
        message = LocationSendMessage(
            title='my location',
            address='Tokyo',
            latitude=35.65910807942215,
            longitude=139.70372892916203
        )
    elif get_massage == "sticker":
        message = StickerSendMessage(
            package_id='4',
            sticker_id='260'
        )
    elif get_massage == "buttontemplate":
        message = TemplateSendMessage(
            alt_text = 'Buttons template',
            template = ButtonsTemplate(
                thumbnail_image_url='https://img.hypesphere.com/2015-10-22-174039-60.jpg',
                title='Menu',
                text='Please select',
                actions=[
                    PostbackTemplateAction(
                        label='postback',
                        text='postback text',
                        data='action=buy&itemid=1'
                    ),
                    MessageTemplateAction(
                        label='message',
                        text='message text'
                    ),
                    URITemplateAction(
                        label='uri',
                        uri='http://example.com/'
                    )
                ]
            )
        )
    elif get_massage == "confirmtemplate":
        message = TemplateSendMessage(
            alt_text='Confirm template',
            template=ConfirmTemplate(
                text='Are you sure?',
                actions=[
                    PostbackTemplateAction(
                        label='postback',
                        text='postback text',
                        data='data'
                    ),
                    MessageTemplateAction(
                        label='message',
                        text='message text'
                    )
                ]
            )
        )
    elif get_massage == "carouseltemplate":
        message = TemplateSendMessage(
            alt_text='Carousel template',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://www.smartm.com.tw/data/Images/ec/24/a5/4d/f6ff18b13a9728bea09279d.jpg',
                        title='this is menu1',
                        text='description1',
                        actions=[
                            PostbackTemplateAction(
                                label='postback1',
                                text='postback text1',
                                data='action=buy&itemid=1'
                            ),
                            MessageTemplateAction(
                                label='message1',
                                text='message text1'
                            ),
                            URITemplateAction(
                                label='uri1',
                                uri='https://www.smartm.com.tw/article/31363834cea3'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://is1-ssl.mzstatic.com/image/thumb/Video111/v4/9d/8e/34/9d8e34e2-2327-3840-c184-bf4a125c5d37/pr_source.lsr/268x0w.png',
                        title='this is menu2',
                        text='description2',
                        actions=[
                            PostbackTemplateAction(
                                label='postback2',
                                text='postback text2',
                                data='action=buy&itemid=2'
                            ),
                            MessageTemplateAction(
                                label='message2',
                                text='message text2'
                            ),
                            URITemplateAction(
                                label='uri2',
                                uri='https://itunes.apple.com/tw/movie/%E5%B0%8F%E5%B0%8F%E5%85%B5/id991371510'
                            )
                        ]
                    )
                ]
            )
        )
    elif get_massage == "imagecarouseltemplate":
        message = TemplateSendMessage(
            alt_text='ImageCarousel template',
            template=ImageCarouselTemplate(
                columns=[
                    ImageCarouselColumn(
                        image_url='https://img.hypesphere.com/2015-10-22-174039-60.jpg',
                        action=PostbackTemplateAction(
                            label='postback1',
                            text='postback text1',
                            data='data'
                        )
                    ),
                    ImageCarouselColumn(
                        image_url='https://img.hypesphere.com/2015-10-22-174039-60.jpg',
                        action=MessageTemplateAction(
                            label='Message',
                            text='Message text2',
                        )
                    )
                    ,
                    ImageCarouselColumn(
                        image_url='https://img.hypesphere.com/2015-10-22-174039-60.jpg',
                        action=URITemplateAction(
                            label='uri',
                            uri='http://example.com/'
                        )
                    )

                ]
            )
        )
    elif "發票對獎號碼"in get_massage:
        i = Invoice()
        i.set_date(109,1)
        number = i.get_number()
        text = "{}年{}月開獎號碼\n".format(i.year,i.moth)
        print(i.year,i.moth)
        for n in number:
            text = text+n+"\n"
        message = TextSendMessage(text=text)
    else:
        message = TextSendMessage(text=get_massage)#回復訊息設定
    line_bot_api.reply_message(event.reply_token, message)#回復訊息

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
