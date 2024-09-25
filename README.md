# bron-llm-cohere
Use bron as RAG with [CoHere](https://cohere.com/)

## installation

1. `git pull`
2. modify the docker-compose.yml file so that a CO_API_KEY is exposed with your CoHere API Key, like below
3. `cd docker`
4. `docker-compose up -d`
5. `docker exec -it bron-llm_shell_1 ./llm.py`

## example docker-compose with CoHere API key 
```
version: "3.7"
services:
   shell:
    build:
      context: .
      dockerfile: Dockerfile
    environment:
      - "CO_API_KEY=xxxxx"
    volumes:
      - ../:/opt/bron-llm
    networks:
      - bron-llm
    restart: always
networks:
  bron-llm:

```
