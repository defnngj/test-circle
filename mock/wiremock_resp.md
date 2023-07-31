
# wiremock 响应模板

## 动态response使用例子

### xPath用法

从xml请求体重提取数据

* xml文件(output.xml)

```xml
<?xml version="1.0"?>
<output>
    <xpathText>{{xPath request.body '/outer/inner/text()'}}</xpathText>
    <xpath>{{xPath request.body '/outer/inner'}}</xpath>
</output>
```

* 拷贝到docker 容器中

```bash
docker cp /home/xxx/wiremock/files/output.xml 8ad4a2b31fc1:/home/wiremock/__files/
```

`/home/xxx/wiremock/files/output.xml` 宿主机地址。

`8ad4a2b31fc1` 容器ID。

`/home/wiremock/__files/` 容器里面路径。

* 创建接口

```bash
curl --request POST \
  --url http://10.2.180.77:8080/__admin/mappings \
  --header 'content-type: application/json' \
  --data '{
    "request": {
        "method": "POST",
        "url": "/v1/mock/resp_xml_templating"
    },
    "response": {
        "status": 200,
        "bodyFileName": "output.xml",
        "headers": {
            "Content-Type": "application/xml"
        },
        "transformers": ["response-template"]
    }
}'
```

* 请求

```xml
<outer>
    <inner>Stuff</inner>
</outer>
```

* 响应

```xml
<?xml version="1.0"?>
<output>
    <xpathText>
        Stuff
    </xpathText>
    <xpath>
        &lt;inner&gt;Stuff&lt;/inner&gt;
    </xpath>
</output>
```

### xPath高级用法

返回的节点对象具有以下属性: 
 
name—本地XML元素名称。 
 
text-元素的文本内容。 
 
attributes—元素属性的映射(name: value)


* xml文件(output2.xml)

```xml
<?xml version="1.0"?>
<output>
    <xpath>{{#each (xPath request.body '/things/item') as |node|}}name: {{node.name}}, text: {{node.text}}, ID attribute: {{node.attributes.id}}{{/each}}</xpath>
</output>
```

* 创建接口

```bash
curl --request POST \
  --url http://10.2.180.77:8080/__admin/mappings \
  --header 'content-type: application/json' \
  --data '{
    "request": {
        "method": "POST",
        "url": "/v2/mock/resp_xml_templating"
    },
    "response": {
        "status": 200,
        "bodyFileName": "output2.xml",
        "headers": {
            "Content-Type": "application/xml"
        },
        "transformers": ["response-template"]
    }
}'
```

* 请求

```xml
<things>
    <item id="111">hello</item>
</things>
```

* 响应

```xml
<?xml version="1.0"?>
   <output>
      <xpath>
         name: item, text: hello, ID attribute: 111
      </xpath>
</output>
```


### soapPath用法

从soap请求体重提取数据

* xml文件（output_soap.xml）

```xml
<?xml version="1.0"?>
<soap:Envelope
xmlns:soap="http://www.w3.org/2001/12/soap-envelope"
soap:encodingStyle="http://www.w3.org/2001/12/soap-encoding">

<soap:Body xmlns:m="http://www.example.org/stock">
  <m:GetStockPriceResponse>
    <m:Result>{{soapXPath request.body '/a/test/text()'}}</m:Result>
  </m:GetStockPriceResponse>
</soap:Body>

</soap:Envelope>
```

* 创建接口

```bash
curl --request POST \
  --url http://10.2.180.77:8080/__admin/mappings \
  --header 'content-type: application/json' \
  --data '{
    "request": {
        "method": "POST",
        "url": "/v3/mock/resp_xml_templating"
    },
    "response": {
        "status": 200,
        "bodyFileName": "output_soap.xml",
        "headers": {
            "Content-Type": "application/xml"
        },
        "transformers": ["response-template"]
    }
}'
```

* 请求

```xml
<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope/">
    <soap:Body>
        <m:a>
            <m:test>success</m:test>
        </m:a>
    </soap:Body>
</soap:Envelope>
```

* 响应

