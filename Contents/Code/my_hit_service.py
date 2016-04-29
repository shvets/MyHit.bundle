# -*- coding: utf-8 -*-

from http_service import HttpService

class MyHitService(HttpService):
    URL = 'https://my-hit.org'

    def available(self):
        document = self.fetch_document(self.URL)

        return document.xpath('//div[@class="container"]/div[@class="row"]')

    def get_page_path(self, path, page=1):
        if page == 1:
            new_path = path
        else:
            new_path = path + "&p=" + str(page)

        return new_path

    def get_popular_movies(self, page=1):
        return self.get_movies("/film/?s=3", page=page)

    def get_movies(self, path, page=1):
        list = []

        page_path = self.get_page_path(path, page)

        document = self.fetch_document(self.URL + page_path)

        items = document.xpath('//div[@class="film-list"]/div[@class="row"]')

        for item in items:
            link = item.xpath('div/a')[0]

            href = link.xpath('@href')[0]
            name = link.get("title")
            name = name[:len(name)-18]
            thumb = self.URL + link.xpath('div/img/@src')[0]

            list.append({'path': href, 'thumb': thumb, 'name': name})

        pagination = self.extract_pagination_data(page_path, page=page)

        return {"movies": list, "pagination": pagination["pagination"]}

    def get_urls(self, path):
        content = self.fetch_content(self.URL + path)

        document = self.to_document(content)

        script = document.xpath('//div[@class="row"]/div/script')[1].text_content()

        index1 = script.find("file:")
        index2 = script.find(".f4m")

        url = script[index1+6:index2] + ".f4m"

        return [url]

    def extract_pagination_data(self, path, page):
        page = int(page)

        document = self.fetch_document(self.URL + path)

        pages = 1

        response = {}

        pagination_root = document.xpath('//div/ul[@class="pagination"]')

        if pagination_root:
            pagination_block = pagination_root[0]

            item_blocks = pagination_block.xpath('li')

            if item_blocks:
                pages = int(len(item_blocks)-2)

        response["pagination"] = {
            "page": page,
            "pages": pages,
            "has_previous": page > 1,
            "has_next": page < pages,
        }

        return response

    def get_play_list_urls(self, url):
        play_list = self.get_play_list(url)

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