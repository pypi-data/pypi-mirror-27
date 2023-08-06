import coreapi
import coreschema
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_api_actions.views import ActionReadMixin


class UsersAPIView(APIView):
    """
    获得用户列表

    返回值：用户列表 `['a', 'b', ...]`

    """

    def get(self, request):
        return Response(['a', 'b'])


class InvitationAPIView(APIView):
    """
    获得用户列表

    返回值：用户列表 `['a', 'b', ...]`

    """

    def get(self, request):
        return Response(['i', 'j'])


class UsersActionReadAPIView(ActionReadMixin, APIView):
    """
    获得用户列表, 用了`ActionReadMixin`后这是一个用 Read

    返回值：用户列表 `['a', 'b', ...]`

    """

    def get(self, request):
        return Response(['a', 'b'])


class UsersExtraFieldsAPIView(APIView):
    """
    获得用户列表, 带user_id/user_name会过滤

    返回值：
        - 带user_id: `['a']`
        - 不带user_id: `['a','b']`
    """

    extra_fields = [
        coreapi.Field(name='user_father', location='query', required=True,
                      schema=coreschema.String(description='用户的爹')),
        coreapi.Field(name='user_id', location='query', required=False,
                      schema=coreschema.Integer(description='用户id')),
        coreapi.Field(name='obj', location='query', required=False,
                      schema=coreschema.Object(description='object param')),
        coreapi.Field(name='arr', location='query', required=False,
                      schema=coreschema.Array(description='array param')),
        coreapi.Field(name='boo', location='query', required=False,
                      schema=coreschema.Boolean(description='boolean param')),
        coreapi.Field(name='enu', location='query', required=False,
                      schema=coreschema.Enum([1, 2, 3], description='enum param')),
        # 下面这些类型在doc里面会有问题，在api.js里正常
        # coreapi.Field(name='nul', location='query', required=False,
        #               schema=coreschema.Null(description='Null param')),
        # coreapi.Field(name='any', location='query', required=False,
        #               schema=coreschema.Anything(description='anything param')),
        # coreapi.Field(name='uni', location='query', required=False,
        #               schema=coreschema.Union([1, 2], description='union param')),
        # coreapi.Field(name='no', location='query', required=False,
        #               schema=coreschema.Not(1, description='not param')),
    ]

    def get(self, request):
        user_id = request.GET.get('user_id', '')
        if user_id:
            return Response(['a'])
        else:
            return Response(['a', 'b'])
