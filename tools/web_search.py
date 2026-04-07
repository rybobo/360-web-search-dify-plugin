  from dify_plugin import Tool
  from dify_plugin.entities.tool import ToolInvokeMessage
  from typing import Any, Generator
  import requests
  import uuid

  class WebSearchTool(Tool):
      def _invoke(self, tool_parameters: dict[str, Any]) -> Generator[ToolInvokeMessage]:
          """执行搜索"""

          # 获取参数
          api_key = self.runtime.credentials.get("api_key")
          query = tool_parameters.get("query")
          count = tool_parameters.get("count", 5)

          # 参数验证
          if not query:
              yield self.create_text_message("搜索关键词不能为空")
              return

          # 构建请求参数
          params = {
              "q": query,
              "ref_prom": "aiso-pro",  # 默认使用进阶版
              "sid": str(uuid.uuid4()),
              "count": min(50, max(1, int(count)))
          }

          headers = {
              "Authorization": f"Bearer {api_key}"
          }

          try:
              # 调用360搜索API
              response = requests.get(
                  "https://api.360.cn/v2/mwebsearch",
                  headers=headers,
                  params=params,
                  timeout=10
              )

              # 处理响应
              if response.status_code == 401:
                  yield self.create_text_message("API密钥无效，请检查配置")
                  return

              if response.status_code != 200:
                  yield self.create_text_message(f"搜索失败: {response.status_code}")
                  return

              data = response.json()

              # 检查结果
              if not data.get("data"):
                  yield self.create_text_message("未找到相关结果")
                  return

              # 格式化输出
              results = []
              for i, item in enumerate(data["data"], 1):
                  title = item.get("title", "")
                  url = item.get("url", "")
                  summary = item.get("summary_ai") or item.get("summary", "")
                  page_time = item.get("page_time", "")

                  # 输出每条结果
                  yield self.create_text_message(
                      f"\n{i}. {title}\n"
                      f"   {summary}\n"
                      f"   🔗 {url}\n"
                      f"   ⏰ {page_time}\n"
                  )

                  results.append({
                      "title": title,
                      "url": url,
                      "summary": summary,
                      "page_time": page_time
                  })

              # 返回JSON格式供AI处理
              yield self.create_json_message({
                  "query": query,
                  "total": len(results),
                  "results": results
              })

          except requests.RequestException as e:
              yield self.create_text_message(f"网络请求失败: {str(e)}")
          except Exception as e:
              yield self.create_text_message(f"搜索出错: {str(e)}")
