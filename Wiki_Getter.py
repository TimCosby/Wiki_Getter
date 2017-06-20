from urllib.request import urlopen
import json


def get_json(search):
    if 'wikipedia' in search[:21].lower():  # Search by url
        search += ' '
        start = search[20:].find('wiki/') + 5
        end = search[20:].find('/', start)

        return json.loads(urlopen('https://en.wikipedia.org/w/api.php?action=query&titles=' + search[start + 20:end] + '&prop=revisions&rvprop=content&format=json').readline().decode('utf-8'))

    else:  # Search by keyword
        return json.loads(urlopen('https://en.wikipedia.org/w/api.php?action=query&titles=' + search + '&prop=revisions&rvprop=content&format=json').readline().decode('utf-8'))


def get_art_url(json_page, title):
    query = json_page['query']['pages'][list(json_page['query']['pages'].keys())[0]]['revisions'][0]['*']

    start = query.find(' image ')
    start = query.find(' = ', start + 6) + 3
    end = query.find('\n', start)

    return 'https://en.wikipedia.org/wiki/' + title + '#/media/File:' + query[start:end]


def cut_comments(query):
    while True:
        start = query.find('<ref>')

        if start == -1:
            break

        else:
            query = query[:start + 6] + cut_comments(query[start + 5:])

            end = query.find('</ref>', start)

            query = query[:start] + query[end + 6:]

    while True:
        start = query.find('<')

        if start == -1:
            break

        else:
            query = query[:start] + cut_comments(query[start + 1:])

            end = query.find('>', start)

            query = query[:start] + query[end + 1:]

    while True:
        start = query.find('{')

        if start == -1:
            break

        else:
            query = query[:start] + cut_comments(query[start + 1:])

            end = query.find('}', start)

            query = query[:start] + query[end + 3:]

    return query


def get_description(json_page):
    query = json_page['query']['pages'][list(json_page['query']['pages'].keys())[0]]['revisions'][0]['*']
    start = query.find('\n\n') + 4

    end = query.find('\n', start)

    query = query[start:end].replace('\'', '')

    query = cut_comments(query)
    return query


def get_name(json_page):
    query = json_page['query']['pages'][list(json_page['query']['pages'].keys())[0]]['revisions'][0]['*']

    start = query.find('\'name ')
    start = query.find(' = ', start + 6) + 3

    end = query.find('\n', start)

    return query[start:end]


def get_title(json_page):
    """
    Gets the title of the wikipedia page

    :param json_page:
    :return: str
    """

    return json_page['query']['pages'][list(json_page['query']['pages'].keys())[0]]['title']


def get_info(search):
    json_page = get_json(search)

    print(json_page)

    if list(json_page['query']['pages'].keys()) == ['-1']:
        return [None, None, None]

    else:
        #info_grab = json_page['query']['pages'][list(json_page['query']['pages'].keys())[0]]['revisions'][0]['*'].split('\n| ')

        title = get_title(json_page)

        name = get_name(json_page)

        art_url = get_art_url(json_page, title)

        description = get_description(json_page)

        return [name, art_url, description]

if __name__ == '__main__':
    print(get_info(input('Enter your search or url:\n').strip()))
