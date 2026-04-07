  from dify_plugin import ToolProvider
  from dify_plugin.errors.tool import ToolProviderCredentialValidationError
  from tools.web_search import WebSearchTool
  import requests

  class Qihoo360Provider(ToolProvider):
      def _validate_credentials(self, credentials: dict) -> None:
          """验证API密钥"""
          try:
              api_key = credentials.get("api_key")
              # 调用一次API验证密钥
              response = requests.get(
                  "https://api.360.cn/v2/mwebsearch",
                  headers={"Authorization": f"Bearer {api_key}"},
                  params={"q": "test", "ref_prom": "aiso-pro", "sid": "test"},
                  timeout=5
              )
              if response.status_code == 401:
                  raise ToolProviderCredentialValidationError("API密钥无效")
          except Exception as e:
              raise ToolProviderCredentialValidationError(f"验证失败: {str(e)}")
