# -*- coding: utf-8 -*-
# @File: errors.py
# @Author: https://github.com/ohhal
# @Date: 2021/01/27
# @Desc: 错误


def ErrorAnti(error):
    '''Anti错误'''
    errors = {
        'ERROR_KEY_DOES_NOT_EXIST': '在系统中找不到帐户授权密钥',
        'ERROR_NO_SLOT_AVAILABLE': '目前没有空闲的验证码工作人员，请稍后再试或尝试 在此处提高最高出价。',
        'ERROR_ZERO_CAPTCHA_FILESIZE': '您要上传的验证码的大小小于100个字节。',
        'ERROR_TOO_BIG_CAPTCHA_FILESIZE': '您要上传的验证码的大小超过500,000字节',
        'ERROR_ZERO_BALANCE': '帐户为0或负余额',
        'ERROR_IP_NOT_ALLOWED': '您的IP不允许使用当前帐户密钥进行请求。',
        'ERROR_CAPTCHA_UNSOLVABLE': '验证码无法由5位不同的工人解决',
        'ERROR_BAD_DUPLICATES': '100％识别功能由于缺乏猜测尝试而无法使用',
        'ERROR_NO_SUCH_METHOD': '使用不存在的方法向API请求',
        'ERROR_IMAGE_TYPE_NOT_SUPPORTED': '无法通过其exif标头确定验证码文件类型，或者不支持图像类型。唯一允许的格式是JPG，GIF，PNG',
        'ERROR_NO_SUCH_CAPCHA_ID': '您要求的验证码不存在于您当前的验证码列表中或已过期。',
        'ERROR_FACTORY_SERVER_BAD_JSON': 'JSON响应不正确，已损坏',
        'ERROR_IP_BLOCKED': '由于API使用不当，您的IP被阻止',
        'ERROR_TASK_ABSENT': 'Task属性为空或未在createTask方法中设置。请参阅API v2文档。',
        'ERROR_TASK_NOT_SUPPORTED': '任务类型不受支持或打印不正确。请检查任务对象中的\“ type \”参数。',
        'ERROR_INCORRECT_SESSION_DATA': '缺少一些连续用户仿真所需的值。',
        'ERROR_PROXY_CONNECT_REFUSED': '无法连接到与任务相关的代理，连接被拒绝',
        'ERROR_PROXY_CONNECT_TIMEOUT': '无法连接到与任务相关的代理，连接超时',
        'ERROR_PROXY_READ_TIMEOUT': '与任务代理的连接已超时',
        'ERROR_PROXY_BANNED': '代理IP被目标服务禁止',
        'ERROR_RECAPTCHA_TIMEOUT': 'Recaptcha任务超时，可能是由于代理服务器或Google服务器运行缓慢。',
        'ERROR_TOKEN_EXPIRED': '验证码提供者服务器报告其他变量令牌已过期。请使用新令牌重试。',
    }
    try:
        return errors[error]
    except Exception:
        return error


def ErrorConfluence(error):
    '''Confluence错误'''
    errors = {
        'ERROR_KEY_DOES_NOT_EXIST': '在系统中找不到或格式错误的帐户授权密钥（长度为）',
        'ERROR_ZERO_CAPTCHA_FILESIZE': '您要上传的验证码的大小小于100个字节。',
        'ERROR_TOO_BIG_CAPTCHA_FILESIZE': '您要上传的验证码的大小超过50,000个字节。',
        'ERROR_ZERO_BALANCE': '帐户余额为零',
        'ERROR_IP_NOT_ALLOWED': '您的IP不允许使用当前帐户密钥进行请求',
        'ERROR_CAPTCHA_UNSOLVABLE': '服务不支持这种类型的验证码，或者图像不包含答案，也许太吵了。这也可能意味着图像已损坏或渲染不正确。',
        'ERROR_NO_SUCH_CAPCHA_ID': '找不到您要求的验证码。确保仅在上传后5分钟内请求状态更新。',
        'WRONG_CAPTCHA_ID': '找不到您要求的验证码。确保仅在上传后5分钟内请求状态更新。',
        'CAPTCHA_NOT_READY': '验证码尚未解决',
        'ERROR_IP_BANNED': '您使用错误的api密钥超出了请求的限制，请在控制面板中检查api密钥的正确性，过一段时间后再试一次',
        'ERROR_NO_SUCH_METHOD': '此方法不受支持或为空',
        'ERROR_TOO_MUCH_REQUESTS': '您已超出接收一项任务答案的请求限制。尝试在2秒内请求任务结果不超过1次。'
    }
    try:
        return errors[error]
    except Exception:
        return error


