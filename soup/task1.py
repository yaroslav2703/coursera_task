from bs4 import BeautifulSoup
import unittest


def parse(path_to_file):
    with open('./' + path_to_file, 'r', encoding='utf-8') as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'lxml')
        body = soup.find('div', id="bodyContent")
        return [task1(body), task2(body), task3(body), task4(body)]


def task1(body):
    imgs = [img for img in body.find_all('img') if
            img.has_attr('width') and int(img.attrs['width']) >= 200]
    return len(imgs)


def task2(body):
    headers = [header for header in body.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']) if
               header.text[0] == 'E' or header.text[0] == 'T' or header.text[0] == 'C']
    return len(headers)


def task3(body):
    aparents = [0]
    list_a = body.find_all('a')
    h = list_a[0].parent
    i = 0
    for a in list_a:
        if a.parent is h and (i == 0 or a.previousSibling.name == 'a' or a.previousSibling.previousSibling.name == 'a'):
            aparents[i] += 1
            h = a.parent
        else:
            aparents.append(1)
            i += 1
            h = a.parent

    return max(aparents)


def task4(body):
    lists = [list_ for list_ in body.find_all(['ol', 'ul']) if
             list_.find_parent(['ol', 'ul']) is None]
    return len(lists)


class TestParse(unittest.TestCase):
    def test_parse(self):
        test_cases = (
            ('wiki/Stone_Age', [13, 10, 12, 40]),
            ('wiki/Brain', [19, 5, 25, 11]),
            ('wiki/Artificial_intelligence', [8, 19, 13, 198]),
            ('wiki/Python_(programming_language)', [2, 5, 17, 41]),
            ('wiki/Spectrogram', [1, 2, 4, 7]),
            ('wiki/Forward_chaining', [0, 3, 5, 7]),)

        for path, expected in test_cases:
            with self.subTest(path=path, expected=expected):
                self.assertEqual(parse(path), expected)


if __name__ == '__main__':
    unittest.main()
