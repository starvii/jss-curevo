#!/usr/bin/env python
# -*- coding: utf-8 -*-

from collections import OrderedDict
from sqlalchemy import or_
from model.entity import NaturalClass
from method.serial import to_dict_with_label, to_json, merge_from_dict
from method.idgen import object_id
from method.restful import METHOD_OVERRIDE, JSON_SUCCESS, JSON_FAILED, parse_body
from method.date import now
import constants
from handler import BaseHandler
from method.logger import default_logger as log


class NaturalClassAPI(BaseHandler):

    def get(self, *args, **kwargs):
        """
        如果 url param 带有id则查找单个实体
        如果不带id则返回列表
        :param args:
        :param kwargs:
        :return:
        """
        if len(args) == 1 and len(args[0]) > 0:
            tid = args[0]
            t = self.query_entity_by_id(tid)
            if t:
                self.finish(t)
            else:
                self.set_status(404)
                self.finish()
        else:
            page = self.get_argument('page', '1')
            page = int(page) if str.isnumeric(page) else 1
            size = self.get_argument('size', str(constants.DEFAULT_PAGE_SIZE))
            size = int(size) if str.isnumeric(size) else constants.DEFAULT_PAGE_SIZE
            size = size if size in constants.PAGE_SIZE else constants.DEFAULT_PAGE_SIZE
            keyword = self.get_argument('keyword', '')
            r = self.query_entities_by_keyword(page, size, keyword)
            self.finish(r)

    def post(self, *args, **kwargs):
        tid = None
        if len(args) == 1 and len(args[0]) > 0:
            tid = args[0]
        if METHOD_OVERRIDE not in self.request.headers:
            self.do_post(parse_body(self.request.body))
        else:
            method = self.request.headers[METHOD_OVERRIDE]
            if 'POST' == method:
                self.do_post(parse_body(self.request.body))
            elif 'PUT' == method:
                self.do_put(tid, parse_body(self.request.body))
            elif 'DELETE' == method:
                self.do_delete(tid)
            else:
                self.finish(JSON_FAILED)

    def do_post(self, dict_data):
        try:
            self.insert_entity(dict_data)
            self.finish(JSON_SUCCESS)
        except Exception as e:
            log.error(e)
            self.finish(JSON_FAILED)

    def do_put(self, tid, dict_data):
        if tid != dict_data['Id']:
            self.finish(JSON_FAILED)
        else:
            try:
                self.update_entity(dict_data)
                self.finish(JSON_SUCCESS)
            except Exception as e:
                log.error(e)
                self.finish(JSON_FAILED)

    def do_delete(self, tid):
        try:
            if self.delete_entity(tid):
                self.finish(JSON_SUCCESS)
            else:
                self.finish(JSON_FAILED)
        except Exception as e:
            log.error(e)
            self.finish(JSON_FAILED)

    def query_entity_by_id(self, tid):
        t = self.db.query(NaturalClass).filter_by(Id=tid).first()
        if t:
            d = to_dict_with_label(t, 'detail')
            j = to_json(d)
            return j

    def query_entities_by_keyword(self, page, size, keyword):
        k = keyword.strip()
        f = NaturalClass.DeleteAt.is_(None)
        if len(k) > 0:
            k = ''.join(('%', k, '%'))
            o = or_(NaturalClass.Grade.like(k), NaturalClass.BelongToCollege.like(k), NaturalClass.Dept.like(k),
                    NaturalClass.Name.like(k), NaturalClass.Comment.like(k), NaturalClass.StudentCount == k)
            c = self.db.query(NaturalClass.DbId).filter(f).filter(o).count()
            l = self.db.query(NaturalClass).filter(f).filter(o).offset((page - 1) * size).limit(size).all()
        else:
            c = self.db.query(NaturalClass.DbId).filter(f).count()
            l = self.db.query(NaturalClass).filter(f).offset((page - 1) * size).limit(size).all()
        l = [to_dict_with_label(e, 'list') for e in l]
        params = OrderedDict(page=page, size=size, keyword=keyword)
        r = dict(count=c, data=l, params=params)
        j = to_json(r)
        return j

    def insert_entity(self, entity_dict):
        t = NaturalClass()
        t.Id = object_id()
        merge_from_dict(t, entity_dict)
        try:
            self.db.add(t)
            self.db.commit()
        except:
            raise

    def update_entity(self, entity_dict):
        t = NaturalClass()
        merge_from_dict(t, entity_dict)
        try:
            # 由于不是使用 id 作为主键，融合时还需要再查询一次 db_id
            eid = entity_dict['Id']
            db_id = self.db.query(NaturalClass.DbId).filter(NaturalClass.Id == eid).scalar()
            t.DbId = db_id
            self.db.merge(t)
            self.db.commit()
        except:
            raise

    def delete_entity(self, eid):
        try:
            result = self.db.execute('UPDATE natural_class SET delete_at = :now WHERE id = :id', {'now': now(), 'id': eid})
            self.db.commit()
            if 1 == result.rowcount:
                return True
            else:
                return False
        except:
            raise


url = [(r'/api/class/natural/?(.*)', NaturalClassAPI)]