def Error2Captcha(error):
    '''2Captcha错误'''
    errors = {
        'ERROR_WRONG_USER_KEY': '您提供的关键参数值格式错误，应包含32个符号。停止发送请求。检查您的API密钥。',
        'ERROR_KEY_DOES_NOT_EXIST': '您提供的密钥不存在。',
        'ERROR_ZERO_BALANCE': '您的请求中缺少pageurl参数。',
        'ERROR_PAGEURL': '帐户余额为零',
        'ERROR_NO_SLOT_AVAILABLE': '未正常解决该验证码',
        'ERROR_ZERO_CAPTCHA_FILESIZE': '图像大小小于100个字节。',
        'ERROR_TOO_BIG_CAPTCHA_FILESIZE': '图像大小超过100 kB。',
        'ERROR_WRONG_FILE_EXTENSION': '图片文件的扩展名不受支持。接受的扩展名：jpg，jpeg，gif，png。',
        'ERROR_IMAGE_TYPE_NOT_SUPPORTED': '服务器无法识别图像文件类型。',
        'ERROR_UPLOAD': '服务器无法从您的POST请求中获取文件数据。如果您的POST请求格式错误或base64数据不是有效的base64映像，则会发生这种情况。',
        'ERROR_IP_NOT_ALLOWED': '该请求是从不在您允许的IP列表中的IP发送的。',
        'IP_BANNED': '由于多次频繁尝试使用错误的授权密钥访问服务器，因此您的IP地址被禁止。',
        'ERROR_BAD_TOKEN_OR_PAGEURL': '您的请求包含无效的googlekey和pageurl对',
        'ERROR_GOOGLEKEY': '这表示您要求中提供的sitekey值不正确：空白或格式错误。',
        'ERROR_CAPTCHAIMAGE_BLOCKED': '您发送的图像在我们的数据库中被标记为无法识别。',
        'TOO_MANY_BAD_IMAGES': '您发送了太多无法识别的图像',
        'MAX_USER_TURN': '您在3秒钟内对in.php发出了60多个请求。您的帐户被禁止10秒钟。禁令将自动解除。',
        'ERROR_BAD_PARAMETERS': '如果您将ReCaptcha提交为图像，但您的请求缺少针对工人的说明，则会返回错误代码。',
        'ERROR_BAD_PROXY': '通过代理服务器发送验证码时，您会收到此错误代码，该验证码被我们的API标记为BAD。',
        'CAPCHA_NOT_READY': '您的验证码尚未解决。',
        'ERROR_CAPTCHA_UNSOLVABLE': '我们无法解决您的验证码-我们的三名工作人员无法解决该问题，或者我们在90秒内没有收到答复（ReCaptcha V2为300秒）。我们不会就该请求向您收费。',
        'ERROR_WRONG_ID_FORMAT': '您提供的验证码ID格式错误。ID只能包含数字。',
        'ERROR_WRONG_CAPTCHA_ID': '您提供的验证码ID不正确。',
        'ERROR_BAD_DUPLICATES': '启用100％准确性功能时，将返回错误。该错误表示已达到最大尝试次数，但未找到最小匹配数。',
        'REPORT_NOT_RECORDED': '如果您已经投诉了许多正确解决的验证码（超过40％），则会将错误返回到您的报告请求中。或者，如果您提交验证码后超过15分钟。',
        'ERROR_DUPLICATE_REPORT': '如果您尝试多次报告同一验证码，则会将错误返回给您的报告请求。',
        'ERROR_TOKEN_EXPIRED': 'challenge您提供的值已过期。',
        'ERROR_EMPTY_ACTION': '动作参数丢失或没有为action 参数提供值。',
        'ERROR_PROXY_CONNECTION_FAILED': '我们无法通过您的代理服务器加载验证码'
    }
    try:
        return errors[error]
    except Exception:
        return error
