import wxpy
APPKEY='84c02de352f04e28a37e3956c50a7654'
tuling = wxpy.Tuling(APPKEY)

def bot_reply(my_friend):
    bot = wxpy.Bot()
# 使用图灵机器人自动与指定好友聊天
    @bot.register(my_friend)
    def reply_my_friend(msg):
        tuling.do_reply(msg)
    wxpy.embed()
