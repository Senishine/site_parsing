import scrapy
from scrapy.http import HtmlResponse
import re
import json
from instaparser.items import InstaparseItem
from instaparser.ini import password


class InstaspiderSpider(scrapy.Spider):
    name = 'instaspider'
    allowed_domains = ['instagram.com']
    start_urls = ['http://instagram.com/']
    inst_login_link = 'https://www.instagram.com/accounts/login/ajax/'
    inst_login = 'marina.tarasova.7773'
    users_for_parse = ['elizawhitephoto', 'julyzorina']
    inst_user_followers_url = 'https://i.instagram.com/api/v1/friendships/{user_id}/followers/'
    inst_user_subscribers_url = 'https://i.instagram.com/api/v1/friendships/{user_id}/following/'
    inst_links = [inst_user_followers_url, inst_user_subscribers_url]
    inst_pwd = password

    def parse(self, response: HtmlResponse):
        csrf_token = self.fetch_csrf_token(response.text)

        yield scrapy.FormRequest(
            self.inst_login_link,
            method='POST',
            callback=self.login,
            formdata={'username': self.inst_login, 'enc_password': self.inst_pwd},
            headers={'X-CSRFToken': csrf_token}
        )

    def login(self, response: HtmlResponse):
        j_data = response.json()
        if j_data['authenticated']:
            for user_for_parse in self.users_for_parse:
                yield response.follow(f'/{user_for_parse}',
                                      callback=self.user_data_parse,
                                      cb_kwargs={'username': user_for_parse})

    def user_data_parse(self, response: HtmlResponse, username):
        user_data = self.fetch_user_id(response.text)
        user_id = user_data.get('id')
        for link in self.inst_links:
            max_id = 12
            info_url = f'{link.format(user_id=user_id, max_id=max_id)}'
            yield response.follow(info_url,
                                  callback=self.user_post_parse,
                                  cb_kwargs={'username': username,
                                             'user_id': user_id},
                                  headers={'User-Agent': 'Instagram 155.0.0.37.107'})

    def user_post_parse(self, response: HtmlResponse, username, user_id):
        data = response.json()
        next_max_page = data.get('next_max_id', None)
        if next_max_page:
            url_to_get = f'{self.inst_user_subscribers_url.format(user_id=user_id)}?count=12&max_id={next_max_page}'
            if 'followers' in response.url:
                url_to_get = f'{self.inst_user_followers_url.format(user_id=user_id)} \
                                ?count=12&max_id={next_max_page}&search_surface=follow_list_page'

            yield response.follow(url_to_get,
                                  callback=self.user_post_parse,
                                  cb_kwargs={'username': username,
                                             'user_id': user_id},
                                  headers={'User-Agent': 'Instagram 155.0.0.37.107'})

        user_list = data.get('users')
        for user in user_list:
            item = InstaparseItem(
                username=user.get('username', None),
                main_user=username,
                followers=True if 'followers' in response.url else False,
                full_name=user.get('full_name', None),
                user_id=user.get('pk', None),
                photo=user.get('profile_pic_url', None),
            )
            yield item

    def fetch_csrf_token(self, text):
        """Get csrf-token for auth"""
        match = re.search('\"csrf_token\":\"\\w+\"', text).group()
        return match.split(':').pop().replace(r'"', '')

    def fetch_user_id(self, text):
        """return dict with keys 'id' and 'username' """
        matched = re.findall(r'"owner":{(.*?)}', text)
        j_data = json.loads('{%s}' % matched[0])
        return j_data
