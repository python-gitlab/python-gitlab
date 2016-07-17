class _StdoutStream(object):
    def __call__(self, chunk):
        print(chunk)


def response_content(response, streamed, action, chunk_size):
    if streamed is False:
        return response.content

    if action is None:
        action = _StdoutStream()

    for chunk in response.iter_content(chunk_size=chunk_size):
        if chunk:
            action(chunk)
