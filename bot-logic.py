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

def botJoinPrivateChatAction(bot, groupId, user):
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
  text = ''
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

def botAuthAction(bot):
  '''
  After bot auth success,
  can do some bot actions
  default: do nothing
  '''
  return

def userAuthSuccessAction(bot, groupId, userId):
  """
  user auth bot app to access user data success,
  bot would do something
  default: send login success message to chatgroup
  if you only have bot app, it is not needed
  """
  bot.sendMessage(groupId, {
    'text': f'![:Person]({userId}), you have successfully authorized me to access your RingCentral data!'
  })

def userAddGroupInfoAction(bot, user, groupId):
  """
  user add group and bot connect info,
  bot or user could do something about it,
  default: do nothing
  if you only have bot app, it is not needed
  """
  return

def userAuthSuccessHtml(user, conf):
  """
  user auth success, would see this html from browser
  if you only have bot app, it is not needed
  """
  return '<div style="text-align: center;font-size: 20px;border: 5px solid #08c;padding: 30px;">You have authorized the bot to access your RingCentral data! Please close this page and get back to Glip</div>'

def userEventAction(
  user,
  eventType,
  event,
  getBot
):
  """
  bot got subscribed user event,
  do something about it
  default: post to chatgroup about the event
  if you only have bot app, it is not needed
  """
  return

def botFilters():
  '''
  customize bot filters to subscribe
  '''
  return [
    '/restapi/v1.0/glip/posts',
    '/restapi/v1.0/glip/groups'
  ]

def userFilters():
  '''
  customize user filters to subscribe
  '''
  return [
    '/restapi/v1.0/account/~/extension/~/message-store'
  ]