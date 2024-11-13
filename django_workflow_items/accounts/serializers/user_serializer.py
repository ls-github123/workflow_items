from rest_framework import serializers
from ..models import CustomUser, Department
from .department_serializer import DepartmentSerializer

class UserSerializer(serializers.ModelSerializer):
    """
    用户序列化器, 用于将用户模型转换为JSON格式。
    """
    department = DepartmentSerializer(read_only=True)
    department_id = serializers.PrimaryKeyRelatedField(
        queryset = Department.objects.all(),
        source = 'department',
        write_only = True,
        required = False,
        allow_null = True,
        help_text = '所属部门ID'
    )
    avatar_url = serializers.SerializerMethodField()
    
    class Meta:
        model = CustomUser
        fields = [
            # 定义需要序列化的字段
            # id -- 雪花ID
            'id', 'username', 'email', 'date_joined', 
            'department', 'department_id', 'position', 'work_status', 'current_destination',
            'date_of_joining', 'date_of_leaving', 'phone_number',
            'emergency_contact', 'avatar', 'avatar_url',
        ]
        
        # 指定只读字段, 防止通过前端修改
        read_only_fields = ['id', 'date_joined', 'date_of_leaving', 'avatar_url']
        
    def get_avatar_url(self, obj):
        """
        获取用户头像的完整 URL。
        如果用户上传了头像，则返回其 URL, 否则返回 None。
        """
        request = self.context.get('request')
        if obj.avatar and hasattr(obj.avatar, 'url'):
            return request.build_absolute_uri(obj.avatar.url) # Azure Blob Storage 已设置 MEDIA_URL
        return None
    
    def update(self, instance, validated_data):
        # 处理部门关联
        department = validated_data.app('department', None)
        if department is not None:
            instance.department = department
        return super().update(instance, validated_data)