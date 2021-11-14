# encoding:utf-8
import os.path

from flask import Blueprint
from flask_restful import Resource, marshal_with, fields, reqparse, marshal
from werkzeug.datastructures import FileStorage

from apps.user.model import User, Friend
from exits import api, db
from settings import Config

user_bp = Blueprint('user', __name__, url_prefix = '/api')
# 订制格式 其中的名字必须匹配 名字必须与数据库中的model中的一样
user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'password': fields.String,
    'udatetime': fields.String,
    'UID': fields.String
}
# 参数解析
# request.form.get() | request.args.get() | request.cookies.get()
parser = reqparse.RequestParser(bundle_errors = True)  # 产生一个解析对象 bundle_errors 同时报出错误 默认提醒一个
parser.add_argument('username', type = str, required = True, help = '必须输入用户名',
                    location = ['form'])  # ->required 表示必须填入用户信息，如果没有会返回help中的信息,location限制为post请求，表单提交
parser.add_argument('password', type = str, required = True, help = '必须输入密码', location = ['form'])
parser.add_argument('B_UID', type = str, location = ['form'])
parser.add_argument('hobby', action = 'append')  # 多个项以列表的形式进行添加 ['篮球','游戏','旅游']
parser.add_argument('icon', type = FileStorage, location = ['files'])  # 添加图片


class UserResource(Resource):  # ----->类视图
    @marshal_with(user_fields)  # 定义数据返回格式
    def get(self):
        users = User.query.all()
        return users

    @marshal_with(user_fields)
    def post(self):
        args = parser.parse_args()  # --->获取数据
        username = args.get('username')
        password = args.get('password')
        B_UID = args.get('B_UID')
        icon = args.get('icon')
        user = User()
        print(Config.UPLOAD_ICON_DIR)
        user.username = username
        user.password = password
        if icon:
            upload_path = os.path.join(Config.UPLOAD_ICON_DIR, icon.filename)
            icon.save(upload_path)
            user.icon = os.path.join('upload/icon', icon.filename)
        if B_UID:
            user.B_UID = B_UID
        db.session.add(user)
        db.session.commit()
        return user

    def delete(self):
        return {'msg': '---->delete'}

    def put(self):
        return {'msg': '---->put'}


class UerSimpleResource(Resource):
    @marshal_with(user_fields)  # --->User转成序列化对象
    def get(self, uid):
        user = User.query.get(uid)
        return user  # 将返回的用户进行序列化转化

    def put(self, uid):
        pass

    def delete(self, uid):
        pass


parser1 = reqparse.RequestParser()
parser1.add_argument('B_UID', type = str)
user_friend_fields = {
    'username': fields.String,
    'nums': fields.Integer,
    'friends': fields.List(fields.Nested(user_fields))
}


class UserFriendResource(Resource):
    # @marshal_with(user_friend_fields)
    def get(self):
        args1 = parser1.parse_args()  # --->获取数据
        id = args1.get('B_UID')
        print(id)
        if id is None:
            return {'msg': 'Please input an id'}
        friends = Friend.query.filter(Friend.uid == id).all()
        user = User.query.get(id)
        friend_list = []
        for friend in friends:
            u = User.query.get(friend.fid)
            friend_list.append(u)
        data = {
            'username': user.username,
            'nums': len(friends),
            # 下面两个方法都可以
            # 'friends': friend_list  # --->套用Marshal_with中的结构
            'friends': marshal(friend_list, user_fields)  # --->作为一个套叠的结构，将列表序列化
        }
        return data

    def delete(self):
        pass


api.add_resource(UserResource, '/user', endpoint = 'all_user')  # ->使用url_for('all_user')就可以返回/user
api.add_resource(UerSimpleResource, '/user/<int:uid>')  # --->路径传参
# api.add_resource(UserFriendResource, '/friend/<int:id>', endpoint = 'user_friend')
api.add_resource(UserFriendResource, '/friend', endpoint = 'user_friend')