"""
sample config module
run "cp config.sample.py config.py" to create local config
edit config.py functions to override default bot behavior
"""

__name__ = 'localConfig'
__package__ = 'ringcentral_bot_framework'

import pydash as _
import json

def helpMsg(botId, groupId, user, authed = False):
  authUrl = user.getAuthUri(groupId, botId)
  loginStr = ''
  if authed == False:
    loginStr = f' I **needs your authorization** before I can process your cmd. [Click here]({authUrl}) to authorize the bot.'
  return f'''Hello, I am the assistant bot. Please reply "@![:Person]({botId}) **cmd**" if you want me to show your user/company infomation.{loginStr}

**cmd** list

**user info** -- show your user info
**company info** -- show your company info
  '''

def botJoinPrivateChatAction(bot, groupId, user, dbAction):
  """
  bot join private chat event handler
  bot could send some welcome message or help, or something else
  """
  bot.sendMessage(
    groupId,
    {
      'text': helpMsg(bot.id, groupId, user)
    }
  )

def botGotPostAddAction(
  bot,
  groupId,
  creatorId,
  user,
  text,
  dbAction,
  handledByExtension
):
  """
  bot got group chat message: text
  bot could send some response
  """

  if not f'![:Person]({bot.id})' in text:
    return

  msg = ''

  if user.id == '':
    msg = helpMsg(bot.id, groupId, user)

  elif 'user info' in text:
    userInfo = user.platform.get('/account/~/extension/~')
    txt = json.loads(userInfo.text())
    txt = json.dumps(txt, indent=2)
    msg = f'![:Person]({user.id}) your user info json is:\n' + txt

  elif 'company info' in text:
    compInfo = user.platform.get('/account/~')
    txt = json.loads(compInfo.text())
    txt = json.dumps(txt, indent=2)
    msg = f'![:Person]({user.id}) your company info json is:\n' + txt

  else:
    msg = helpMsg(bot.id, groupId, user, True)

  bot.sendMessage(
    groupId,
    {
      'text': msg
    }
  )
