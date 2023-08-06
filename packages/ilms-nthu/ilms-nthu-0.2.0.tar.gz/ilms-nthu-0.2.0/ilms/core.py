import os

from ilms import parser
from ilms import exception
from ilms.route import route
from ilms.request import RequestProxyer
from ilms.utils import (
    unzip_all, check_is_download, stream_download,
    json_dump, json_load, safe_str)

reqs = RequestProxyer()


class User:

    def __init__(self, user, pwd):
        self.user = user
        self.pwd = pwd
        self.email = None

    def check_login(self):
        try:
            resp = reqs.get(route.profile)
            parser.parse_profile(resp.text)
            return True
        except exception.PermissionDenied:
            return False

    def login(self):
        if self.check_login():
            return True
        resp = reqs.post(
                route.login_submit,
                data={'account': self.user, 'password': self.pwd})
        json = resp.json()
        if json['ret']['status'] == 'false':
            raise exception.LoginError
        self.email = json['ret']['email']
        reqs.save_session()
        return json


class Item():

    def __init__(self, raw, callee):
        self.raw = raw
        self.callee = callee
        self.uid = raw['id']
        self.insert_attrs(raw)

    def insert_attrs(self, attrs):
        for key, val in attrs.items():
            setattr(self, key, val)

    def download(self):
        for target in self.detail:
            download(target['id'])


class ItemContainer():

    def __init__(self, parse_result, instance, callee):
        self.items = [
            instance(item, callee=callee)
            for item in parse_result.result
        ]

    def __getitem__(self, x):
        return self.items[x]

    def __iter__(self):
        return self.items.__iter__()

    def get(self, x):
        return self.items[x]

    def find(self, **query_kws):
        for item in self.items:
            for query_k, query_v in query_kws.items():
                if not query_v:
                    break
                targ = getattr(item, query_k)
                if targ and isinstance(targ, str) and query_v not in targ:
                    break
                if targ and isinstance(targ, dict):
                    for targ_k, targ_v in targ.items():
                        if query_v in targ_v:
                            print(query_v, targ_v)
                            return item
                    else:
                        break
            else:
                return item


class Handin(Item):

    @property
    def detail(self):
        if hasattr(self, '_detail'):
            return self._detail
        resp = reqs.get(
            route.course(self.callee.callee.id).document(self.uid))
        self._detail = parser.parse_homework_handin_detail(resp.text).result
        return self._detail

    def download(self, root_folder):
        folder_name = os.path.join(root_folder, '%s-%s' % (self.account_id, self.authour))
        if check_is_download(folder_name, ['*.zip', '*.rar']):
            return
        for target in self.detail:
            download(target['id'], folder=folder_name)
        unzip_all(folder_name)

    def set_score(self, score):
        score_id = self.score.get('score_id')
        assert int(score_id)

        params = {'score': score, 'id': score_id}
        r = reqs.post(route.score, params=params)

        assert r.ok
        return r

    def __str__(self):
        return safe_str('<Homework Handin: %s-%s>' % (self.account_id, self.authour))


class Homework(Item):

    @property
    def detail(self):
        if hasattr(self, '_detail'):
            return self._detail
        resp = reqs.get(
            route.course(self.callee.id).homework(self.uid))
        self._detail = parser.parse_homework_detail(resp.text).result
        return self._detail

    @property
    def handin_list(self):
        if hasattr(self, '_handin_list'):
            return self._handin_list
        resp = reqs.get(
            route.course(self.callee.id).homework_handin_list(self.uid))
        parser_func = {
            '分組作業': lambda x: parser.parse_homework_handin_list(x, is_group=True),
            '個人作業': parser.parse_homework_handin_list,
        }[self.detail['extra']['屬性']]
        self._handin_list = ItemContainer(
            parser_func(resp.text),
            instance=Handin,
            callee=self
        )
        return self._handin_list

    def score_handins(self, score_map):
        for handin in self.handin_list:
            try:
                assert handin.account_id in score_map

                score = score_map[handin.account_id]
                result = handin.set_score(score)

                print(handin, result.json()['ret']['msg'])
            except Exception as e:
                print('Catch exception', e, 'while scoring', handin)

    def download_handins(self, root_folder):
        meta_path = os.path.join(root_folder, 'meta.json')
        done_lut = json_load(meta_path)
        try:
            for handin in self.handin_list:
                metadata = done_lut.get(handin.id)
                if (metadata
                   and metadata.get('last_update')
                   and handin.date_string >= metadata['last_update']):
                    continue
                print(handin)
                handin.download(root_folder=root_folder)
                done_lut[handin.id] = {'last_update': handin.date_string}
        except Exception as e:
            print('Catch exception', e, 'while downloading')
        finally:
            json_dump(done_lut, meta_path)

    def __str__(self):
        return '<Homework: %s>' % (self.title)


class Material(Item):

    @property
    def detail(self):
        if hasattr(self, '_detail'):
            return self._detail
        resp = reqs.get(
            route.course(self.callee.id).document(self.uid))
        self._detail = parser.parse_material_detail(resp.text).result
        return self._detail

    def download(self, root_folder):
        folder_name = os.path.join(root_folder, '%s' % self.標題)
        if check_is_download(folder_name, ['*.pdf', '*.ppt', '*.pptx']):
            return
        for target in self.detail:
            download(target['id'], folder=folder_name)

    def __str__(self):
        return '<Material: %s, %s hits>' % (self.標題, self.人氣)


class Course(Item):

    def get_homeworks(self):
        resp = reqs.get(route.course(self.uid).homework())
        self.homeworks = ItemContainer(
            parser.parse_homework_list(resp.text),
            instance=Homework,
            callee=self
        )
        return self.homeworks

    def get_materials(self, download=False):
        resp = reqs.get(route.course(self.uid).document())
        self.materials = ItemContainer(
            parser.parse_material_list(resp.text),
            instance=Material,
            callee=self
        )
        return self.materials

    def get_forum_list(self, page=1):
        resp = reqs.get(
            route.course(self.uid).forum() + '&page=%d' % page)
        return parser.parse_forum_list(resp.text)

    def get_group_list(self):
        resp = reqs.get(
            route.course(self.uid).forum() + '&page=%d' % page)
        return parser.parse_group_list(resp.text)

    def __str__(self):
        return '<Course: %s %s>' % (self.course_id, self.name.get('zh'))


class Core():

    def __init__(self, user):
        self.profile = None
        self.courses = None

    def get_profile(self):
        resp = reqs.get(route.profile)
        self.profile = parser.parse_profile(resp.text)
        return self.profile

    def get_courses(self):
        resp = reqs.get(route.home)
        self.courses = ItemContainer(
            parser.parse_course_list(resp.text),
            instance=Course,
            callee=self
        )
        return self.courses

    def get_post_detail(self, post_id):
        resp = reqs.post(route.post, data={'id': post_id})
        return parser.parse_post_detail(resp.json())


def download(attach_id, folder='download'):
    resp = reqs.get(route.attach.format(attach_id=attach_id), stream=True)
    stream_download(resp, folder)
