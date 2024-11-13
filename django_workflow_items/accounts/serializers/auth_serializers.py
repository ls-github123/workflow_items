from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from ..models import CustomUser, Department
from .user_serializer import UserSerializer
from .department_serializer import DepartmentSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    """
    用户注册序列化器, 用于处理用户注册请求的数据验证和创建新用户。
    包含密码和确认密码的验证, 以及头像文件的验证。
    """
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'}, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'}, label="确认密码")
    department_id = serializers.PrimaryKeyRelatedField(
        queryset = Department.objects.all(),
        source = 'department',
        write_only = True,
        required = False,
        allow_null = True,
        help_text = '所属部门ID'
    )

    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'gender', 'password', 'password_confirm',
            'department_id', 'position', 'work_status', 'current_destination',
            'date_of_joining', 'phone_number', 'emergency_contact', 'avatar'
        ]
    
    def validate_email(self, value):
        """
        验证邮箱是否唯一。
        """
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("该邮箱已被注册!")
        return value
    
    def validate_avatar(self, value):
        """
        验证上传的头像文件。
        - 限制文件大小为5MB。
        - 确保文件类型为图片。
        """
        if value:
            if value.size > 5 * 1024 * 1024: # 限制为5MB
                raise serializers.ValidationError("头像文件大小不能超过5MB!")
            if not value.content_type.startswith('image/'):
                raise serializers.ValidationError("只能上传图片文件!")
        return value
            
    def validate(self, attrs):
        """
        验证密码和确认密码是否一致。
        """
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "两次密码输入不一致!"})
        return attrs
    
    def create(self, validated_data):
        """
        创建用户实例。
        - 移除'password_confirm'字段,。
        - 使用自定义用户管理器创建用户，确保密码被正确哈希。
        """
        validated_data.pop('password_confirm')
        user = CustomUser.objects.create_user(**validated_data)
        return user

    
class LoginSerializer(TokenObtainPairSerializer):
    """
    自定义登录序列化器，继承自 TokenObtainPairSerializer, 
    用于验证用户凭据并生成 JWT 令牌, 添加额外的用户信息到响应中。
    """
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    def validate(self, attrs):
        """
        验证用户凭据是否有效。
        - 使用 Django 的 authenticate 方法验证用户名和密码。
        - 如果验证通过，生成 access 和 refresh 令牌。
        - 添加额外的用户信息到响应数据中。
        """
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("用户已被禁用!")
                attrs['user'] = user
                data = super().validate(attrs) # 生成令牌
                data.update({'user': UserSerializer(user, context=self.context).data})
                return data
            else:
                raise serializers.ValidationError("提供的凭据无效!") 
        else:
            raise serializers.ValidationError("必须包含 'username'和'password'。")
        
    @classmethod
    def get_token(cls, user):
        """
        重写 get_token 方法, 向令牌中添加自定义的声明。
        """
        token = super().get_token(user)
        
        # 添加自定义声明
        token['email'] = user.email
        token['username'] = user.username
        token['department'] = user.department.name if user.department else None
        token['position'] = user.position
        token['work_status'] = user.work_status
        
        return token