# nodebin

Aliyun mirror | 阿里云镜像 for nodebin.herokai.com

## Features

- Same API with nodebin.herokai.com, which provides binaries for node, yarn and iojs.
- Replaced binary addresses by aliyun mirror, which can be used in Mainland China

## Getting Started

- Officially deployed service at https://nodebin.jxltom.com.

- Deploy to Heroku by [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/jxltom/nodebin)

- Deploy to AWS Lambda by setting up AWS credentials by environment variables, ```pipenv shell```, and ```zappa deploy dev|test|prod```

## Known Issues

- Unencoded Caret in query string in server deployed in AWS Lambda with API Gateway is not supported. It must be encoded as ```%5E``` such as ```https://nodebin.jxltom.com/v1/node/linux-x64?range=%5E8.1```
