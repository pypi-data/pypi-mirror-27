# -*- coding: utf-8 -*-
#
# Telegram Notify Wrapper
#
# Copyright (C) 2017 Chris Caron <lead2gold@gmail.com>
#
# This file is part of apprise.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# To use this plugin, you need to first access https://api.telegram.org
# You need to create a bot and acquire it's Token Identifier (bot_token)
#
# Basically you need to create a chat with a user called the 'BotFather'
# and type: /newbot
#
# Then follow through the wizard, it will provide you an api key
# that looks like this:123456789:alphanumeri_characters
#
# For each chat_id a bot joins will have a chat_id associated with it.
# You will need this value as well to send the notification.
#
# Log into the webpage version of the site if you like by accessing:
#    https://web.telegram.org
#
# You can't check out to see if your entry is working using:
#    https://api.telegram.org/botAPI_KEY/getMe
#
#    Pay attention to the word 'bot' that must be present infront of your
#    api key that the BotFather gave you.
#
#  For example, a url might look like this:
#    https://api.telegram.org/bot123456789:alphanumeri_characters/getMe
#
import requests
import re

from json import loads
from json import dumps

from .NotifyBase import NotifyBase
from .NotifyBase import NotifyFormat
from .NotifyBase import HTTP_ERROR_MAP

from ..utils import compat_is_basestring

# Token required as part of the API request
# allow the word 'bot' infront
VALIDATE_BOT_TOKEN = re.compile(
    r'(bot)?(?P<key>[0-9]+:[A-Za-z0-9_-]+)/*$',
    re.IGNORECASE,
)

# Chat ID is required
# If the Chat ID is positive, then it's addressed to a single person
# If the Chat ID is negative, then it's targeting a group
IS_CHAT_ID_RE = re.compile(
    r'(@*(?P<idno>-?[0-9]{1,32})|(?P<name>[a-z_-][a-z0-9_-]*))',
    re.IGNORECASE,
)

# Disable image support for now
# The stickers/images are kind of big and consume a lot of space
# It's not as appealing as just having the post not contain
# an image at all.
TELEGRAM_IMAGE_XY = None

# Used to break path apart into list of chat identifiers
CHAT_ID_LIST_DELIM = re.compile(r'[ \t\r\n,#\\/]+')


