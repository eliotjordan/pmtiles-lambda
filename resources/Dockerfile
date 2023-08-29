FROM public.ecr.aws/a9s2e4u8/pmtiles_base:latest

RUN pip install fastapi mangum>=0.17.0 numpy pydantic urllib3 -t /var/task

RUN pip install aiofiles

WORKDIR /var/task

COPY handler.py /var/task/handler.py

ENTRYPOINT [ "/var/lang/bin/python", "-m", "awslambdaric" ]

CMD [ "handler.handler" ]
