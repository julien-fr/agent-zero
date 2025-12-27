"""Mock whisper module for testing."""

def load_model(name):
    class MockModel:
        def transcribe(self, audio, **kwargs):
            return {"text": "mock transcription"}
    return MockModel()

class Whisper:
    @staticmethod
    def load_model(name):
        return MockModel()