```json
<?xml version="1.0"?>
   <soap:Envelopexmlns:soap="http://www.w3.org/2001/12/soap-envelope"soap:encodingStyle="http://www.w3.org/2001/12/soap-encoding">
      <soap:Body xmlns:m="http://www.example.org/stock">
         <m:GetStockPriceResponse>
            <m:Result>
               success
            </m:Result>
</m:GetStockPriceResponse>
</soap:Body>
</soap:Envelope>
```

### jsonPath 用法

从请求体的 body 中提取 name 填充到 response 中。


* 创建接口

```bash
curl --location 'http://127.0.0.1:8090/__admin/mappings' \
--header 'Content-Type: application/json' \
--data '{
    "request": {
        "method": "POST",
        "url": "/v1/mock/req_matching"
    },
    "response": {
        "status": 200,
        "jsonBody": {
            "status": true,
            "message": "success",
            "result": {
                "Hello": "{{jsonPath request.body '\''$.name'\''}}"
            }
        },
        "headers": {
            "Content-Type": "application/json"
        }
    }
}'
```

* 请求

```json
{
    "name": "jack"
}
```

* 响应

```json
{
    "status": true,
    "message": "success",
    "result": {
        "Hello": "jack"
    }
}
```

### Parse JSON 用法

ParseJSON 可以把 JSON结构体变成一个对象，然后通过这个对象，在进一步提取数据。

* 创建接口

```bash
curl --location 'http://127.0.0.1:8090/__admin/mappings' \
--header 'Content-Type: application/json' \
--data '{
    "request": {
        "method": "POST",
        "url": "/v5/mock/resp_templating"
    },
    "response": {
        "status": 200,
        "jsonBody": {
            "status": true,
            "message": "success",
            "result": {
                "jsonBody": "{{parseJson request.body '\''bodyJson'\''}}{{bodyJson.name}}",
                "find": "{{lookup (parseJson request.body) '\''age'\''}}"
            }
        },
        "headers": {
            "Content-Type": "application/json"
        }
    }
}'
```

* 请求

```json
{
    "name": "jack",
    "items": {
        "age":11
    }
}
```

* 响应

```json
{
    "status": true,
    "message": "success",
    "result": {
        "jsonBody": "jack",
        "find": "{name&#x3D;jack, items&#x3D;{age&#x3D;11}}"
    }
}
```

### 日期时间使用

* 创建接口

```bash
curl --location 'http://127.0.0.1:8090/__admin/mappings' \
--header 'Content-Type: application/json' \
--data '{
    "request": {
        "method": "POST",
        "url": "/v6/mock/resp_templating"
    },
    "response": {
        "status": 200,
        "jsonBody": {
            "status": true,
            "message": "success",
            "result": {
                "now1": "{{now}}",
                "now2": "{{now offset='\''3 days'\''}}",
                "now3": "{{now offset='\''-24 seconds'\''}}",
                "now4": "{{now offset='\''1 years'\''}}",
                "now5": "{{now offset='\''10 years'\'' format='\''yyyy-MM-dd'\''}}",
                "now6": "{{now timezone='\''Australia/Sydney'\'' format='\''yyyy-MM-dd HH:mm:ssZ'\''}}",
                "now7": "{{now offset='\''2 years'\'' format='\''epoch'\''}}",
                "now8": "{{now offset='\''2 years'\'' format='\''unix'\''}}"
            }
        },
        "headers": {
            "Content-Type": "application/json"
        }
    }
}'
```

* 请求

```json
{}
```

* 响应

```json
{
    "status": true,
    "message": "success",
    "result": {
        "now1": "2023-07-30T14:29:41Z",
        "now2": "2023-08-02T14:29:41Z",
        "now3": "2023-07-30T14:29:17Z",
        "now4": "2024-07-30T14:29:41Z",
        "now5": "2033-07-30",
        "now6": "2023-07-31 00:29:41+1000",
        "now7": "1753885781413",
        "now8": "1753885781"
    }
}
```


### 随机数使用1

* 创建接口

