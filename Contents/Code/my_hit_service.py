# -*- coding: utf-8 -*-

import re

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

    def get_all_series(self, page=1):
        return self.get_series("/serial/", page=page)

    def get_popular_movies(self, page=1):
        return self.get_movies("/film/?s=3", page=page)

    def get_popular_series(self, page=1):
        return self.get_series("/serial/?s=3", page=page)

    def get_movies(self, path, page=1):
        data = []

        page_path = self.get_page_path(path, page)

        document = self.fetch_document(self.URL + page_path)

        items = document.xpath('//div[@class="film-list"]/div[@class="row"]')

        for item in items:
            link = item.xpath('div/a')[0]

            href = link.xpath('@href')[0]
            name = link.get("title")
            name = name[:len(name)-18]
            thumb = self.URL + link.xpath('div/img/@src')[0]

            data.append({'path': href, 'thumb': thumb, 'name': name})

        pagination = self.extract_pagination_data(page_path, page=page)

        return {"movies": data, "pagination": pagination["pagination"]}

    def get_media_data(self, path):
        data = {}

        document = self.fetch_document(self.URL + path)

        info_root = document.xpath('//div[@class="row"]/div')

        if len(info_root) > 0:
            info_node = info_root[0].xpath('//ul[@class="list-unstyled"]')

            for item in info_node[0]:
                line = item.text_content()

                index = line.find(':')

                key = line[0:index]
                value = line[index+1:]

                if index >= 0:
                    if key == u'Продолжительность':
                        data['duration'] = int(value.replace(u'мин.', '').strip()) * 60 * 1000
                    elif key == u'Режиссер':
                        data['directors'] = value.strip().replace('.', '').split(',')
                    elif key == u'Жанр':
                        data['tags'] = value.strip().split(',')
                    else:
                        data[key] = value

            artists = info_node[1].text_content()
            artists = artists[len(u'В ролях:'):].split(',')

            data['artists'] = artists

            description_node = info_root[0].xpath('//div[@itemprop="description"]')

            if len(description_node) > 0:
                description = description_node[0].text_content()
            else:
                description = ''

            data['description'] = description

        return data

    def get_series(self, path, page=1):
        data = []

        page_path = self.get_page_path(path, page)

        document = self.fetch_document(self.URL + page_path)

        items = document.xpath('//div[@class="serial-list"]/div[@class="row"]')

        for item in items:
            link = item.xpath('div/a')[0]

            href = link.xpath('@href')[0]
            name = link.get("title")
            name = name[:len(name) - 18]
            thumb = self.URL + link.xpath('div/img/@src')[0]

            data.append({'path': href, 'thumb': thumb, 'name': name})

        pagination = self.extract_pagination_data(page_path, page=page)

        return {"movies": data, "pagination": pagination["pagination"]}

    def get_soundtracks(self, page=1):
        data = []

        page_path = self.get_page_path("/soundtrack/", page)

        document = self.fetch_document(self.URL + page_path)

        items = document.xpath('//div[@class="soundtrack-list"]/div[@class="row"]/div')

        for item in items:
            link1 = item.xpath('div/b/a')[0]
            link2 = item.xpath('a')[0]

            href = link1.xpath('@href')[0]
            name = link1.text_content()

            thumb = self.URL + link2.xpath('img/@src')[0]

            data.append({'path': href, 'thumb': thumb, 'name': name})

        pagination = self.extract_pagination_data(page_path, page=page)

        return {"movies": self.unique(data, "path"), "pagination": pagination["pagination"]}

    def get_albums(self, path, page=1):
        data = []

        page_path = self.get_page_path(path, page)

        document = self.fetch_document(self.URL + page_path)

        root = document.xpath('//div[@class="container"]/div[@class="row"]/*/div[@class="row"]')

        for index, item in enumerate(root):
            if index % 2:
                thumb = self.URL + item.find("div/a/img").get("src")
                name = item.find("div/a").get("title")

                composer = ''
                for li in item.xpath("div")[1].xpath("ul/li"):
                    if li.text_content().find('Композитор:'.decode("utf-8")) >= 0:
                        composer = li.text_content()[len('Композитор:'.decode("utf-8")):len(li.text_content())-1]

                data.append({
                    "thumb": thumb,
                    "name": name,
                    "composer": composer,
                    "tracks": []
                })

        items = document.xpath('//*[@id="soundtrack_modify_table"]')

        for index, item in enumerate(items):
            tracks = item.xpath('tbody/tr/td/div')

            for track in tracks:
                name = track.xpath('div[1]')[0].text_content()

                duration = track.xpath('../following-sibling::td')[0].text_content()
                bitrate = track.xpath('../following-sibling::td')[1].text_content()

                data[index]['tracks'].append({
                  "url": self.URL + track.get("data-file-url") + ".mp3",
                  "name": name,
                  "duration": self.convert_track_duration(duration),
                  "bitrate": int(bitrate)
                })

        return data

    def get_selections(self, page=1):
        data = []

        page_path = self.get_page_path("/selection/", page)

        document = self.fetch_document(self.URL + page_path)

        items = document.xpath('//div[@class="selection-list"]/div[@class="row"]/div')

        for item in items:
            link1 = item.xpath('div/b/a')[0]
            link2 = item.xpath('a')[0]

            href = link1.xpath('@href')[0]
            name = link1.text_content()
            thumb = self.URL + link2.xpath('img/@src')[0]

            data.append({'path': href, 'thumb': thumb, 'name': name})

        pagination = self.extract_pagination_data(page_path, page=page)

        return {"movies": data, "pagination": pagination["pagination"]}

    def get_selection_id(self, path):
        return path[2:len(path) - 1]

    def get_selection(self, path, page=1):
        data = []

        id = self.get_selection_id(path)
        page_path = self.get_page_path("/selection/" + id + '/', page)

        document = self.fetch_document(self.URL + page_path)

        items = document.xpath('//div[@class="selection-view"]/div')

        for item in items:
            link = item.xpath('div/a')[0]

            href = link.xpath('@href')[0]
            name = link.get("title")

            name = name[:len(name) - 18]

            thumb = self.URL + link.xpath('div/img/@src')[0]

            data.append({'path': href, 'thumb': thumb, 'name': name})

        pagination = self.extract_pagination_data(page_path, page=page)

        return {"movies": data, "pagination": pagination["pagination"]}

    def get_filters(self, mode='film'):
        data = []

        document = self.fetch_document(self.URL + "/" + mode + "/")

        current_group = None

        items = document.xpath('//div[@class="sidebar-nav"]/ul/li')

        for item in items:
            clazz = item.get("class")

            if clazz == 'nav-header':
                current_group = []

                name = item.text_content().replace(':', '')

                data.append({name : current_group})

            elif clazz == 'text-nowrap':
                link = item.xpath("a")[0]
                href = link.xpath('@href')[0]
                name = link.text_content()

                current_group.append({'path': href, 'name': name})

            elif clazz == 'dropdown':
                li_items = item.xpath("ul/li")

                del current_group[:]

                for li_item in li_items:
                    link = li_item.xpath("a")[0]
                    href = link.xpath('@href')[0]
                    name = link.text_content()

                    current_group.append({'path': href, 'name': name})

        return data

    def get_serie_info(self, path):
        serie_info = self.to_json(self.fetch_content(self.URL + path + "/playlist.txt"))['playlist']

        if serie_info and len(serie_info) > 0 and 'playlist' not in serie_info[0]:
            serie_info = [{
                "pltitle": "Сезон 1",
                "playlist": serie_info
            }]

        return serie_info

    def search(self, query, page=1):
        path = self.build_url("/search/", q=str(query), p=str(page))

        return self.get_movies(path=path, page=page)

    def get_metadata(self, url):
        data = []

        bandwidth = url[url.find("chunklist_b")+11:url.find(".m3u8")]

        source_url = self.get_base_url(url) + "/manifest.f4m"

        document = self.fetch_document(source_url)

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

    def get_source_url(self, url):
        content = self.fetch_content(url)

        document = self.to_document(content)

        script = document.xpath('//div[@class="row"]/div/script')[1].text_content()

        index1 = script.find("file:")
        index2 = script.find(".f4m")
        name = script[index1 + 6:index2]

        if name:
            name = name + ".f4m"
        else:
            name = None

        return name

    def get_urls(self, path=None, url=None):
        if not path and not url:
            print("Missing path or url")

            return []
        else:
            if path:
                source_url = self.get_source_url(self.URL + path)
            else:
                source_url = url

        if source_url:
            new_url = source_url.replace('.f4m', '.m3u8')

            urls = self.get_play_list_urls( new_url)

            return list(reversed(urls))
        else:
            return []

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

    def get_thumb(self, path):
        if path.find(self.URL) < 0:
            thumb = self.URL + path
        else:
            thumb = path

        return thumb

    def convert_track_duration(self, s):
        tokens = s.split(':')

        result = []

        for token in tokens:
            data = re.search('(\d+)', token)

            if data:
                result.append(data.group(0))

        minutes = int(result[0])
        seconds = int(result[1])

        return (minutes*60 + seconds) * 1000

    def unique(self, elements, key):
        new_elements = []

        for el in elements:
            values = []

            for el2 in new_elements:
                values.append(el2[key])

            if el[key] not in values:
                new_elements.append(el)

        return new_elements

    def get_episode_url(self, url, season, episode):
        if season:
            return '%s?season=%d&episode=%d' % (url, int(season), int(episode))

        return url