class NotifyTelegram(NotifyBase):
    """
    A wrapper for Telegram Notifications
    """

    # The default secure protocol
    secure_protocol = 'tgram'

    # Telegram uses the http protocol with JSON requests
    notify_url = 'https://api.telegram.org/bot'

    def __init__(self, bot_token, chat_ids, **kwargs):
        """
        Initialize Telegram Object
        """
        super(NotifyTelegram, self).__init__(
            title_maxlen=250, body_maxlen=4096,
            image_size=TELEGRAM_IMAGE_XY, **kwargs)

        if bot_token is None:
            raise TypeError(
                'The Bot Token specified is invalid.'
            )

        result = VALIDATE_BOT_TOKEN.match(bot_token.strip())
        if not result:
            raise TypeError(
                'The Bot Token specified (%s) is invalid.' % bot_token,
            )

        # Store our API Key
        self.bot_token = result.group('key')

        if compat_is_basestring(chat_ids):
            self.chat_ids = filter(bool, CHAT_ID_LIST_DELIM.split(
                chat_ids,
            ))

        elif isinstance(chat_ids, (set, tuple, list)):
            self.chat_ids = list(chat_ids)

        else:
            self.chat_ids = list()

        if self.user:
            # Treat this as a channel too
            self.chat_ids.append(self.user)

        # Bot's can't send messages to themselves which is fair enough
        # but if or when they can, this code will allow a default fallback
        # solution if no chat_id and/or channel is specified
        # if len(self.chat_ids) == 0:
        #
        #     chat_id = self._get_chat_id()
        #     if chat_id is not None:
        #         self.logger.warning(
        #             'No chat_id or @channel was specified; ' +\
        #             'using detected bot_chat_id (%d).' % chat_id,
        #         )
        #         self.chat_ids.append(str(chat_id))

        if len(self.chat_ids) == 0:
            self.logger.warning('No chat_id(s) were specified.')
            raise TypeError('No chat_id(s) were specified.')

    def _get_chat_id(self):
        """
        This function retrieves the chat id belonging to the key specified
        """
        headers = {
            'User-Agent': self.app_id,
            'Content-Type': 'application/json',
        }

        url = '%s%s/%s' % (
            self.notify_url,
            self.bot_token,
            'getMe'
        )

        self.logger.debug('Telegram (Detection) GET URL: %s' % url)

        chat_id = None
        try:
            r = requests.post(url, headers=headers)
            if r.status_code == requests.codes.ok:
                # Extract our chat ID
                result = loads(r.text)
                if result.get('ok', False) is True:
                    chat_id = result['result'].get('id')
                    if chat_id <= 0:
                        chat_id = None
            else:
                # We had a problem
                try:
                    # Try to get the error message if we can:
                    error_msg = loads(r.text)['description']

                except:
                    error_msg = None

                try:
                    if error_msg:
                        self.logger.warning(
                            'Failed to lookup Telegram chat_id from '
                            'apikey: (%s) %s.' % (r.status_code, error_msg))

                    else:
                        self.logger.warning(
                            'Failed to lookup Telegram chat_id from '
                            'apikey: %s (error=%s).' % (
                                HTTP_ERROR_MAP[r.status_code],
                                r.status_code))

                except IndexError:
                    self.logger.warning(
                        'Failed to lookup Telegram chat_id from '
                        'apikey: (error=%s).' % r.status_code)

        except requests.ConnectionError as e:
            self.logger.warning(
                'A Connection error occured looking up Telegram chat_id '
                'from apikey.')
            self.logger.debug('Socket Exception: %s' % str(e))

        return chat_id

    def notify(self, title, body, notify_type, **kwargs):
        """
        Perform Telegram Notification
        """

        headers = {
            'User-Agent': self.app_id,
            'Content-Type': 'application/json',
        }

        # error tracking (used for function return)
        has_error = False

        image_url = None
        image_content = self.image_raw(notify_type)
        if image_content is not None:
            # prepare our image URL
            image_url = '%s%s/%s' % (
                self.notify_url,
                self.bot_token,
                'sendPhoto'
            )

            # Set up our upload
            files = {'photo': ('%s.png' % notify_type, image_content)}

        url = '%s%s/%s' % (
            self.notify_url,
            self.bot_token,
            'sendMessage'
        )

        payload = {}

        if self.notify_format == NotifyFormat.HTML:
            # HTML
            payload['parse_mode'] = 'HTML'
            payload['text'] = '<b>%s</b>\r\n%s' % (title, body)

        else:
            # Text
            # payload['parse_mode'] = 'Markdown'
            payload['parse_mode'] = 'HTML'
            payload['text'] = '<b>%s</b>\r\n%s' % (
                NotifyBase.escape_html(title),
                NotifyBase.escape_html(body),
            )

        # Create a copy of the chat_ids list
        chat_ids = list(self.chat_ids)
        while len(chat_ids):
            chat_id = chat_ids.pop(0)
            chat_id = IS_CHAT_ID_RE.match(chat_id)
            if not chat_id:
                self.logger.warning(
                    "The specified chat_id '%s' is invalid; skipping." % (
                        chat_id,
                    )
                )
                continue

            if chat_id.group('name') is not None:
                # Name
                payload['chat_id'] = '@%s' % chat_id.group('name')

            else:
                # ID
                payload['chat_id'] = chat_id.group('idno')

            if image_url is not None:
                image_payload = {
                    'chat_id': payload['chat_id'],
                    'disable_notification': True,
                }

                self.logger.debug(
                    'Telegram (image) POST URL: %s (cert_verify=%r)' % (
                        image_url, self.verify_certificate))

                self.logger.debug(
                    'Telegram (image) Payload: %s' % str(image_payload))

                try:
                    r = requests.post(
                        image_url,
                        data=image_payload,
                        headers={
                            'User-Agent': self.app_id,
                        },
                        files=files,
                        verify=self.verify_certificate,
                    )
                    if r.status_code != requests.codes.ok:
                        # We had a problem

                        try:
                            # Try to get the error message if we can:
                            error_msg = loads(r.text)['description']
                        except:
                            error_msg = None

                        try:
                            if error_msg:
                                self.logger.warning(
                                    'Failed to send Telegram Image:%s '
                                    'notification: (%s) %s.' % (
                                        payload['chat_id'],
                                        r.status_code, error_msg))

                            else:
                                self.logger.warning(
                                    'Failed to send Telegram Image:%s '
                                    'notification: %s (error=%s).' % (
                                        payload['chat_id'],
                                        HTTP_ERROR_MAP[r.status_code],
                                        r.status_code))

                        except IndexError:
                            self.logger.warning(
                                'Failed to send Telegram Image:%s '
                                'notification (error=%s).' % (
                                    payload['chat_id'],
                                    r.status_code))

                        has_error = True
                        continue

                except requests.ConnectionError as e:
                    self.logger.warning(
                        'A Connection error occured sending Telegram:%s ' % (
                            payload['chat_id']) + 'notification.'
                    )
                    self.logger.debug('Socket Exception: %s' % str(e))
                    has_error = True
                    continue

            self.logger.debug('Telegram POST URL: %s' % url)
            self.logger.debug('Telegram POST URL: %s (cert_verify=%r)' % (
                url, self.verify_certificate,
            ))
            self.logger.debug('Telegram Payload: %s' % str(payload))

            try:
                r = requests.post(
                    url,
                    data=dumps(payload),
                    headers=headers,
                    verify=self.verify_certificate,
                )
                if r.status_code != requests.codes.ok:
                    # We had a problem

                    try:
                        # Try to get the error message if we can:
                        error_msg = loads(r.text)['description']
                    except:
                        error_msg = None

                    try:
                        if error_msg:
                            self.logger.warning(
                                'Failed to send Telegram:%s '
                                'notification: (%s) %s.' % (
                                    payload['chat_id'],
                                    r.status_code, error_msg))

                        else:
                            self.logger.warning(
                                'Failed to send Telegram:%s '
                                'notification: %s (error=%s).' % (
                                    payload['chat_id'],
                                    HTTP_ERROR_MAP[r.status_code],
                                    r.status_code))

                    except IndexError:
                        self.logger.warning(
                            'Failed to send Telegram:%s '
                            'notification (error=%s).' % (
                                payload['chat_id'], r.status_code))

                    # self.logger.debug('Response Details: %s' % r.raw.read())

                    # Return; we're done
                    has_error = True

            except requests.ConnectionError as e:
                self.logger.warning(
                    'A Connection error occured sending Telegram:%s ' % (
                        payload['chat_id']) + 'notification.'
                )
                self.logger.debug('Socket Exception: %s' % str(e))
                has_error = True

            if len(chat_ids):
                # Prevent thrashing requests
                self.throttle()

        return has_error

    @staticmethod
    def parse_url(url):
        """
        Parses the URL and returns enough arguments that can allow
        us to substantiate this object.

        """
        # super() is formatted slightly different when dealing with
        # static method inheritance
        results = NotifyBase.parse_url(url)

        if results:
            # We're done early
            return results

        # This is a dirty hack; but it's the only work around to
        # tgram:// messages since the bot_token has a colon in it.
        # It invalidates an normal URL.

        # This hack searches for this bogus URL and corrects it
        # so we can properly load it further down. The other
        # alternative is to ask users to actually change the colon
        # into a slash (which will work too), but it's more likely
        # to cause confusion... So this is the next best thing
        tgram = re.match(
            r'(?P<protocol>%s://)(bot)?(?P<prefix>([a-z0-9_-]+)'
            r'(:[a-z0-9_-]+)?@)?(?P<btoken_a>[0-9]+):+'
            r'(?P<remaining>.*)$' % 'tgram',
            url, re.I)

        if not tgram:
            # Content is simply not parseable
            return None

        if tgram.group('prefix'):
            # Try again
            result = NotifyBase.parse_url(
                '%s%s%s/%s' % (
                    tgram.group('protocol'),
                    tgram.group('prefix'),
                    tgram.group('btoken_a'),
                    tgram.group('remaining'),
                ),
            )

        else:
            # Try again
            result = NotifyBase.parse_url(
                '%s%s/%s' % (
                    tgram.group('protocol'),
                    tgram.group('btoken_a'),
                    tgram.group('remaining'),
                ),
            )

        # The first token is stored in the hostnamee
        bot_token_a = result['host']

        # Now fetch the remaining tokens
        try:
            bot_token_b = filter(
                bool, NotifyBase.split_path(result['fullpath']))[0]

            bot_token = '%s:%s' % (bot_token_a, bot_token_b)

        except (AttributeError, IndexError):
            # Force a bad value that will get caught in parsing later
            bot_token = None

        try:
            chat_ids = ','.join(
                filter(bool, NotifyBase.split_path(result['fullpath']))[1:])

        except (AttributeError, IndexError):
            # Force some bad values that will get caught
            # in parsing later
            chat_ids = None

        # Return our results
        return result + {
            'bot_token': bot_token,
            'chat_ids': chat_ids,
        }.items()