```bash
curl --location 'http://127.0.0.1:8090/__admin/mappings' \
--header 'Content-Type: application/json' \
--data '{
    "request": {
        "method": "POST",
        "url": "/v7/mock/resp_templating"
    },
    "response": {
        "status": 200,
        "jsonBody": {
            "status": true,
            "message": "success",
            "result": {
                "random1": "{{randomValue length=33 type='\''ALPHANUMERIC'\''}}",
                "random2": "{{randomValue length=12 type='\''ALPHANUMERIC'\'' uppercase=true}}",
                "random3": "{{randomValue length=55 type='\''ALPHABETIC'\''}}",
                "random4": "{{randomValue length=27 type='\''ALPHABETIC'\'' uppercase=true}}",
                "random5": "{{randomValue length=10 type='\''NUMERIC'\''}}",
                "random6": "{{randomValue length=5 type='\''ALPHANUMERIC_AND_SYMBOLS'\''}}",
                "random7": "{{randomValue type='\''UUID'\''}}",
                "random8": "{{randomValue length=32 type='\''HEXADECIMAL'\'' uppercase=true}}",
                "pickRandom1": "{{pickRandom '\''1'\'' '\''2'\'' '\''3'\''}}",
                "pickRandom2": "{{pickRandom (jsonPath request.body '\''$.names'\'')}}"
            }
        },
        "headers": {
            "Content-Type": "application/json"
        }
    }
}'
```

* 请求

```json
{
    "names": ["tom", "jack", "jerry"]
}
```

* 响应

```json
{
    "status": true,
    "message": "success",
    "result": {
        "random1": "smonbjvyppghawrdjwypsuishybxhlc6i",
        "random2": "LXVTQIASHWQO",
        "random3": "lufizqaoaebgvxtiuovepiutkikhmtuvcqtzumreadnmoqojergwbbk",
        "random4": "XVNUGPKNIALOTYDDEGZWVUTJHCI",
        "random5": "0222011363",
        "random6": "f.y&#x27;8",
        "random7": "a0fab894-dccd-4a06-b9c0-e9482f1d72d9",
        "random8": "1CC56A111230999B2529F4ED7D2F801A",
        "pickRandom1": "2",
        "pickRandom2": "jack"
    }
}
```

### 随机数使用2

* 创建接口

```bash
curl --location 'http://127.0.0.1:8090/__admin/mappings' \
--header 'Content-Type: application/json' \
--data '{
    "request": {
        "method": "POST",
        "url": "/v8/mock/resp_templating"
    },
    "response": {
        "status": 200,
        "jsonBody": {
            "status": true,
            "message": "success",
            "result": {
                "randomInt1": "{{randomInt}}",
                "randomInt2": "{{randomInt lower=5 upper=9}}",
                "randomInt3": "{{randomInt upper=54323}}",
                "randomInt4": "{{randomInt lower=-24}}",
                "randomDecimal1": "{{randomDecimal}}",
                "randomDecimal2": "{{randomDecimal lower=-10.1 upper=-0.9}}",
                "randomDecimal3": "{{randomDecimal upper=12.5}}",
                "randomDecimal4": "{{randomDecimal lower=-24.01}}"
            }
        },
        "headers": {
            "Content-Type": "application/json"
        }
    }
}'
```

* 请求

```json
{}
```

* 响应

```json
{
    "status": true,
    "message": "success",
    "result": {
        "randomInt1": "1187964902",
        "randomInt2": "6",
        "randomInt3": "-2002731563",
        "randomInt4": "1928991986",
        "randomDecimal1": "2.6989576813880077E307",
        "randomDecimal2": "-7.066690883970283",
        "randomDecimal3": "9.541102612120222",
        "randomDecimal4": "1.0078909472313308E308"
    }
}
```

### 数学公式使用

* 创建接口

```bash
curl --location 'http://127.0.0.1:8090/__admin/mappings' \
--header 'Content-Type: application/json' \
--data '{
    "request": {
        "method": "POST",
        "url": "/v9/mock/resp_templating"
    },
    "response": {
        "status": 200,
        "jsonBody": {
            "status": true,
            "message": "success",
            "result": {
                "math1": "{{math 1 '\''+'\'' 2}}",
                "math2": "{{math 4 '\''-'\'' 2}}",
                "math3": "{{math 2 '\''*'\'' 3}}",
                "math4": "{{math 8 '\''/'\'' 2}}",
                "math5": "{{math 10 '\''%'\'' 3}}"
            }
        },
        "headers": {
            "Content-Type": "application/json"
        }
    }
}'
```

