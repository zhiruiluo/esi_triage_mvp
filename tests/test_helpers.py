class FakeUsage:
    def __init__(self, prompt_tokens=10, completion_tokens=5, total_tokens=15):
        self.prompt_tokens = prompt_tokens
        self.completion_tokens = completion_tokens
        self.total_tokens = total_tokens


class FakeMessage:
    def __init__(self, content: str):
        self.content = content


class FakeChoice:
    def __init__(self, content: str):
        self.message = FakeMessage(content)


class FakeResponse:
    def __init__(self, content: str):
        self.choices = [FakeChoice(content)]
        self.usage = FakeUsage()


class FakeChat:
    def __init__(self, content: str):
        self._content = content

    async def create(self, **_kwargs):
        return FakeResponse(self._content)


class FakeCompletions:
    def __init__(self, content: str):
        self.chat = type("ChatHolder", (), {"completions": FakeChat(content)})()


class FakeAsyncOpenAI:
    def __init__(self, content: str):
        self.chat = type("ChatHolder", (), {"completions": FakeChat(content)})()
