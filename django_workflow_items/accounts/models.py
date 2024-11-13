from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
import uuid

class CustomUserManager(BaseUserManager):
    """
    自定义用户管理器, 用于创建普通用户和超级用户。
    """
    def create_user(self, username, email, gender, password=None, **extra_fields):
        """
        创建并保存一个普通用户。
        
        参数:
            username (str): 用户名，必须唯一。
            email (str): 用户电子邮件，必须唯一。
            gender (str): 用户性别，选项为 'M', 'F', 'O'。
            password (str): 用户密码，默认为 None。
            extra_fields (dict): 其他可选字段。
        
        返回: 
            CustomUser --> 创建的普通用户实例。
        """
        if not username:
            raise ValueError('必须设置用户名!')
        if not email:
            raise ValueError('必须设置邮箱!')
        if not gender:
            raise ValueError('必须设置性别!')
        
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, gender=gender, **extra_fields)
        user.set_password(password) # 设置密码，使用加密存储
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, gender, password=None, **extra_fields):
        """
        创建并保存一个超级用户。
        
        参数:
            username (str): 用户名，必须唯一。
            email (str): 用户电子邮件，必须唯一。
            gender (str): 用户性别，选项为 'M', 'F', 'O'。
            password (str): 用户密码，默认为 None。
            extra_fields (dict): 其他可选字段。
            
        返回:
            CustomUser --> 创建的超级用户实例。
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        # 验证超级用户标记
        if extra_fields.get('is_staff') is not True:
            raise ValueError('超级用户 is_staff 字段必须为True!')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('超级用户 is_superuser 字段必须为True!')
        
        return self.create_user(username, email, gender, password, **extra_fields)

class Department(models.Model):
    """
    部门模型, 表示公司或组织中的部门。
    """
    name = models.CharField('部门名称', max_length=50, unique=True, null=False)
    description = models.TextField('部门描述', blank=True, null=True)
    
    class Meta:
        db_table = 'department_info'
        verbose_name = '部门信息'
        verbose_name_plural = '部门信息'
        ordering = ['name'] # 默认按名称排序
    
    def __str__(self):
        return self.name
    

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    自定义用户模型, 使用UUID作为主键, 扩展基本用户信息。
    """
    
    GENDER_CHOICES = [
        ('M', '男'),
        ('F', '女'),
        ('U', '未知'),
    ]
    
    WORK_STATUS_CHOICES = [
        ('active', '在职'),
        ('leave', '休假'),
        ('business_trip', '出差'),
        ('inactive', '离职'),
    ]
    
    # UUID4 -- 完全基于随机数生成
    id = models.UUIDField(
        primary_key = True,
        default = uuid.uuid4,
        editable=False, # 防止在Django Admin或表单中编辑
        verbose_name='用户ID'
    )
    username = models.CharField('用户名', max_length=150, unique=True, null=False)
    email = models.EmailField('用户邮箱', unique=True, null=False)
    phone_number = models.CharField('手机号', max_length=15, blank=True, null=True)
    gender = models.CharField('性别', max_length=2, choices=GENDER_CHOICES, null=False)
    is_staff = models.BooleanField('是否为管理员', default=False)
    is_active = models.BooleanField('是否活跃', default=True)
    date_joined = models.DateTimeField('添加时间', auto_now_add=True)
    department = models.CharField('所属部门', max_length=50, blank=True, null=True)
    position = models.CharField('负责职位', max_length=50, blank=True, null=True)
    work_status = models.CharField('工作状态', max_length=20, choices=WORK_STATUS_CHOICES, null=False, default='active')
    current_destination = models.CharField('当前去向', max_length=255, blank=True, null=True)
    date_of_joining = models.DateField('入职日期', blank=True, null=True)
    date_of_leaving = models.DateField('离职日期', blank=True, null=True)
    emergency_contact = models.CharField('紧急联系人信息', max_length=100, blank=True, null=True)
    avatar = models.ImageField('员工头像', upload_to='avatars/', null=True, blank=True)
    
    # 指定使用自定义用户管理器
    objects = CustomUserManager()
    
    # 设置用户名字段和必填字段
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'gender']
    
    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
        ordering = ['-date_joined']
    
    def __str__(self):
        return self.username