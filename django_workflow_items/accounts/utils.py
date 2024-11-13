from snowflake import SnowflakeGenerator
from django.conf import settings


class CustomSnowflakeGenerator:
    def __init__(self, datacenter_id, worker_id):
        # 根据库实际支持的参数名进行修改
        self.generator = SnowflakeGenerator(worker_id=worker_id, machine_id=datacenter_id)

    def generate_id(self):
        return self.generator.generate()

# 使用自定义生成器
snowflake_generator = CustomSnowflakeGenerator(
    datacenter_id=settings.SNOWFLAKE_DATACENTER_ID,
    worker_id=settings.SNOWFLAKE_WORKER_ID
)