* 请求

```json
{}
```

* 响应

```json
{
    "status": true,
    "message": "success",
    "result": {
        "math1": "3",
        "math2": "2",
        "math3": "6",
        "math4": "4",
        "math5": "1"
    }
}
```

## 循环使用

* 创建接口

```bash
curl --location 'http://127.0.0.1:8090/__admin/mappings' \
--header 'Content-Type: application/json' \
--data '{
    "request": {
        "method": "POST",
        "url": "/v10/mock/resp_templating"
    },
    "response": {
        "status": 200,
        "jsonBody": {
            "status": true,
            "message": "success",
            "result": {
                "range1": "{{range 3 8}}",
                "range2": "{{range -2 2}}",
                "range3": "{{#each (range 0 (randomInt lower=1 upper=10)) as |index|}} id: {{index}}{{/each}}"
            }
        },
        "headers": {
            "Content-Type": "application/json"
        }
    }
}'
```

* 请求

```json
{}
```

* 响应

```json
{
    "status": true,
    "message": "success",
    "result": {
        "range1": "[3, 4, 5, 6, 7, 8]",
        "range2": "[-2, -1, 0, 1, 2]",
        "range3": " id: 0 id: 1 id: 2 id: 3 id: 4 id: 5 id: 6 id: 7 id: 8 id: 9"
    }
}
```

### 数组使用

* 创建接口

```bash
curl --location 'http://127.0.0.1:8090/__admin/mappings' \
--header 'Content-Type: application/json' \
--data '{
    "request": {
        "method": "POST",
        "url": "/v11/mock/resp_templating"
    },
    "response": {
        "status": 200,
        "jsonBody": {
            "status": true,
            "message": "success",
            "result": {
                "array1": "{{array 1 '\''two'\'' true}}",
                "array2": "{{array}}"
            }
        },
        "headers": {
            "Content-Type": "application/json"
        }
    }
}'
```

* 请求

```json
{}
```

* 响应

```json
{
    "status": true,
    "message": "success",
    "result": {
        "array1": "[1, two, true]",
        "array2": "[]"
    }
}
```

### if判断使用

* 创建接口

```bash
curl --location 'http://127.0.0.1:8090/__admin/mappings' \
--header 'Content-Type: application/json' \
--data '{
    "request": {
        "method": "POST",
        "url": "/v12/mock/resp_templating"
    },
    "response": {
        "status": 200,
        "jsonBody": {
            "status": true,
            "message": "success",
            "result": {
                "if1": "{{#if (contains '\''abcde'\'' '\''abc'\'')}}YES{{/if}}",
                "if2": "{{#if (contains (array '\''a'\'' '\''b'\'' '\''c'\'') '\''a'\'')}}YES{{/if}}",
                "contains1": "{{#contains '\''abcde'\'' '\''abc'\''}}YES{{/contains}}",
                "contains2": "{{#contains (array '\''a'\'' '\''b'\'' '\''c'\'') '\''a'\''}}YES{{/contains}}"
            }
        },
        "headers": {
            "Content-Type": "application/json"
        }
    }
}'
```

* 请求

```json
{}
```

* 响应

```json
{
    "status": true,
    "message": "success",
    "result": {
        "if1": "YES",
        "if2": "YES",
        "contains1": "YES",
        "contains2": "YES"
    }
}
```

### 循环请求列表使用

* 创建接口

```bash
curl --location 'http://127.0.0.1:8090/__admin/mappings' \
--header 'Content-Type: application/json' \
--data '{
    "request": {
        "method": "POST",
        "url": "/v1/test"
    },
    "response": {
        "status": 200,
        "jsonBody": {
            "status": true,
            "message": "success",
            "result": {
                "data": "{{#each (jsonPath request.body '\''$.data'\'') as |data|}}data: {{data}}{{/each}}"
            }
        },
        "headers": {
            "Content-Type": "application/json"
        }
    }
}'
```

* 请求

```json
{
    "data": ["a,", "b,", "c,"]
}
```

* 响应

```json
{
    "status": true,
    "message": "success",
    "result": {
        "data": "data: a,data: b,data: c,"
    }
}
```