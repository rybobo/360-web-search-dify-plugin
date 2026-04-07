{\rtf1\ansi\ansicpg936\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fnil\fcharset0 Menlo-Regular;}
{\colortbl;\red255\green255\blue255;\red0\green0\blue0;\red64\green11\blue217;\red159\green160\blue28;
\red46\green174\blue187;\red180\green36\blue25;\red47\green180\blue29;}
{\*\expandedcolortbl;;\csgray\c0;\cssrgb\c32309\c18666\c88229;\cssrgb\c68469\c68012\c14211;
\cssrgb\c20199\c73241\c78251;\cssrgb\c76411\c21697\c12527;\cssrgb\c20241\c73898\c14950;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx560\tx1120\tx1680\tx2240\tx2800\tx3360\tx3920\tx4480\tx5040\tx5600\tx6160\tx6720\pardirnatural\partightenfactor0

\f0\fs22 \cf2 \CocoaLigature0   \cf3 from\cf2  dify_plugin \cf3 import\cf2  ToolProvider\
  \cf3 from\cf2  dify_plugin.errors.tool \cf3 import\cf2  ToolProviderCredentialValidationError\
  \cf3 from\cf2  tools.web_search \cf3 import\cf2  WebSearchTool\
  \cf3 import\cf2  requests\
\
  \cf3 class\cf2  \cf3 Qihoo360Provider(ToolProvider):\cf2 \
      \cf3 def\cf4  _validate_credentials(self,\cf2  \cf4 credentials:\cf2  \cf5 dict\cf4 )\cf2  \cf4 ->\cf2  \cf3 None\cf4 :\cf2 \
          \cf6 """\uc0\u39564 \u35777 API\u23494 \u38053 """\cf2 \
          \cf3 try\cf2 :\
              api_key = credentials.get(\cf6 "api_key"\cf2 )\
              \cf7 #\cf2  \cf7 \uc0\u35843 \u29992 \u19968 \u27425 API\u39564 \u35777 \u23494 \u38053 \cf2 \
              response = requests.get(\
                  \cf6 "https://api.360.cn/v2/mwebsearch"\cf2 ,\
                  headers=\{\cf6 "Authorization"\cf2 : \cf6 f"Bearer\cf2  \cf6 \{api_key\}"\cf2 \},\
                  params=\{\cf6 "q"\cf2 : \cf6 "test"\cf2 , \cf6 "ref_prom"\cf2 : \cf6 "aiso-pro"\cf2 , \cf6 "sid"\cf2 : \cf6 "test"\cf2 \},\
                  timeout=\cf7 5\cf2 \
              )\
              \cf3 if\cf2  response.status_code == \cf7 401\cf2 :\
                  \cf3 raise\cf2  ToolProviderCredentialValidationError(\cf6 "API\uc0\u23494 \u38053 \u26080 \u25928 "\cf2 )\
          \cf3 except\cf2  Exception \cf3 as\cf2  e:\
              \cf3 raise\cf2  ToolProviderCredentialValidationError(\cf6 f"\uc0\u39564 \u35777 \u22833 \u36133 :\cf2  \cf6 \{\cf5 str\cf6 (e)\}"\cf2 )}