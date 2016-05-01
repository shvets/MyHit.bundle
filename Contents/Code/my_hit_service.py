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
            new_path = self.build_url(path, p=str(page))

        return new_path

    def get_all_movies(self, page=1):
        return self.get_movies("/film/", page=page)

    def get_all_serials(self, page=1):
        return self.get_serials("/serial/", page=page)

    def get_popular_movies(self, page=1):
        return self.get_movies("/film/?s=3", page=page)

    def get_popular_serials(self, page=1):
        return self.get_serials("/serial/?s=3", page=page)

    # def get_selected_movies(self, page=1):
    #     return self.get_movies("/selection/film", page=page)
    #
    # def get_selected_serials(self, page=1):
    #     return self.get_movies("/selection/serial", page=page)

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

    def get_serials(self, path, page=1):
        list = []

        page_path = self.get_page_path(path, page)

        document = self.fetch_document(self.URL + page_path)

        items = document.xpath('//div[@class="serial-list"]/div[@class="row"]')

        for item in items:
            link = item.xpath('div/a')[0]

            href = link.xpath('@href')[0]
            name = link.get("title")
            name = name[:len(name) - 18]
            thumb = self.URL + link.xpath('div/img/@src')[0]

            list.append({'path': href, 'thumb': thumb, 'name': name})

        pagination = self.extract_pagination_data(page_path, page=page)

        return {"movies": list, "pagination": pagination["pagination"]}

    def get_soundtracks(self, page=1):
        list = []

        page_path = self.get_page_path("/soundtrack/", page)

        document = self.fetch_document(self.URL + page_path)

        items = document.xpath('//div[@class="soundtrack-list"]/div[@class="row"]/div')

        for item in items:
            link1 = item.xpath('div/b/a')[0]
            link2 = item.xpath('a')[0]

            href = link1.xpath('@href')[0]
            name = link1.text_content()

            thumb = self.URL + link2.xpath('img/@src')[0]

            list.append({'path': href, 'thumb': thumb, 'name': name})

        pagination = self.extract_pagination_data(page_path, page=page)

        return {"movies": list, "pagination": pagination["pagination"]}

    def get_selections(self, page=1):
        list = []

        page_path = self.get_page_path("/selection/", page)

        document = self.fetch_document(self.URL + page_path)

        items = document.xpath('//div[@class="selection-list"]/div[@class="row"]/div')

        for item in items:
            link1 = item.xpath('div/b/a')[0]
            link2 = item.xpath('a')[0]

            href = link1.xpath('@href')[0]
            name = link1.text_content()

            id = href[2:len(href) - 1]

            thumb = self.URL + link2.xpath('img/@src')[0]

            list.append({'id': id, 'thumb': thumb, 'name': name})

        pagination = self.extract_pagination_data(page_path, page=page)

        return {"movies": list, "pagination": pagination["pagination"]}

    def get_selection(self, id, page=1):
        list = []

        page_path = self.get_page_path("/selection/" + id + '/', page)

        document = self.fetch_document(self.URL + page_path)

        items = document.xpath('//div[@class="selection-view"]/div')

        for item in items:
            link = item.xpath('div/a')[0]

            href = link.xpath('@href')[0]
            name = link.get("title")

            name = name[:len(name) - 18]

            thumb = self.URL + link.xpath('div/img/@src')[0]

            list.append({'path': href, 'thumb': thumb, 'name': name})

        pagination = self.extract_pagination_data(page_path, page=page)

        return {"movies": list, "pagination": pagination["pagination"]}

    def get_source_url(self, path):
        content = self.fetch_content(self.URL + path)

        document = self.to_document(content)

        script = document.xpath('//div[@class="row"]/div/script')[1].text_content()

        index1 = script.find("file:")
        index2 = script.find(".f4m")

        return script[index1 + 6:index2] + ".f4m"

    def get_metadata(self, url):
        bandwidth = url[url.find("chunklist_b")+11:url.find(".m3u8")]

        source_url = self.get_base_url(url) + "/manifest.f4m"

        document = self.fetch_document(source_url)

        data = []

        media_block = document.xpath("//manifest/media")

        for media in media_block:
            data.append({
                'width': int(media.get('width')),
                'height':int(media.get('height')),
                'bitrate': int(media.get('bitrate')) * 1000,
                'url': media.get('url')
            })

        location = -1
        for index2, item in enumerate(data):
            if item['url'].find(bandwidth) >= 0:
                location = index2
                break

        return data[location]

    def get_urls(self, path):
        url = self.get_source_url(path)

        new_url = url.replace('.f4m', '.m3u8')

        urls = self.get_play_list_urls(new_url)

        return urls

    def extract_pagination_data(self, path, page):
        page = int(page)

        document = self.fetch_document(self.URL + path)

        pages = 1

        response = {}

        pagination_root = document.xpath('//div[@class="container"]/div[@class="row"]/div/div[@class="row"]')

        if pagination_root:
            pagination_block = pagination_root[1]

            text = pagination_block[0].text_content()

            pos1 = text.find(":")
            pos2 = text.find("(")

            items = int(text[pos1+1:pos2])

            pages = items / 24

            if items % 24 > 0:
                pages = pages +1

        response["pagination"] = {
            "page": page,
            "pages": pages,
            "has_previous": page > 1,
            "has_next": page < pages,
        }

        return response

    def get_play_list_urls3(self, url):
        base_url = url[:len(url) - len('manifest.f4m')]

        buffer = self.http_request(url).read()

        document = self.to_document(buffer)

        urls = []

        media_block = document.xpath("//manifest/media")

        for media in media_block:
            urls.append(base_url + media.get('url'))

        return urls


