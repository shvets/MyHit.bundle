# -*- coding: utf-8 -*-

from http_service import HttpService

class MyHitService(HttpService):
    URL = 'https://my-hit.org'

    def available(self):
        document = self.fetch_document(self.URL)

        return document.xpath('//div[@class="container"]/div[@class="row"]')

    def get_movies(self, path):
        list = []

        document = self.fetch_document(self.URL + path)

        items = document.xpath('//div[@class="film-list"]/div[@class="row"]')

        for item in items:
            link = item.xpath('div/a')[0]

            path = link.xpath('@href')[0]
            name = link.get("title")
            name = name[:len(name)-18]
            thumb = self.URL + link.xpath('div/img/@src')[0]

            list.append({'path': path, 'thumb': thumb, 'name': name})

        return list

    def get_urls(self, path):
        content = self.fetch_content(self.URL + path)

        document = self.to_document(content)

        script = document.xpath('//div[@class="row"]/div/script')[1].text_content()

        index1 = script.find("file:")
        index2 = script.find(".f4m")

        url = script[index1+6:index2] + ".f4m"

        return [url]

    def get_play_list_urls(self, url):
        play_list = self.get_play_list(url)

        # print(play_list)

        lines = play_list.splitlines()

        urls = []

        for line in lines:
            if line[:1] != '#':
                urls.append(line)

        return urls

    def get_play_list2(self, base_url, url):
        lines = self.http_request(url).read().splitlines()

        new_lines = []

        for line in lines:
            if line[:1] == '#':
                new_lines.append(line)
            else:
                new_lines.append(base_url[:len(base_url) - len('manifest.m3u8') - 1] + '/' + line)

        return "\n".join(new_lines)