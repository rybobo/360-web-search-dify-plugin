{\rtf1\ansi\ansicpg936\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fnil\fcharset0 Menlo-Regular;}
{\colortbl;\red255\green255\blue255;\red0\green0\blue0;\red64\green11\blue217;\red171\green223\blue228;
\red159\green160\blue28;\red46\green174\blue187;\red180\green36\blue25;\red47\green180\blue29;}
{\*\expandedcolortbl;;\csgray\c0;\cssrgb\c32309\c18666\c88229;\csgenericrgb\c67157\c87278\c89373;
\cssrgb\c68469\c68012\c14211;\cssrgb\c20199\c73241\c78251;\cssrgb\c76411\c21697\c12527;\cssrgb\c20241\c73898\c14950;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx560\tx1120\tx1680\tx2240\tx2800\tx3360\tx3920\tx4480\tx5040\tx5600\tx6160\tx6720\pardirnatural\partightenfactor0

\f0\fs22 \cf2 \CocoaLigature0   \cf3 from\cf2  dify_plugin \cf3 import\cf2  Tool\
  \cf3 from\cf2  dify_plugin.entities.tool \cf3 import\cf2  ToolInvokeMessage\
  \cf3 from\cf2  typing \cf3 import\cf2  \cf4 Any\cf2 , Generator\
  \cf3 import\cf2  requests\
  \cf3 import\cf2  uuid\
\
  \cf3 class\cf2  \cf3 WebSearchTool(Tool):\cf2 \
      \cf3 def\cf5  _invoke(self,\cf2  \cf5 tool_parameters:\cf2  \cf6 dict\cf5 [\cf6 str\cf5 ,\cf2  \cf4 Any\cf5 ])\cf2  \cf5 ->\cf2  \cf5 Generator[ToolInvokeMessage]:\cf2 \
          \cf7 """\uc0\u25191 \u34892 \u25628 \u32034 """\cf2 \
\
          \cf8 #\cf2  \cf8 \uc0\u33719 \u21462 \u21442 \u25968 \cf2 \
          api_key = self.runtime.credentials.get(\cf7 "api_key"\cf2 )\
          query = tool_parameters.get(\cf7 "query"\cf2 )\
          count = tool_parameters.get(\cf7 "count"\cf2 , \cf8 5\cf2 )\
\
          \cf8 #\cf2  \cf8 \uc0\u21442 \u25968 \u39564 \u35777 \cf2 \
          \cf3 if\cf2  \cf3 not\cf2  query:\
              \cf3 yield\cf2  self.create_text_message(\cf7 "\uc0\u25628 \u32034 \u20851 \u38190 \u35789 \u19981 \u33021 \u20026 \u31354 "\cf2 )\
              \cf3 return\cf2 \
\
          \cf8 #\cf2  \cf8 \uc0\u26500 \u24314 \u35831 \u27714 \u21442 \u25968 \cf2 \
          params = \{\
              \cf7 "q"\cf2 : query,\
              \cf7 "ref_prom"\cf2 : \cf7 "aiso-pro"\cf2 ,  \cf8 #\cf2  \cf8 \uc0\u40664 \u35748 \u20351 \u29992 \u36827 \u38454 \u29256 \cf2 \
              \cf7 "sid"\cf2 : \cf6 str\cf2 (uuid.uuid4()),\
              \cf7 "count"\cf2 : \cf6 min\cf2 (\cf8 50\cf2 , \cf6 max\cf2 (\cf8 1\cf2 , \cf6 int\cf2 (count)))\
          \}\
\
          headers = \{\
              \cf7 "Authorization"\cf2 : \cf7 f"Bearer\cf2  \cf7 \{api_key\}"\cf2 \
          \}\
\
          \cf3 try\cf2 :\
              \cf8 #\cf2  \cf8 \uc0\u35843 \u29992 360\u25628 \u32034 API\cf2 \
              response = requests.get(\
                  \cf7 "https://api.360.cn/v2/mwebsearch"\cf2 ,\
                  headers=headers,\
                  params=params,\
                  timeout=\cf8 10\cf2 \
              )\
\
              \cf8 #\cf2  \cf8 \uc0\u22788 \u29702 \u21709 \u24212 \cf2 \
              \cf3 if\cf2  response.status_code == \cf8 401\cf2 :\
                  \cf3 yield\cf2  self.create_text_message(\cf7 "API\uc0\u23494 \u38053 \u26080 \u25928 \u65292 \u35831 \u26816 \u26597 \u37197 \u32622 "\cf2 )\
                  \cf3 return\cf2 \
\
              \cf3 if\cf2  response.status_code != \cf8 200\cf2 :\
                  \cf3 yield\cf2  self.create_text_message(\cf7 f"\uc0\u25628 \u32034 \u22833 \u36133 :\cf2  \cf7 \{response.status_code\}"\cf2 )\
                  \cf3 return\cf2 \
\
              data = response.json()\
\
              \cf8 #\cf2  \cf8 \uc0\u26816 \u26597 \u32467 \u26524 \cf2 \
              \cf3 if\cf2  \cf3 not\cf2  data.get(\cf7 "data"\cf2 ):\
                  \cf3 yield\cf2  self.create_text_message(\cf7 "\uc0\u26410 \u25214 \u21040 \u30456 \u20851 \u32467 \u26524 "\cf2 )\
                  \cf3 return\cf2 \
\
              \cf8 #\cf2  \cf8 \uc0\u26684 \u24335 \u21270 \u36755 \u20986 \cf2 \
              results = []\
              \cf3 for\cf2  i, item \cf3 in\cf2  \cf6 enumerate\cf2 (data[\cf7 "data"\cf2 ], \cf8 1\cf2 ):\
                  title = item.get(\cf7 "title"\cf2 , \cf7 ""\cf2 )\
                  url = item.get(\cf7 "url"\cf2 , \cf7 ""\cf2 )\
                  summary = item.get(\cf7 "summary_ai"\cf2 ) \cf3 or\cf2  item.get(\cf7 "summary"\cf2 , \cf7 ""\cf2 )\
                  page_time = item.get(\cf7 "page_time"\cf2 , \cf7 ""\cf2 )\
\
                  \cf8 #\cf2  \cf8 \uc0\u36755 \u20986 \u27599 \u26465 \u32467 \u26524 \cf2 \
                  \cf3 yield\cf2  self.create_text_message(\
                      \cf7 f"\\n\{i\}.\cf2  \cf7 \{title\}\\n"\cf2 \
                      \cf7 f"\cf2    \cf7 \{summary\}\\n"\cf2 \
                      \cf7 f"\cf2    \cf7 \uc0\u55357 \u56599 \cf2  \cf7 \{url\}\\n"\cf2 \
                      \cf7 f"\cf2    \cf7 \uc0\u9200 \cf2  \cf7 \{page_time\}\\n"\cf2 \
                  )\
\
                  results.append(\{\
                      \cf7 "title"\cf2 : title,\
                      \cf7 "url"\cf2 : url,\
                      \cf7 "summary"\cf2 : summary,\
                      \cf7 "page_time"\cf2 : page_time\
                  \})\
\
              \cf8 #\cf2  \cf8 \uc0\u36820 \u22238 JSON\u26684 \u24335 \u20379 AI\u22788 \u29702 \cf2 \
              \cf3 yield\cf2  self.create_json_message(\{\
                  \cf7 "query"\cf2 : query,\
                  \cf7 "total"\cf2 : \cf6 len\cf2 (results),\
                  \cf7 "results"\cf2 : results\
              \})\
\
          \cf3 except\cf2  requests.RequestException \cf3 as\cf2  e:\
              \cf3 yield\cf2  self.create_text_message(\cf7 f"\uc0\u32593 \u32476 \u35831 \u27714 \u22833 \u36133 :\cf2  \cf7 \{\cf6 str\cf7 (e)\}"\cf2 )\
          \cf3 except\cf2  Exception \cf3 as\cf2  e:\
              \cf3 yield\cf2  self.create_text_message(\cf7 f"\uc0\u25628 \u32034 \u20986 \u38169 :\cf2  \cf7 \{\cf6 str\cf7 (e)\}"\cf2 )}